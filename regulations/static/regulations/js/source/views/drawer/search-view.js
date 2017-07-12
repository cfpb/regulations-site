'use strict';
var $ = require( 'jquery' );
var _ = require( 'underscore' );
var Backbone = require( 'backbone' );
var Router = require( '../../router' );
var MainEvents = require( '../../events/main-events' );
var GAEvents = require( '../../events/ga-events' );
Backbone.$ = $;

var SearchView = Backbone.View.extend( {
  el: '#search',

  events: {
    'change #version-select': 'logSearchVersion',
    'submit': 'openSearchResults'
  },

  initialize: function() {
    // if the browser doesn't support pushState, don't
    // trigger click events for links
    if ( Router.hasPushState === false ) {
      this.events = {};
    }
  },

  logSearchVersion: function( e ) {
    var version = $( e.target ).val();
    GAEvents.sendEvent( 'searchVersion:change', version );
  },

  openSearchResults: function( e ) {
    sessionStorage.setItem( 'drawerDefault', 'search' );

    e.preventDefault();
    var $form = $( e.target ),
        options = {};

    options.query = $form.find( 'input[name=q]' )[0].value;
    options.searchVersion = $form.find( 'select[name=version]' )[0].value;
    MainEvents.trigger( 'search-results:open', null, options, 'search-results' );
  }

} );

module.exports = SearchView;
