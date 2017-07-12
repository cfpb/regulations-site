// Launches app
'use strict';
// make jQuery globally accessible for plugins and analytics
global.$ = global.jQuery = require( 'jquery' );
var app = require( './app-init' );

// A `bind()` polyfill
if ( !Function.prototype.bind ) {
  Function.prototype.bind = function( oThis ) {
    if ( typeof this !== 'function' ) {
      // closest thing possible to the ECMAScript 5 internal IsCallable function
      throw new TypeError( 'Function.prototype.bind - what is trying to be bound is not callable' );
    }

    var aArgs = Array.prototype.slice.call( arguments, 1 ),
        fToBind = this,
        FNOP = function() {},
        fBound = function() {
          return fToBind.apply( this instanceof FNOP && oThis ? this : oThis, aArgs.concat( Array.prototype.slice.call( arguments ) ) );
        };

    FNOP.prototype = this.prototype;
    fBound.prototype = new FNOP();

    return fBound;
  };
}

// a 'window.location.origin' polyfill for IE10
// http://tosbourn.com/2013/08/javascript/a-fix-for-window-location-origin-in-internet-explorer/
if ( !window.location.origin ) {
  window.location.origin = window.location.protocol + '//' + window.location.hostname + ( window.location.port ? ':' + window.location.port : '' );
}

$( document ).ready( function() {
  app.init();
} );

// tests for some accessibility misses
// use in browser console with AccessibilityTest()
window.AccessibilityTest = function() {
  // I think this will keep IE from crying?
  var console = console || { error: function() {} };

  /* eslint-disable */
    $('img').each(function() {
        if (typeof this.attributes.alt === 'undefined') {
            console.error('Image does not have alt text', this);
        }
    });

    $('p, h1, h2, h3, h4, h5, h6, div, span').each(function() {
        if ($(this).css('font-size').indexOf('em') === -1 && $(this).css('font-size').indexOf('px') > 0) {
            console.error('Font size is set in px, not ems', this);
        }
    });
    /* eslint-enable */
};
