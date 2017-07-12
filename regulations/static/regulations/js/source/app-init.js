// Module called on app load, once doc.ready
'use strict';

var $ = require( 'jquery' );
var _ = require( 'underscore' );
var Backbone = require( 'backbone' );
var MainView = require( './views/main/main-view' );
var Router = require( './router' );
var SidebarView = require( './views/sidebar/sidebar-view' );
var HeaderView = require( './views/header/header-view' );
var DrawerView = require( './views/drawer/drawer-view' );
var analyticsEvents = require( './events/ga-events' );
Backbone.$ = $;

module.exports = {
  // Purgatory for DOM event bindings that should happen in a View
  bindEvents: function() {
    // disable/hide an alert
    $( '.disable-link' ).on( 'click', function( e ) {
      e.preventDefault();
      $( this ).closest( '.displayed' ).addClass( 'disabled' );
    } );
  },

  init: function() {
    Router.start();
    this.bindEvents();
    analyticsEvents.init();
    var main = new MainView(),
        sidebar = new SidebarView(),
        header = new HeaderView(), // Header before Drawer as Drawer sends Header events
        drawer = new DrawerView();
    setTimeout( function() {
      $( 'html' ).addClass( 'selenium-start' );
    }, 5000 );
  }
};
