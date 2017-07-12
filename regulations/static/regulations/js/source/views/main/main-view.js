'use strict';
var $ = require( 'jquery' );
var _ = require( 'underscore' );
var Backbone = require( 'backbone' );
var SearchResultsView = require( './search-results-view' );
var RegView = require( './reg-view' );
var RegModel = require( '../../models/reg-model' );
var SearchModel = require( '../../models/search-model' );
var SubHeadView = require( '../header/sub-head-view' );
var SectionFooter = require( './section-footer-view' );
var MainEvents = require( '../../events/main-events' );
var SidebarEvents = require( '../../events/sidebar-events' );
var DiffModel = require( '../../models/diff-model' );
var DiffView = require( './diff-view' );
var Router = require( '../../router' );
var HeaderEvents = require( '../../events/header-events' );
var DrawerEvents = require( '../../events/drawer-events' );
var Helpers = require( '../../helpers' );
var MainEvents = require( '../../events/main-events' );
var ChildView = require( './child-view' );
var Resources = require( '../../resources.js' );
Backbone.$ = $;

var MainView = Backbone.View.extend( {
  el: '#content-body',

  initialize: function() {
    this.render = _.bind( this.render, this );
    this.externalEvents = MainEvents;

    if ( Router.hasPushState ) {
      this.externalEvents.on( 'search-results:open', this.createView, this );
      this.externalEvents.on( 'section:open', this.createView, this );
      this.externalEvents.on( 'diff:open', this.createView, this );
      this.externalEvents.on( 'breakaway:open', this.breakawayOpen, this );
      this.externalEvents.on( 'section:error', this.displayError, this );
    }

    var childViewOptions = {},
        appendixOrSupplement;
    this.$topSection = this.$el.find( 'section[data-page-type]' );

    // which page are we starting on?
    this.contentType = this.$topSection.data( 'page-type' );
    // what version of the reg?
    this.regVersion = Helpers.findVersion( Resources.versionElements );
    // what section do we have open?
    this.sectionId = this.$topSection.attr( 'id' );
    if ( typeof this.sectionId === 'undefined' ) {
      //  Find the first child which *does* have a label
      this.sectionId = this.$topSection.find( 'section[id]' ).attr( 'id' );
    }
    this.regPart = $( '#menu' ).data( 'reg-id' );
    this.cfrTitle = $( '#menu' ).data( 'cfr-title-number' );

    // build options object to pass into child view constructor
    childViewOptions.id = this.sectionId;
    childViewOptions.regVersion = this.regVersion;
    childViewOptions.cfrTitle = this.cfrTitle;

    appendixOrSupplement = this.isAppendixOrSupplement();
    if ( appendixOrSupplement ) {
      // so that we will know what the doc title format should be
      childViewOptions.subContentType = appendixOrSupplement;
    }

    // find search query
    if ( this.contentType === 'search-results' ) {
      childViewOptions.id = Helpers.parseURL( window.location.href );
      childViewOptions.params = childViewOptions.id.params;
      childViewOptions.query = childViewOptions.id.params.q;
    }

    if ( this.contentType === 'landing-page' ) {
      DrawerEvents.trigger( 'pane:change', 'table-of-contents' );
    }

    // we don't want to ajax in data that the page loaded with
    childViewOptions.render = false;

    if ( this.sectionId ) {
      // store the contents of our $el in the model so that we
      // can re-render it later
      this.modelmap[this.contentType].set( this.sectionId, this.$el.html() );
      childViewOptions.model = this.modelmap[this.contentType];
    }

    if ( this.contentType && typeof this.viewmap[this.contentType] !== 'undefined' ) {
      // create new child view
      this.childView = new this.viewmap[this.contentType]( childViewOptions );
    }

    this.sectionFooter = new SectionFooter( { el: this.$el.find( '.section-nav' ) } );
  },

  modelmap: {
    'reg-section': RegModel,
    'search-results': SearchModel,
    'diff': DiffModel,
    'appendix': RegModel,
    'interpretation': RegModel
  },

  viewmap: {
    'reg-section': RegView,
    'search-results': SearchResultsView,
    'diff': DiffView,
    'appendix': RegView,
    'interpretation': RegView
  },

  createView: function( id, options, type ) {
    // close breakaway if open
    if ( typeof this.breakawayCallback !== 'undefined' ) {
      this.breakawayCallback();
      delete this.breakawayCallback;
    }

    this.contentType = type;

    // id is null on search results as there is no section id
    if ( id !== null ) {
      this.sectionId = id;
    }

    // this is a triage measure. I don't know how this could
    // ever be null, but apparently somewhere along the line it is
    if ( this.regVersion === null ) {
      this.regVersion = this.$el.find( 'section[data-page-type]' ).data( 'base-section' );
    }

    if ( typeof options.render === 'undefined' ) {
      // tell the child view it should render
      options.render = true;
    }

    options.id = id;
    options.type = this.contentType;
    options.regVersion = this.regVersion;
    options.regPart = this.regPart;
    options.model = this.modelmap[this.contentType];
    options.cb = this.render;
    options.cfrTitle = this.cfrTitle;

    // diffs need some more version context
    if ( this.contentType === 'diff' ) {
      options.baseVersion = this.regVersion || Helpers.findVersion( Resources.versionElements );
      options.newerVersion = Helpers.findDiffVersion( Resources.versionElements );
      if ( typeof options.fromVersion === 'undefined' ) {
        options.fromVersion = $( '#table-of-contents' ).data( 'from-version' );
      }
    }

    // search needs to know which version to search and switch to that version
    if ( this.contentType === 'search-results' && typeof options.searchVersion !== 'undefined' ) {
      options.regVersion = options.searchVersion;
    }

    this.loading();
    SidebarEvents.trigger( 'section:loading' );

    if ( typeof this.childView !== 'undefined' ) {
      this.childView.remove();
      delete this.childView;
    }

    this.childView = new this.viewmap[this.contentType]( options );
  },

  isAppendixOrSupplement: function() {
    if ( Helpers.isAppendix( this.sectionId ) ) {
      return 'appendix';
    }
    else if ( Helpers.isSupplement( this.sectionId ) ) {
      return 'supplement';
    }
    return false;
  },

  breakawayOpen: function( cb ) {
    this.breakawayCallback = cb;
    this.loading();
  },

  displayError: function() {
    // get ID of still rendered last section
    var oldId = this.$el.find( 'section[data-page-type]' ).attr( 'id' ),
        $error = this.$el.prepend( '<div class="error"><span class="cf-icon cf-icon-error icon-warning"></span>Due to a network error, we were unable to retrieve the requested information.</div>' );

    DrawerEvents.trigger( 'section:open', oldId );
    HeaderEvents.trigger( 'section:open', oldId );

    this.loaded();
    SidebarEvents.trigger( 'section:error' );

    window.scrollTo( $error.offset().top, 0 );

  },

  render: function( html, options ) {
    var offsetTop, $scrollToId;

    if ( typeof this.childView !== 'undefined' ) {
      this.sectionFooter.remove();
    }

    this.$el.html( html );

    MainEvents.trigger( 'section:rendered' );

    SidebarEvents.trigger( 'update', {
      type: this.contentType,
      id: this.sectionId
    } );

    if ( options && typeof options.scrollToId !== 'undefined' ) {
      $scrollToId = $( '#' + options.scrollToId );
      if ( $scrollToId.length > 0 ) {
        offsetTop = $scrollToId.offset().top;
      }
    }

    window.scrollTo( 0, offsetTop || 0 );

    this.loaded();
  },

  loading: function() {
    // visually indicate that a new section is loading
    $( '.main-content' ).addClass( 'loading' );

  },

  loaded: function() {
    $( '.main-content' ).removeClass( 'loading' );

    // change focus to main content area when new sections are loaded
    $( '.section-focus' ).focus();
  }
} );
module.exports = MainView;
