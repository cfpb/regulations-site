'use strict';
var $ = require( 'jquery' );
var _ = require( 'underscore' );
var Backbone = require( 'backbone' );
var Router = require( '../../router' );
var MainEvents = require( '../../events/main-events' );
Backbone.$ = $;

var SectionFooterView = Backbone.View.extend( {
  events: {
    'click .navigation-link': 'sendNavEvent'
  },

  initialize: function() {
    // if the browser doesn't support pushState, don't
    // trigger click events for links
    if ( Router.hasPushState === false || $( '#table-of-contents' ).hasClass( 'diff-toc' ) ) {
      this.events = {};
    }
  },

  sendNavEvent: function( e ) {
    e.preventDefault();
    var sectionId = $( e.currentTarget ).data( 'linked-section' );

    MainEvents.trigger( 'section:open', sectionId, {}, 'reg-section' );
  },

  remove: function() {
    this.stopListening();
    return this;
  }
} );

module.exports = SectionFooterView;
