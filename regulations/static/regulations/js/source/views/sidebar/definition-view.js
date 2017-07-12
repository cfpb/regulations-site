'use strict';
var $ = require( 'jquery' );
var _ = require( 'underscore' );
var Backbone = require( 'backbone' );
var SidebarModuleView = require( './sidebar-module-view' );
var RegModel = '../../models/reg-model.js';
var Helpers = require( '../../helpers' );
var Router = require( '../../router' );
var MainEvents = require( '../../events/main-events' );
var SidebarEvents = require( '../../events/sidebar-events' );
var GAEvents = require( '../../events/ga-events' );
Backbone.$ = $;

// **Constructor**
// this.options:
//
// * **id** string, dash-delimited id of definition paragraph
// * **$anchor** jQobj, the reg-view link that opened the def
//
// this.options turns into this.model
var DefinitionView = SidebarModuleView.extend( {
  el: '#definition',

  events: {
    'click .close-button': 'close',
    'click .update-definition': 'updateDefinition'
  },

  initialize: function() {
    this.externalEvents = SidebarEvents;
    this.listenTo( this.externalEvents, 'definition:outOfScope', this.displayScopeMsg );
    this.listenTo( this.externalEvents, 'definition:inScope', this.removeScopeMsg );
    this.listenTo( this.externalEvents, 'definition:activate', this.unGrayDefinition );
    this.listenTo( this.externalEvents, 'definition:deactivate', this.grayOutDefinition );

    if ( typeof this.options.id !== 'undefined' ) {
      this.id = this.options.id;
    }

    if ( typeof this.options.term !== 'undefined' ) {
      this.term = this.options.term;
      this.$el.data( 'defined-term', this.term );
    }

    // insert the spinner header to be replaced
    // by the full def once it loads
    this.renderHeader();

    // if pushState is supported, attach the
    // appropriate event handlers
    if ( Router.hasPushState ) {
      this.events['click .continue-link.interp'] = 'openInterpretation';
      this.events['click .continue-link.full-def'] = 'openFullDefinition';
      this.events['click .definition'] = 'openFullDefinition';
      this.delegateEvents( this.events );
    }
  },

  // temporary header w/spinner while definition is loading
  renderHeader: function() {
    this.$el.html( '<div class="sidebar-header group spinner"><h4>Defined Term</h4></div>' );
  },

  render: function( html ) {
    this.$el.html( html );
  },

  renderError: function( error ) {
    this.$el.html( '' );
    this.renderHeader();
    this.$el.children().removeClass( 'spinner' );
    this.$el.append( '<div class="error"><span class="cf-icon cf-icon-error icon-warning"></span>' + error + '</div>' );
  },

  close: function( e ) {
    e.preventDefault();
    // return focus to the definition link once the definition is removed
    $( '.definition.active' ).focus();

    MainEvents.trigger( 'definition:close' );
    this.remove();

    GAEvents.sendEvent( 'definition:close', this.term );
  },

  updateDefinition: function( e ) {
    e.preventDefault( e );

    this.externalEvents.trigger( 'definition:open', {
      id: $( e.target ).data( 'definition' ),
      term: this.term,
      cb: function() {
        // update list of out of scope paragraphs for new definition
        MainEvents.trigger( 'definition:carriedOver' );
      }
    } );
  },

  // displayed when an open definition doesn't apply to the
  // whole open section
  displayScopeMsg: function( id ) {
    var msg = '<p>This term has a different definition for some portions of ';
    msg += id ? Helpers.idToRef( id ) + '.' : 'this section.';
    msg += '</p>';

    this.$warningContainer = this.$warningContainer || this.$el.find( '.definition-warning' );

    this.$warningContainer.removeClass( 'hidden' )
      .find( '.msg' ).html( msg );
  },

  // when a definition is fully applicable to the section
  removeScopeMsg: function() {
    if ( typeof this.$warningContainer !== 'undefined' && this.$warningContainer.length > 0 ) {
      this.$warningContainer.addClass( 'hidden' ).find( '.msg' ).html( '' );
    }

    this.unGrayDefinition();
  },

  // for when the definition does not apply to the active section
  grayOutDefinition: function( defId, href, activeSectionId ) {
    var $text = this.$el.find( '.definition-text' ),
        linkText = 'Load the correct definition for ',
        link,
        $msg;

    if ( typeof this.$warningContainer === 'undefined' ) {
      this.displayScopeMsg( Helpers.findBaseSection( activeSectionId ) );
    }

    $msg = this.$warningContainer.find( '.msg' );
    linkText += defId ? Helpers.idToRef( activeSectionId ) : 'this section';
    link = '<a href="' + href + '" class="update-definition inactive internal" data-definition="' + defId + '">';
    link += linkText + '</a>';

    // remove duplicates
    $msg.find( 'a' ).remove();

    // insert link to load applicable definition
    $msg.append( link );

    // gray out definition text
    $text.addClass( 'inactive' );
  },

  // for when a definition is not in conflict for the active section,
  // but doesn't apply to the entire section, either
  unGrayDefinition: function() {
    var $text = this.$el.find( '.definition-text' );
    $text.removeClass( 'inactive' );

    this.$el.find( '.definition-warning a' ).remove();
  },

  openFullDefinition: function( e ) {
    e.preventDefault();
    var id = $( e.target ).data( 'linked-section' ) || $( e.target ).data( 'definition' ),
        parentId = Helpers.findBaseSection( id );

    MainEvents.trigger( 'section:open', parentId, {
      scrollToId: id
    }, 'reg-section' );

    GAEvents.sendEvent( 'definition:followCitation', id );
  },

  openInterpretation: function( e ) {
    e.preventDefault();
    var $e = $( e.target ),
        id = $e.data( 'linked-section' ),
        pid = $e.data( 'linked-subsection' );

    MainEvents.trigger( 'section:open', id, {
      scrollToId: pid
    }, 'interpretation' );

    GAEvents.sendEvent( 'definition:followCitation', id );
  },

  remove: function() {
    this.stopListening();
    this.off();
    this.$el.html( '' );
    this.$el.unbind();

    return this;
  }
} );

module.exports = DefinitionView;
