define('header-view', ['jquery', 'underscore', 'backbone', 'regs-dispatch'], function($, _, Backbone, Dispatch) {
    'use strict';
    var HeaderView = Backbone.View.extend({
        el: '.reg-header',

        initialize: function() {
            this.$activeEls = $('#menu, #site-header, #reg-content');
            this.$panel = $('.panel');
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
                Dispatch.trigger('toc:click', state + ' toc');
                $target.toggleClass('open');
                this.$activeEls.toggleClass('active');
            }
        },

        toggleDrawer: function(e) {
            e.preventDefault();

            var $target = $(e.target),
                $targetLink = $(e.target).attr('href'),
                $tocLinks = $('.toc-nav-link'),
                $panelClass = this.$panel.attr('class'),
                $newActive = $('.' + $panelClass + ' ' + $targetLink),
                $currentActive = $('.' + $panelClass + ' .current');

                $tocLinks.removeClass('current');
                $target.addClass('current');

                if ($newActive.hasClass('hidden')) {
                    $currentActive.toggleClass('hidden current');
                    $newActive.toggleClass('hidden current');
                }

        }
    });

    return HeaderView;
});
