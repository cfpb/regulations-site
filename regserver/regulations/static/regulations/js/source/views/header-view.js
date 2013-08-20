define('header-view', ['jquery', 'underscore', 'backbone', 'regs-dispatch'], function($, _, Backbone, Dispatch) {
    'use strict';
    var HeaderView = Backbone.View.extend({
        el: '.reg-header',

        initialize: function() {
            this.$activeEls = $('#menu, #site-header, #reg-content');

            // view switcher buttons - TOC, calendar, search
            this.$tocLinks = $('.toc-nav-link');
        },

        events: {
            'click .toc-toggle': 'openTOC',
            'click .toc-nav-link': 'toggleDrawer'
        },

        openTOC: function(e) {
            e.preventDefault();

            var $target = $(e.target),
                state = ($target.hasClass('open')) ? 'close' : 'open';

            if (typeof this.$activeEls !== 'undefined') {
                Dispatch.trigger('toc:toggle', state + ' toc');
                $target.toggleClass('open');
                this.$activeEls.toggleClass('active');
            }
        },

        toggleDrawer: function(e) {
            e.preventDefault();

            var $target = $(e.target);

            this.$tocLinks.removeClass('current');
            $target.addClass('current');

            Dispatch.trigger('toc:stateChange', $target.attr('href'));
        }
    });

    return HeaderView;
});
