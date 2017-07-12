'use strict';
var $ = require( 'jquery' );
var _ = require( 'underscore' );
var Backbone = require( 'backbone' );
var Helpers = require( '../helpers' );
var Resources = require( '../resources' );
Backbone.$ = $;

var MetaModel = Backbone.Model.extend( {

  constructor: function( properties ) {
    var k;

    if ( typeof properties !== 'undefined' ) {
      for ( k in properties ) {
        if ( properties.hasOwnProperty( k ) ) {
          this[k] = properties[k];
        }
      }
    }

    // in the case of reg-model
    // an index of all of the entities in the reg, whether or not they've been loaded
    this.content = this.content || {};

    // in the case of reg-model
    // content = markup to string representations of each reg paragraph/entity
    // loaded into the browser (rendered or not)
    this.structure = this.structure || [];

    Backbone.Model.apply( this, arguments );
  },

  set: function( sectionId, sectionValue ) {
    var cached = this.has( sectionId ),
        section;

    if ( typeof sectionId !== 'undefined' && !_.isEmpty( sectionId ) ) {
      if ( !cached ) {
        this.content[sectionId] = sectionValue;
        section = sectionValue;

        if ( _.indexOf( this.structure, sectionId ) === -1 ) {
          this.structure.push( sectionId );
        }
      }
      else {
        section = cached;
      }
    }
    return section;
  },

  // **Param**
  // id, string, dash-delimited reg entity id
  //
  // **Returns** boolean
  has: function( id ) {
    return this.content[id] ? true : false;
  },

  // **Params**
  //
  // * ```id```: string, dash-delimited reg entity id
  // * ```callback```: function to be called once content is loaded
  get: function( id, callback ) {
    var $promise, resolve;

    // if we have the requested content cached, retrieve it
    // otherwise, we need to ask the server for it
    $promise = this.has( id ) ? this.retrieve( id ) : this.request( id );

    // callback once the promise resolves
    resolve = function( response ) {
      if ( typeof callback !== 'undefined' ) {
        callback( true, response );
      }
    };

    $promise.done( resolve );

    $promise.fail( function() {
      callback( false );
    } );

    return this;
  },

  // basically returns ```this.content[id]``` immediately,
  // but is consistent with the interface that ```this.request``` provides
  retrieve: function( id ) {
    var $deferred = $.Deferred();

    $deferred.resolve( this.content[id] );

    return $deferred.promise();
  },

  request: function( id ) {
    var url = this.getAJAXUrl( id ),
        $promise;

    $promise = $.ajax( {
      url: url,
      success: function( data ) { this.set( id, data ); }.bind( this )
    } );

    return $promise;
  },

  getAJAXUrl: function( id ) {
    var url,
        urlPrefix = window.APP_PREFIX;

    if ( urlPrefix ) {
      url = urlPrefix + 'partial/';
    }
    else {
      url = '/partial/';
    }

    if ( typeof this.supplementalPath !== 'undefined' ) {
      url += this.supplementalPath + '/';
    }

    url += id;

    if ( id.indexOf( '/' ) === -1 ) {
      url += '/' + Helpers.findVersion( Resources.versionElements );
    }

    return url;
  }
} );

module.exports = MetaModel;
