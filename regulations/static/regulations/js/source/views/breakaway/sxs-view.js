'use strict';
var $ = require( 'jquery' );
var _ = require( 'underscore' );
var Backbone = require( 'backbone' );
var SxS = require( './sxs-view' );
var Router = require( '../../router' );
var SxSModel = require( '../../models/sxs-model' );
var BreakawayEvents = require( '../../events/breakaway-events' );
var MainEvents = require( '../../events/main-events' );
Backbone.$ = $;

var SxSView = Backbone.View.extend( {
  el: '#breakaway-view',

  events: {
    'click .sxs-back-button': 'remove',
    'click .footnote-jump-link': 'footnoteHighlight',
    'click .return-link': 'removeHighlight'
  },

  initialize: function() {
    var render;
    this.externalEvents = BreakawayEvents;

    // visibly open the SxS panel immediately
    this.$el.addClass( 'open-sxs' );

    // give it a state of `progress` until content loads
    this.changeState( 'inprogress' );

    // callback to be sent to model's get method
    // called after ajax resolves sucessfully
    render = function( success, returned ) {
      this.changeState( 'completed' );
      if ( success ) {
        this.render( returned );
      }
      else {
        this.render( '<div class="error"><span class="cf-icon cf-icon-error icon-warning"></span>Due to a network error, we were unable to retrieve the requested information.</div>' );
      }
    }.bind( this );

    SxSModel.get( this.options.url, render ),

    this.listenTo( this.externalEvents, 'sxs:close', this.remove );

    // if the browser doesn't support pushState, don't
    // trigger click events for links
    if ( Router.hasPushState === false ) {
      this.events = {};
    }
  },

  render: function( analysis ) {
    this.$el.html( analysis );
  },

  changeState: function( state ) {
    // if a previous state exists remove the class before updating
    this.$el.removeClass( this.loadingState );
    this.loadingState = state;
    this.$el.addClass( state );
  },

  footnoteHighlight: function( e ) {
    var target = $( e.target ).attr( 'href' );
    // remove existing highlight
    this.removeHighlight();
    // highlight the selected footnote
    $( '.footnotes ' + target ).toggleClass( 'highlight' );
  },

  removeHighlight: function() {
    $( '.footnotes li' ).removeClass( 'highlight' );
  },

  remove: function( e ) {
    if ( typeof e !== 'undefined' ) {
      e.preventDefault();
      window.history.back();
    }

    this.$el.removeClass( 'open-sxs' );
    this.$el.html( '' );
    this.stopListening();
    this.$el.off();
    return this;
  }
} );

module.exports = SxSView;
