'use strict';
var $ = require( 'jquery' );
var _ = require( 'underscore' );
var Backbone = require( 'backbone' );
var SubHead = require( './sub-head-view' );
Backbone.$ = $;

var HeaderView = Backbone.View.extend( {
  el: '.reg-header',

  initialize: function() {
    this.subHeadView = new SubHead();
  },

  events: {
    'click .mobile-nav-trigger': 'toggleNav'
  },

  toggleNav: function( e ) {
    e.preventDefault();
    $( '.app-nav-list, .mobile-nav-trigger' ).toggleClass( 'open' );
  },

  contextMap: {
    changeSubHeadText: '_updateSubHead'
  },

  ask: function( message, context ) {
    if ( typeof this.contextMap[message] !== 'undefined' ) {
      this.contextMap[message].apply( context );
    }
  },

  // type = wayfinding or search
  // content = new content
  _updateSubHead: function( context ) {
    this.subHeadView.change(
      context.type,
      context.content
    );
  }
} );

module.exports = HeaderView;
