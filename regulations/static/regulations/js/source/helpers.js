// Defines some globally useful helper functions
'use strict';
var $ = require( 'jquery' );
var _ = require( 'underscore' );

// indexOf polyfill
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/indexOf
// TODO this may make sense to move elsewhere
if ( !Array.prototype.indexOf ) {
  Array.prototype.indexOf = function( searchElement, fromIndex ) {
    if ( this === undefined || this === null ) {
      throw new TypeError( '"this" is null or not defined' );
    }

    var length = this.length >>> 0; // Hack to convert object.length to a UInt32

    fromIndex = Number( fromIndex ) || 0;

    if ( Math.abs( fromIndex ) === Infinity ) {
      fromIndex = 0;
    }

    if ( fromIndex < 0 ) {
      fromIndex += length;
      if ( fromIndex < 0 ) {
        fromIndex = 0;
      }
    }

    for ( ;fromIndex < length; fromIndex++ ) {
      if ( this[fromIndex] === searchElement ) {
        return fromIndex;
      }
    }

    return -1;
  };
}

module.exports = {
  isIterable: function( obj ) {
    if ( typeof obj === 'array' || typeof obj === 'object' ) {
      return true;
    }
    return false;
  },

  // **Params**
  // ```interpParts```: Array of Strings or Numbers, entity that is
  // interpreted
  //
  // **Returns** human-readable representation of the reg section
  interpId: function( interpParts ) {
    if ( interpParts.length === 1 ) {
      return 'Supplement I to Part ';
    }
    else if ( isNaN( interpParts[1] ) ) {
      return 'Supplement I to Appendix ';
    }

    return 'Supplement I to ';

  },

  // **Params**
  // ```p0```: String or Number, section ID
  // ```p1```: String or Number, reg ID
  //
  // **Returns** human-readable representation of the reg section
  appendixId: function( part, letter ) {
    return 'Appendix ' + letter + ' to Part ' + part;
  },

  // **Param** dash-delimited string representation of reg entity ID
  //
  // **Returns** Reg entity marker formatted for human readability
  idToRef: function( id ) {
    var ref = '';
    var parts, i, len, dividers, item, interpIndex, interpParts, subpartIndex;
    parts = id.split( '-' );
    len = parts.length - 1;
    subpartIndex = parts.indexOf( 'Subpart' );
    dividers = [ '§ .', '', '( )', '( )', '( )', '( )' ];

    // if we've got only the reg part number
    if ( len === 0 ) {
      ref = parts[0];
      return ref;
    }

    // if there is a subpart
    if ( subpartIndex !== -1 ) {
      parts.splice( 1, subpartIndex );

      // subpartIndex is now the next part after "Subpart"
      // removes subpart letter
      if ( isNaN( parts[subpartIndex] ) && parts[subpartIndex] !== 'Interp' ) {
        parts.splice( 1, subpartIndex );
      }

      len = parts.length - 1;
    }

    // if we have a supplement
    interpIndex = parts.indexOf( 'Interp' );
    if ( interpIndex >= 0 ) {
      interpParts = parts.slice( 0, interpIndex );
      ref += this.interpId( interpParts );
    }
    // if we have an appendix
    else if ( isNaN( parseInt( parts[1], 10 ) ) ) {
      return this.appendixId( parts[0], parts[1] );
    }

    if ( interpParts ) {
      parts = _.compact( interpParts );
      len = parts.length - 1;
    }

    // we have a subpart interpretation to appendices
    if ( parts.indexOf( 'Appendices' ) !== -1 ) {
      return 'Supplement I to Appendices';
    }

    // the second part of a supplement to an appendix
    if ( len === 1 && isNaN( parts[1] ) ) {
      return ref += parts[1];
    }
    // we have a paragraph
    for ( i = 0; i <= len; i++ ) {
      // return part number alone
      if ( len < 1 ) {
        return ref += parts[i];
      }

      // top paragraph has no punctuation
      if ( i === 1 ) {
        ref += parts[i];
      } else {
        item = dividers[i].split( ' ' );
        ref += item[0] + parts[i] + item[1];
      }
    }


    return ref;

  },

  // Finds parent-most reg paragraph
  findBaseSection: function( id ) {
    var parts, interpIndex;

    if ( id.indexOf( '-' ) !== -1 ) {
      parts = id.split( '-' );
    }
    else {
      return id;
    }

    // if what has been passed in is a base section already
    // catches:
    // 123
    // 123-1
    // 123-A
    // 123-Interp
    if ( parts.length <= 2 ) {
      return id;
    }

    interpIndex = parts.indexOf( 'Interp' );

    if ( interpIndex !== -1 ) {
      // catches 123-Interp-h1
      if ( parts[1] === 'Interp' ) {
        return id;
      }
      // catches:
      // 123-4-Interp
      // 123-4-Interp-5
      // 123-Subpart-Interp
      // 123-Subpart-A-Interp
      // 123-Subpart-Interp-4
      // 123-Subpart-A-Interp-4
      // 123-Appendices-Interp
      // 123-Appendices-Interp-4

      return parts.slice( 0, interpIndex + 1 ).join( '-' );

    }

    // catches:
    // 123-4-*
    // 123-A-*
    return parts[0] + '-' + parts[1];
  },

  // Unpaired this function from the DOM to make
  // it more testable and flexible. Look at resources.js
  // to add places to look for version elements.
  // To call: `findVersion(Resources.versionElements)`

  // -- old message --
  // these next two are a little desperate and heavy handed
  // the next step, if the app were going to do more
  // interesting things, is to introduce the concept of reg
  // version and maybe effective dates to the architecture
  // at that time, this should be removed
  findVersion: function( versionElements ) {
    return $( versionElements.toc ).attr( 'data-toc-version' ) ||
                  $( versionElements.regLandingPage ).attr( 'data-base-version' ) ||
                  $( versionElements.timelineList ).find( '.stop-button' ).attr( 'data-version' );
    // includes .stop-button to be sure its not
    // the comparison version in diff mode
  },

  // returns newer version. findVersion will return base version
  findDiffVersion: function( versionElements, currentVersion ) {
    var version;
    currentVersion = currentVersion || this.findVersion( versionElements );
    version = $( versionElements.diffToc ).attr( 'data-from-version' );
    if ( !version || version === currentVersion ) {
      if ( $( versionElements.timelineList ).find( '.version-link' ).attr( 'data-version' ) !== currentVersion ) {
        version = $( versionElements.timelineList ).find( '.version-link' ).attr( 'data-version' );
      }
    }

    return version;
  },

  isSupplement: function( id ) {
    var parts;

    if ( typeof id !== 'undefined' ) {
      parts = _.compact( id.split( '-' ) );
      if ( parts.length < 2 ) {
        return false;
      }

      if ( parts[1].toLowerCase() === 'interp' ) {
        return true;
      }
    }

    return false;
  },

  isAppendix: function( id ) {
    var parts;

    if ( typeof id !== 'undefined' ) {
      parts = _.compact( id.split( '-' ) );
      if ( parts.length < 2 ) {
        return false;
      }

      if ( isNaN( parts[1] ) && parts[1].toLowerCase() !== 'interp' ) {
        return true;
      }
    }

    return false;
  },

  formatSubpartLabel: function( id ) {
    // accepts 123-Subpart-C
    var parts = id.split( '-' ),
        label = 'Subpart ';
    if ( isNaN( parts[0] ) === false && parts[1] === 'Subpart' ) {
      label += parts[2];
    }

    return label;
  },

  // accepts to params:
  // element to be expanded
  // animation duration
  toggleExpandable: function( $expandable, dur ) {
    $expandable.toggleClass( 'open' )
      .next( '.chunk' ).slideToggle( dur );
  },

  // thanks, James Padolsey http://james.padolsey.com/javascript/parsing-urls-with-the-dom/
  parseURL: function( url ) {
    var a = document.createElement( 'a' );
    a.href = url;
    return {
      source: url,
      protocol: a.protocol.replace( ':', '' ),
      host: a.hostname,
      port: a.port,
      query: a.search,
      params: ( function() {
        var ret = {},
            seg = a.search.replace( /^\?/, '' ).split( '&' ),
            len = seg.length,
            i = 0,
            s;
        for ( ;i < len; i++ ) {
          if ( !seg[i] ) { continue; }
          s = seg[i].split( '=' );
          ret[s[0]] = s[1];
        }
        return ret;
      } )(),
      hash: a.hash.replace( '#', '' ),
      path: a.pathname.replace( /^([^\/])/, '/$1' ),
      segments: a.pathname.replace( /^\//, '' ).split( '/' )
    };
  }
};
