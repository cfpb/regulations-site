'use strict';
var $ = require( 'jquery' );
var _ = require( 'underscore' );
var Backbone = require( 'backbone' );
var SxSList = require( './sxs-list-view' );
var SidebarListView = require( './sidebar-list-view' );
var Router = require( '../../router' );
var BreakawayEvents = require( '../../events/breakaway-events' );
var GAEvents = require( '../../events/ga-events' );
var Helpers = require( '../../helpers.js' );

Backbone.$ = $;

var SxSListView = SidebarListView.extend( {
  el: '#sxs-list',

  events: {
    'click .sxs-link': 'openSxS'
  },

  initialize: function() {
    this.render = _.bind( this.render, this );
    this.modifyListDisplay();

    // if the browser doesn't support pushState, don't
    // trigger click events for links
    if ( Router.hasPushState === false ) {
      this.events = {};
    }
  },

  openSxS: function( e ) {
    e.preventDefault();

    var $sxsLink = $( e.target ),
        id = $sxsLink.data( 'sxs-paragraph-id' ),
        docNumber = $sxsLink.data( 'doc-number' ),
        version = $( 'section[data-base-version]' ).data( 'base-version' );

    BreakawayEvents.trigger( 'sxs:open', {
      regParagraph: id,
      docNumber: docNumber,
      fromVersion: version
    } );

    GAEvents.sendEvent( 'sxs:open', id );
  },

  render: function( html ) {
    var $html = $( html ),
        list = $html.find( '#sxs-list' ).html();
    this.$el.html( list );

    this.modifyListDisplay();
  },

  modifyListDisplay: function() {
    var $folderContent = this.$el.find( '.expand-drawer' );
    if ( $folderContent.children().length > 1 ) {
      this.highlightHeader();
      // toggle the SxS slider open if there is content
      this.toggleSxS();
    }
  },

  highlightHeader: function() {
    this.$el.find( 'header' ).addClass( 'has-content' );
  },

  toggleSxS: function() {
    Helpers.toggleExpandable( $( '#sxs-expandable-header' ), 0 );
  }

} );

module.exports = SxSListView;
