'use strict';
var $ = require( 'jquery' );
var _ = require( 'underscore' );
var Backbone = require( 'backbone' );
var DrawerEvents = require( '../../events/drawer-events' );
var GAEvents = require( '../../events/ga-events' );
Backbone.$ = $;

var DrawerTabsView = Backbone.View.extend( {
  el: '.toc-head',

  events: {
    'click .toc-toggle': 'openDrawer',
    'click .toc-nav-link': 'updatePaneTabs'
  },

  idMap: {
    'table-of-contents': '#menu-link',
    'timeline': '#timeline-link',
    'search': '#search-link'
  },

  initialize: function() {
    this.externalEvents = DrawerEvents;

    this.listenTo( this.externalEvents, 'pane:change', this.changeActiveTab );
    this.listenTo( this.externalEvents, 'pane:init', this.setStartingTab );
    this.$activeEls = $( '#menu, #site-header, #content-body, #primary-footer, #content-header' );

    // view switcher buttons - TOC, calendar, search
    this.$tocLinks = $( '.toc-nav-link' );
    this.$toggleArrow = $( '#panel-link' );

    // default the drawer state to close
    this.drawerState = 'close';

    // For browser widths above 1100px apply the 'open' class
    //  and set drawer state to open
    if ( document.documentElement.clientWidth > 1100 ) {
      this.$toggleArrow.addClass( 'open' );
      this.drawerState = 'open';
    }

    this.$activeEls.addClass( this.drawerState );
  },

  setStartingTab: function( tab ) {
    $( this.idMap[tab] ).addClass( 'current' );
  },

  changeActiveTab: function( tab ) {
    this.$tocLinks.removeClass( 'current' );
    $( this.idMap[tab] ).addClass( 'current' );

    GAEvents.sendEvent( 'drawer:switchTab', tab );
  },

  // this.$activeEls are structural els that need to have
  // CSS applied to work with the drawer conditionally based
  // on its state
  updateDOMState: function() {
    if ( typeof this.$activeEls !== 'undefined' ) {
      this.$activeEls.toggleClass( this.drawerState );
    }
  },

  openDrawer: function( e ) {
    var context = { type: 'drawer' };

    if ( e ) {
      e.preventDefault();
    }

    this.toggleDrawerState();

    // only send click event if there was an actual click
    if ( e ) {
      if ( $( e.target ).hasClass( 'open' ) ) {
        GAEvents.sendEvent( 'drawer', 'drawer:open' );
      }
      else {
        GAEvents.sendEvent( 'drawer', 'drawer:close' );
      }
    }
  },

  // figure out whether drawer should open/close
  // tell surrounding elements to update accordingly
  // update the open/close arrow
  // set state
  toggleDrawerState: function() {
    var state = this.drawerState === 'open' ? 'close' : 'open';
    this.updateDOMState();
    this.$toggleArrow.toggleClass( 'open' );
    this.drawerState = state;
    this.updateDOMState();
  },

  // update active pane based on click or external input
  updatePaneTabs: function( e ) {
    e.preventDefault();

    var $target = $( e.target ),
        linkValue = _.last( $target.closest( 'a' ).attr( 'href' ).split( '#' ) );
    this.activePane = linkValue;

    if ( $( '.panel' ).css( 'left' ) === '-200px' ) {
      this.openDrawer();
    }

    this.externalEvents.trigger( 'pane:change', linkValue );
  }
} );

module.exports = DrawerTabsView;
