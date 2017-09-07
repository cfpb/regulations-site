'use strict';
var $ = require( 'jquery' );
var _ = require( 'underscore' );
var Backbone = require( 'backbone' );
require( '../../events/scroll-stop.js' );
var Router = require( '../../router' );
var HeaderEvents = require( '../../events/header-events' );
var DrawerEvents = require( '../../events/drawer-events' );
var Helpers = require( '../../helpers' );
var MainEvents = require( '../../events/main-events' );
Backbone.$ = $;

var ChildView = Backbone.View.extend( {
  initialize: function() {
    var cb;

    this.model = this.options.model;
    this.externalEvents = MainEvents;
    this.listenTo( this.externalEvents, 'section:rendered', this.setElement );

    // callback to be sent to model's get method
    // called after ajax resolves sucessfully
    cb = function( success, returned ) {
      if ( success ) {
        if ( typeof this.options.cb !== 'undefined' ) {
          this.options.cb( returned, this.options );
        }

        if ( typeof this.title === 'undefined' ) {
          this.title = this.assembleTitle();
        }

        this.route( this.options );
        this.attachWayfinding();
        this.render();
      }
      else {
        this.externalEvents.trigger( 'section:error' );
      }
    }.bind( this );

    // if the site wasn't loaded on this content
    if ( this.options.render ) {
      this.model.get( this.options.id, cb );
    }
    else if ( this.options.id ) {
      // hard code the id update for users who directly load a section
      $( '.wayfinding' ).attr( 'id', 'wayfind-' + this.id );
      // attach wayfinding and trigger the section:open drawer event
      this.attachWayfinding();
      DrawerEvents.trigger( 'section:open', this.id );
    }

    this.$sections = this.$sections || {};
    this.activeSection = this.id;
    this.$activeSection = $( '#' + this.activeSection );

    return this;
  },

  setElement: function() {
    if ( this.id ) {
      Backbone.View.prototype.setElement.call( this, '#' + this.id );
    }
  },

  attachWayfinding: function() {
    this.updateWayfinding();
    // * when a scroll event completes, check what the active secion is
    // we can't scope the scroll to this.$el because there's no localized
    // way to grab the scroll event, even with overflow:scroll
    $( window ).on( 'scrollstop', _.bind( this.checkActiveSection, this ) );
  },

  render: function() {
    this.updateWayfinding();
    HeaderEvents.trigger( 'section:rendered', this.id );
    DrawerEvents.trigger( 'section:open', this.id );
  },

  changeFocus: function( id ) {
    $( id ).focus();
  },

  assembleTitle: function() {
    var titleParts, newTitle;
    titleParts = _.compact( document.title.split( ' ' ) );
    newTitle = [ titleParts[0], titleParts[1], Helpers.idToRef( this.id ), '|', 'eRegulations' ];
    return newTitle.join( ' ' );
  },

  // naive way to update the active table of contents link and wayfinding header
  // once a scroll event ends, we loop through each content section DOM node
  // the first one whose offset is greater than the window scroll position, accounting
  // for the fixed position header, is deemed the active section
  checkActiveSection: function() {
    var len = this.$contentContainer.length - 1;

    for ( var i = 0; i <= len; i++ ) {
      if ( this.$sections[i].offset().top + this.$contentHeader.height() >= $( window ).scrollTop() ) {
        if ( _.isEmpty( this.activeSection ) || this.activeSection !== this.$sections[i].id ) {
          this.activeSection = this.$sections[i][0].id;
          this.$activeSection = $( this.$sections[i][0] );
          // **Event** trigger active section change
          HeaderEvents.trigger( 'section:open', this.activeSection );
          this.externalEvents.trigger( 'paragraph:active', this.activeSection );

          if ( typeof window.history !== 'undefined' && typeof window.history.replaceState !== 'undefined' ) {
            // update hash in url
            window.history.replaceState(
              null,
              null,
              window.location.origin + window.location.pathname + window.location.search + '#' + this.activeSection
            );
          }

          return;
        }
      }
    }


    return this;
  },

  updateWayfinding: function() {
    var i, len;

    // cache all sections in the DOM eligible to be the active section
    // also cache some jQobjs that we will refer to frequently
    this.$contentHeader = this.$contentHeader || $( 'header.reg-header' );

    // sections that are eligible for being the active section
    this.$contentContainer = $( '#' + this.id ).find( '.level-1 li[id], .reg-section, .appendix-section, .supplement-section' );

    // cache jQobjs of each reg section
    len = this.$contentContainer.length;

    // short term solution: sometimes, back buttoning on diffs, this.$sections undefined. why?
    this.$sections = this.$sections || {};

    for ( i = 0; i < len; i++ ) {
      this.$sections[i] = $( this.$contentContainer[i] );
    }
  },

  route: function( options ) {
    if ( Router.hasPushState && typeof options.noRoute === 'undefined' ) {
      var url = this.url,
          hashPosition;

      // if a hash has been passed in
      if ( options && typeof options.scrollToId !== 'undefined' ) {
        url += '#' + options.scrollToId;
        this.navigate( url );
        $( 'html, body' ).scrollTop( $( '#' + options.scrollToId ).offset().top );
      } else {
        if ( typeof Backbone.history.fragment === 'undefined' ) {
          hashPosition = -1;
        } else {
          hashPosition = Backbone.history.fragment.indexOf( '#' );
        }

        if ( hashPosition !== -1 ) {
          url = url.slice( 0, hashPosition ) + '#' + options.id;
        } else if ( options.type !== 'diff' ) {
          url += '#' + options.id;
        }

        // explicit url pattern for reg-sections
        // it may be worth doing this for each url pattern
        if ( options.type === 'reg-section' ) {
          url = options.id + '/' + options.regVersion + '#' + options.id;
        }

        this.navigate( url );
      }
    }
  },

  navigate: function( url ) {
    Router.navigate( url );
    document.title = this.title;
  },

  remove: function() {
    $( window ).off( 'scrollstop' );
    this.stopListening();
    this.off();
    return this;
  }
} );

module.exports = ChildView;
