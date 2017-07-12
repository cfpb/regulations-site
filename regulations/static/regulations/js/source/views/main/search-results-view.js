'use strict';
var $ = require( 'jquery' );
var _ = require( 'underscore' );
var Backbone = require( 'backbone' );
var SearchModel = require( '../../models/search-model.js' );
var Router = require( '../../router' );
var HeaderEvents = require( '../../events/header-events' );
var MainEvents = require( '../../events/main-events' );
var DrawerEvents = require( '../../events/drawer-events' );
var ChildView = require( './child-view' );
Backbone.$ = $;

var SearchResultsView = ChildView.extend( {
  events: {
    'click .search-nav a': 'paginate',
    'click h3 .internal': 'openResult'
  },

  initialize: function() {
    this.query = this.options.query;
    // the TOC may link to a different reg version than this.options.resultsRegVersion
    // because the user can select a different version to pull search results from
    this.resultsRegVersion = this.options.regVersion;
    this.page = parseInt( this.options.page, 10 ) || 0;
    this.title = 'Search of ' + this.options.regPart + ' for ' + this.query + ' | eRegulations';

    // if the browser doesn't support pushState, don't
    // trigger click events for links
    if ( Router.hasPushState === false ) {
      this.events = {};
    }

    DrawerEvents.trigger( 'pane:change', 'search' );

    // if the site wasn't loaded on the search results page
    if ( this.options.render ) {
      this.options.id = this.assembleSearchURL( this.options );
      this.url = 'search/' + this.options.id;

      ChildView.prototype.initialize.apply( this, arguments );
    }

  },

  setElement: function() {
    Backbone.View.prototype.setElement.call( this, '#content-wrapper.search-results' );
  },

  assembleSearchURL: function( options ) {
    var url = options.regPart;
    url += '?q=' + options.query;
    url += '&version=' + options.regVersion;

    if ( typeof options.page !== 'undefined' ) {
      url += '&page=' + options.page;
    }

    return url;
  },

  render: function() {
    var $results = this.$el.find( '#result-count' );

    // if the results were ajaxed in, update header
    if ( $results.text().length > 0 ) {
      HeaderEvents.trigger( 'search-results:open', $results.text() );
      $results.remove();
    }

    if ( Router.hasPushState ) {
      if ( typeof this.options.id !== 'undefined' ) {
        Router.navigate( 'search/' + this.options.id );
      }
    }
  },

  paginate: function( e ) {
    e.preventDefault();

    var page = $( e.target ).hasClass( 'previous' ) ? this.page - 1 : this.page + 1,
        config = {
          query: this.query,
          regVersion: this.resultsRegVersion,
          page: page
        };

    MainEvents.trigger( 'search-results:open', null, config, 'search-results' );
  },

  openResult: function( e ) {
    // TOC version retains the version the reg was loaded on whereas the content base section
    // changes to match the search results
    // page should reload if the TOC version doesn't match the searched version
    if ( this.resultsRegVersion === $( 'nav#toc' ).attr( 'data-toc-version' ) ) {
      e.preventDefault();
      var $resultLink = $( e.target ),
          config = {};

      config.regVersion = $resultLink.data( 'linked-version' );
      config.scrollToId = $resultLink.data( 'linked-subsection' );
      MainEvents.trigger( 'section:open', $resultLink.data( 'linked-section' ), config, 'reg-section' );
    }
  }
} );

module.exports = SearchResultsView;
