define('header-view', ['jquery', 'underscore', 'backbone', 'regs-dispatch'], function($, _, Backbone, Dispatch) {
    'use strict';
    var HeaderView = Backbone.View.extend({
        el: '.reg-header',

        initialize: function() {
            this.$activeEls = $('#menu, #site-header, #reg-content');
        },

        events: {
            'click .toc-toggle': 'openTOC'
        },

        openTOC: function(e) {
            e.preventDefault();

            var $target = $(e.target),
                state = ($target.hasClass('open')) ? 'close' : 'open';

            if (typeof this.$activeEls !== 'undefined') {
                Dispatch.trigger('toc:click', state + ' toc');
                $target.toggleClass('open');
                this.$activeEls.toggleClass('active');
            }
        }
    });

    return HeaderView;
});
