'use strict';
var $ = require( 'jquery' );
var _ = require( 'underscore' );
var Backbone = require( 'backbone' );
var RegModel = require( '../../models/reg-model' );
var SxSList = require( './sxs-list-view' );
var HelpView = require( './help-view' );
var AlertView = require( './alert-view' );
var SidebarModel = require( '../../models/sidebar-model' );
var DefinitionModel = require( '../../models/definition-model' );
var Breakaway = require( '../breakaway/breakaway-view' );
var SidebarEvents = require( '../../events/sidebar-events' );
var Definition = require( './definition-view' );
var MetaModel = require( '../../models/meta-model' );
var MainEvents = require( '../../events/main-events' );
var Helpers = require( '../../helpers.js' );
var GAEvents = require( '../../events/ga-events' );

Backbone.$ = $;

var SidebarView = Backbone.View.extend( {
  el: '#sidebar-content',

  events: {
    'click .expandable': 'toggleExpandable'
  },

  initialize: function() {
    this.openRegFolders = _.bind( this.openRegFolders, this );
    this.externalEvents = SidebarEvents;
    this.listenTo( this.externalEvents, 'update', this.updateChildViews );
    this.listenTo( this.externalEvents, 'definition:open', this.openDefinition );
    this.listenTo( this.externalEvents, 'definition:close', this.closeDefinition );
    this.listenTo( this.externalEvents, 'section:loading', this.loading );
    this.listenTo( this.externalEvents, 'section:error', this.loaded );
    this.listenTo( this.externalEvents, 'breakaway:open', this.hideChildren );

    this.childViews = {};
    this.openRegFolders();

    this.model = SidebarModel;
    this.definitionModel = DefinitionModel;
  },

  openDefinition: function( config ) {
    var createDefView = function( cb, success, res ) {
      var errorMsg;

      if ( success ) {
        this.childViews.definition.render( res );
      }
      else {
        errorMsg = 'We tried to load that definition, but something went wrong. ';
        errorMsg += '<a href="#" class="update-definition inactive internal" data-definition="' + this.childViews.definition.id + '">Try again?</a>';

        this.childViews.definition.renderError( errorMsg );
      }
    }.bind( this );

    this.childViews.definition = new Definition( {
      id: config.id,
      term: config.term
    } );

    config.cb = config.cb || null;

    this.definitionModel.get( config.id, _.partial( createDefView, config.cb ) );
  },

  closeDefinition: function() {
    if ( typeof this.childViews.definition !== 'undefined' ) {
      this.childViews.definition.remove();
    }
  },

  updateChildViews: function( context ) {
    var $definition = $definition || this.$el.find( '#definition' );
    switch ( context.type ) {
      case 'reg-section':
        this.model.get( context.id, this.openRegFolders );
        MainEvents.trigger( 'definition:carriedOver' );

        // definition container is hidden when SxS opens
        if ( $definition.is( ':hidden' ) ) {
          $definition.show();
        }

        break;
      case 'search':
        this.closeChildren();
        this.loaded();
        break;
      case 'diff':
        this.loaded();
        break;
      default:
        this.closeChildren();
        this.loaded();
    }

    this.removeLandingSidebar();
  },

  openRegFolders: function( success, html ) {
    // close all except definition
    this.closeChildren( 'definition' );

    if ( arguments.length > 1 ) {
      // if we've already downloaded the sidebar
      this.insertChild( html );
    }
    else {
      this.createPlaceholders();
    }

    // new views to bind to new html
    this.childViews.sxs = new SxSList();
    this.childViews.help = new HelpView();
    this.childViews.alert = new AlertView();

    this.loaded();
  },

  removeLandingSidebar: function() {
    $( '.landing-sidebar' ).hide();
  },

  createPlaceholders: function() {
    if ( this.$el.find( '#update-alert' ).length === 0 ) {
      this.$el.append( '<section id="update-alert" class="regs-meta"></section>' );
    }

    if ( this.$el.find( '#sxs-list' ).length === 0 ) {
      this.$el.append( '<section id="sxs-list" class="regs-meta"></section>' );
    }

    if ( this.$el.find( '#help' ).length === 0 ) {
      this.$el.append( '<section id="help" class="regs-meta"></section>' );
    }
  },

  // open whatever content should populate the sidebar
  insertChild: function( el ) {
    this.$el.append( el );
  },

  removeChild: function( el ) {
    $( el ).remove();
  },

  insertDefinition: function( el ) {
    this.closeExpandables();

    if ( this.$el.definition.length === 0 ) {
      // if the page was loaded on the landing, search or 404 page,
      // it won't have the content sidebar template
      this.$el.prepend( '<section id="definition"></section>' );
      this.$el.definition = this.$el.find( '#definition' );
    }

    this.$el.definition.html( el );
  },

  closeExpandables: function() {
    this.$el.find( '.expandable' ).each( function( i, folder ) {
      var $folder = $( folder );
      if ( $folder.hasClass( 'open' ) ) {
        this.toggleExpandable( $folder );
      }
    }.bind( this ) );
  },

  toggleExpandable: function( e ) {
    var $expandable;

    if ( typeof e.stopPropagation !== 'undefined' ) {
      e.stopPropagation();
      $expandable = $( e.currentTarget );
    }
    else {
      $expandable = e;
    }

    Helpers.toggleExpandable( $expandable, 400 );

    if ( $expandable.hasClass( 'open' ) ) {
      GAEvents.sendEvent( 'sidebarexpanable:open', $expandable.data( 'expandable' ) );
    } else {
      GAEvents.sendEvent( 'sidebarexpanable:close', $expandable.data( 'expandable' ) );
    }

  },

  closeChildren: function( except ) {
    var k;
    for ( k in this.childViews ) {
      if ( this.childViews.hasOwnProperty( k ) ) {
        if ( !except || except !== k ) {
          this.childViews[k].remove();
        }
      }
    }
  },

  loading: function() {
    this.$el.addClass( 'loading' );
  },

  loaded: function() {
    this.$el.removeClass( 'loading' );
  },

  // when breakaway view loads
  hideChildren: function() {
    this.loading();
  }
} );

module.exports = SidebarView;
