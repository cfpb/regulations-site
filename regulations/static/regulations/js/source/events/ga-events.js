'use strict';

var analyticsEvents = {

  tagManagerIsLoaded: false,

  init: function() {
    // detect if Google tag manager is loaded
    if ( window.hasOwnProperty( 'dataLayer' ) ) {
      analyticsEvents.tagManagerIsLoaded = true;
    }
  },

  sendEvent: function( action, label ) {
    if ( analyticsEvents.tagManagerIsLoaded ) {
      window.dataLayer.push( {
        event: 'eRegs Event',
        action: action,
        label: label
      } );
    }
  }

};

module.exports = analyticsEvents;
