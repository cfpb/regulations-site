// Launches app via RequireJS load
require(['jquery', 'app-init'], function($, app) {
    'use strict';
    $(document).ready(function() {
        app.init();
    });

    window.AccessibilityTest = function() {
        $('img').each(function(i, val) {
            if (typeof this.attributes.alt === 'undefined') {
                console.error('Image does not have alt text', this);
            }
        });

        $('p, h1, h2, h3, h4, h5, h6, div, span').each(function(i, val) {
            if ($(this).css('font-size').indexOf('em') === -1 && $(this).css('font-size').indexOf('px') > 0) {
                console.error('Font size is set in px, not ems', this);
            }
        });
    };
});
