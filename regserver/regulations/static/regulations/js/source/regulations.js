// Launches app via RequireJS load
require(['jquery', 'app-init'], function($, app) {
    'use strict';
    // A `bind()` polyfill
    if (!Function.prototype.bind) {
        Function.prototype.bind = function (oThis) {
            if (typeof this !== 'function') {
                // closest thing possible to the ECMAScript 5 internal IsCallable function
                throw new TypeError('Function.prototype.bind - what is trying to be bound is not callable');
            }

          var aArgs = Array.prototype.slice.call(arguments, 1),
              fToBind = this,
              FNOP = function () {},
              fBound = function () {
                return fToBind.apply(this instanceof FNOP && oThis ? this : oThis, aArgs.concat(Array.prototype.slice.call(arguments)));
              };

          FNOP.prototype = this.prototype;
          fBound.prototype = new FNOP();

          return fBound;
        };
    }

    $(document).ready(function() {
        app.init();
    });

    // tests for some accessibility misses
    // use in browser console with AccessibilityTest()
    window.AccessibilityTest = function() {
        // I think this will keep IE from crying?
        var console = console || {error: function() {}};

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
    };
});
