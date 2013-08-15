// Launches app via RequireJS load
require(['jquery', 'app-init'], function($, app) {
    'use strict';
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
