'use strict';
var $ = require( 'jquery' );
var _ = require( 'underscore' );
var Backbone = require( 'backbone' );
require( '../../events/scroll-stop.js' );
var DefinitionView = require( '../sidebar/definition-view' );
var RegModel = require( '../../models/reg-model' );
var SectionFooterView = require( './section-footer-view' );
var Router = require( '../../router' );
var MainEvents = require( '../../events/main-events' );
var HeaderEvents = require( '../../events/header-events' );
var SidebarEvents = require( '../../events/sidebar-events' );
var Helpers = require( '../../helpers' );
var DrawerEvents = require( '../../events/drawer-events' );
var ChildView = require( './child-view' );
var GAEvents = require( '../../events/ga-events' );
Backbone.$ = $;

var RegView = ChildView.extend( {
  el: '#content-wrapper',

  events: {
    'click .definition': 'termLinkHandler',
    'click .inline-interp-header': 'expandInterp',
    'click .internal': 'logCitation'
  },

  initialize: function() {
    this.externalEvents = MainEvents;
    this.listenTo( this.externalEvents, 'section:rendered', ChildView.setElement );

    this.listenTo( this.externalEvents, 'definition:close', this.closeDefinition );
    this.listenTo( this.externalEvents, 'definition:carriedOver', this.checkDefinitionScope );
    this.listenTo( this.externalEvents, 'paragraph:active', this.newActiveParagraph );

    DrawerEvents.trigger( 'pane:init', 'table-of-contents' );

    this.id = this.options.id;
    this.regVersion = this.options.regVersion;
    this.activeSection = this.options.id;
    this.$activeSection = $( '#' + this.activeSection );
    this.$sections = {};
    this.url = this.id + '/' + this.options.regVersion;
    this.regPart = this.options.regPart;
    this.cfrTitle = this.options.cfrTitle;

    if ( typeof this.options.subContentType !== 'undefined' ) {
      this.subContentType = this.options.subContentType;
    }

    HeaderEvents.trigger( 'section:open', this.activeSection );

    if ( Router.hasPushState ) {
      this.events['click .inline-interpretation .section-link'] = 'openInterp';
      this.events['click .citation.internal'] = 'openSection';
      this.events['click .section-nav .navigation-link'] = 'openSection';
      this.delegateEvents();
    }

    ChildView.prototype.initialize.apply( this, arguments );

    this.loadImages();
  },

  // only concerned with resetting DOM, no matter
  // what way the definition was closed
  closeDefinition: function() {
    this.clearActiveTerms();
  },

  toggleDefinition: function( $link ) {
    this.setActiveTerm( $link );

    return this;
  },

  openSection: function( e ) {
    var $e = $( e.target ),
        id = $e.attr( 'data-section-id' ) || $e.attr( 'data-linked-section' ),
        href = $e.attr( 'href' ),
        config = {},
        hashIndex;

    if ( typeof href !== 'undefined' ) {
      hashIndex = href.indexOf( '#' );
    }

    if ( id.length > 0 ) {
      e.preventDefault();
      config.id = id;

      if ( hashIndex !== -1 ) {
        config.scrollToId = href.substr( hashIndex + 1 );
      }

      this.externalEvents.trigger( 'section:open', Helpers.findBaseSection( id ), config, 'reg-section' );
    }
  },

  assembleTitle: function() {
    var newTitle;
    if ( typeof this.subContentType !== 'undefined' ) {
      if ( this.subContentType === 'supplement' ) {
        newTitle = 'Supplement I to Part ' + this.regPart + ' | eRegulations';
      }
      else if ( this.subContentType === 'appendix' ) {
        newTitle = 'Appendix ' + this.id.substr( this.id.length - 1 ) + ' to Part ' + this.regPart + ' | eRegulations';

      }
    }
    else {
      newTitle = this.cfrTitle + ' CFR ' + Helpers.idToRef( this.id ) + ' | eRegulations';
    }

    return newTitle;
  },

  // if an inline definition is open, check the links here to see
  // if the definition is still in scope in this section
  checkDefinitionScope: function() {
    var $def = $( '#definition' ),
        defTerm = $def.data( 'defined-term' ),
        defId = $def.find( '.open-definition' ).attr( 'id' ),
        $termLinks,
        eventTriggered = false;

    if ( defTerm && defId && $def.length > 0 ) {
      this.defScopeExclusions = this.defScopeExclusions || [];
      $termLinks = this.$el.find( 'a.definition' );

      $termLinks.each( function( i, link ) {
        var $link = $( link );

        if ( $link.data( 'defined-term' ) === defTerm && $link.data( 'definition' ) !== defId ) {
          // don't change the DOM over and over for no reason
          // if there are multiple defined term links that
          // are scoped to a different definition body
          if ( !eventTriggered ) {
            SidebarEvents.trigger( 'definition:outOfScope', this.id );
            eventTriggered = true;
          }

          this.defScopeExclusions.push( $link.closest( 'li[data-permalink-section]' ).attr( 'id' ) );
        }
      }.bind( this ) );

      if ( this.defScopeExclusions.length === 0 ) {
        SidebarEvents.trigger( 'definition:inScope' );
      }
    }
  },

  // id = active paragraph
  newActiveParagraph: function( id ) {
    var $newDefLink, newDefId, newDefHref;
    // if there are paragraphs where the open definition is
    // out of scope, display message
    // else be sure there's no out of scope message displayed
    if ( typeof this.defScopeExclusions !== 'undefined' ) {
      if ( this.defScopeExclusions.indexOf( id ) !== -1 ) {
        $newDefLink = this.$activeSection.find(
          '.definition[data-defined-term="' + $( '#definition' ).data( 'definedTerm' ) + '"]'
        ).first();
        newDefId = $newDefLink.data( 'definition' );
        newDefHref = $newDefLink.attr( 'href' );

        SidebarEvents.trigger( 'definition:deactivate', newDefId, newDefHref, this.activeSection );
      }
      else {
        SidebarEvents.trigger( 'definition:activate' );
      }
    }
  },

  render: function() {
    ChildView.prototype.render.apply( this, arguments );

    this.checkDefinitionScope();

    this.loadImages();
  },

  openDef: function( defId, term, $link ) {
    // if its the same definition, diff term link
    if ( $( '.open-definition' ).attr( 'id' ) === defId ) {
      this.toggleDefinition( $link );
    }
    else {
      // close old definition, if there is one
      SidebarEvents.trigger( 'definition:close' );
      // open new definition
      this.setActiveTerm( $link );
      SidebarEvents.trigger( 'definition:open', {
        id: defId,
        term: term
      } );
    }
    GAEvents.sendEvent( 'definition:open', term );
  },

  // content section key term link click handler
  termLinkHandler: function( e ) {
    e.preventDefault();

    var $link = $( e.target ),
        defId = $link.data( 'definition' ),
        term = $link.data( 'defined-term' );

        // if this link is already active, toggle def shut
    if ( $link.data( 'active' ) ) {
      SidebarEvents.trigger( 'definition:close' );
      GAEvents.sendEvent( 'definition:close', defId );
      this.clearActiveTerms();
    }
    else {
      this.openDef( defId, term, $link );
    }

    return this;
  },

  // handler for when inline interpretation is clicked
  expandInterp: function( e ) {
    // user can click anywhere in the header of a closed interp
    // for an open interp, they can click "hide" button or header
    e.stopImmediatePropagation();
    e.preventDefault();
    var header = $( e.currentTarget ),
        section = header.parent(),
        button = header.find( '.expand-button' ),
        buttonText = header.find( '.expand-text' ),
        context = {
          id: section.data( 'interp-id' ),
          to: section.data( 'interp-for' ),
          type: 'inline-interp'
        };

    section.toggleClass( 'open' );
    //  may include multiple sections
    section.find( '.hidden' ).slideToggle();
    button.toggleClass( 'open' );
    buttonText.html( section.hasClass( 'open' ) ? 'Hide' : 'Show' );

    if ( section.hasClass( 'open' ) && section.hasClass( 'inline-interpretation' ) ) {
      GAEvents.sendEvent( 'interpexpandables:open', context.to );
    }
    else if ( section.hasClass( 'inline-interpretation' ) ) {
      GAEvents.sendEvent( 'interpexpandables:close', context.to );
    }

    return this;
  },

  // Sets DOM back to neutral state
  clearActiveTerms: function() {
    this.$el.find( '.active.definition' )
      .removeClass( 'active' )
      .removeData( 'active' );
  },

  setActiveTerm: function( $link ) {
    this.clearActiveTerms();
    $link.addClass( 'active' ).data( 'active', 1 );
  },

  openInterp: function( e ) {
    e.preventDefault();

    var sectionId = $( e.currentTarget ).data( 'linked-section' ),
        subSectionId = $( e.currentTarget ).data( 'linked-subsection' ),
        version = $( 'section[data-base-version]' ).data( 'base-version' );

    Router.navigate( sectionId + '/' + version + '#' + subSectionId, { trigger: true } );

    GAEvents.sendEvent( 'interp:followCitation', subSectionId );
  },

  // lazy load images as the user scrolls
  loadImages: function() {
    // require inside of the loadImages function to accomodate testing dependencies
    var unveil = require( 'unveilable' );
    $( '.reg-image' ).unveil();
  },

  logCitation: function( e ) {
    var $e = $( e.target );

    if ( $e.hasClass( 'citation' ) ) {
      GAEvents.sendEvent( 'link:followCitation', $e.data( 'section-id' ) );
    }

  }
} );

module.exports = RegView;
