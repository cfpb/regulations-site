'use strict';
var $ = require( 'jquery' );
var _ = require( 'underscore' );
var Backbone = require( 'backbone' );
var RegsHelpers = require( '../../helpers' );
var HeaderEvents = require( '../../events/header-events' );
Backbone.$ = $;

var SubHeadView = Backbone.View.extend( {
  el: '#content-header',

  initialize: function() {
    this.externalEvents = HeaderEvents;

    this.listenTo( this.externalEvents, 'section:open', this.changeTitle );
    this.listenTo( this.externalEvents, 'section:rendered', this.addWayfindID );
    this.listenTo( this.externalEvents, 'search-results:open', this.displayCount );
    this.listenTo( this.externalEvents, 'search-results:open', this.changeDate );
    this.listenTo( this.externalEvents, 'search-results:open', this.removeSubpart );
    this.listenTo( this.externalEvents, 'clear', this.reset );
    this.listenTo( this.externalEvents, 'subpart:present', this.renderSubpart );
    this.listenTo( this.externalEvents, 'subpart:absent', this.removeSubpart );

    // cache inner title DOM node for frequent reference
    this.$activeTitle = this.$el.find( '.header-label' );

    // same for subpart label
    this.$subpartLabel = this.$el.find( '.subpart' );

    // same for wayfinding container
    this.$wayfinding = this.$el.find( '.wayfinding' );
  },

  // populates subhead with new title
  changeTitle: function( id ) {
    this.paraTitle = RegsHelpers.idToRef( id ).split( '(' );
    this.paraSectionTitle = this.paraTitle.shift();
    // if the user scrolls add the paragraphs with a span class
    if ( this.paraTitle.length > 0 ) {
      this.$activeTitle.html(
        this.paraSectionTitle +
                '<span class="wayfinding-paragraph">(' +
                this.paraTitle.join( '(' ) +
                '</span>'
      );
      return;
    }
    // add the section title on page load
    this.$activeTitle.html( this.paraSectionTitle );
  },

  // we add a class to the wayfinding container so that we can choose to hide
  // pieces of the content by section when needed
  addWayfindID: function( id ) {
    this.$wayfinding.attr( 'id', 'wayfind-' + id );
  },

  displayCount: function( resultCount ) {
    this.$activeTitle.html( '<span class="subpart">Search results</span> ' + resultCount );
  },

  changeDate: function() {
    this.version = $( 'section[data-base-version]' ).data( 'base-version' );
    this.displayDate = $( 'select[name=version] option[value=' + this.version + ']' ).text();
    $( '.effective-date' ).html( '<strong>Effective date:</strong> ' + this.displayDate );
  },

  renderSubpart: function( label ) {
    this.$subpartLabel.text( label ).show();
    this.$activeTitle.addClass( 'with-subpart' );
  },

  removeSubpart: function() {
    this.$subpartLabel.text( '' ).hide();
    this.$activeTitle.removeClass( 'with-subpart' );
  },

  reset: function() {
    this.$activeTitle.html( '' );
  }
} );

module.exports = SubHeadView;
