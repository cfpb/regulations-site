define('header-view', ['jquery', 'underscore', 'backbone'], function($, _, Backbone) {
    'use strict';
    var HeaderView = Backbone.View.extend({
        el: '.reg-header',

        initialize: function() {
            this.$activeEls = $('#menu, .reg-header');
        },

        events: {
            'click .toc-toggle': 'openTOC'
        },

        openTOC: function(e) {
            e.preventDefault();
            if (typeof this.$activeEls !== 'undefined') {
                this.$activeEls.toggleClass('active');
            }
        }
    });

    return HeaderView;
});
