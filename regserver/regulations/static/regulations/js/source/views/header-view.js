define('header-view', ['jquery', 'underscore', 'backbone', 'dispatch'], function($, _, Backbone, Dispatch) {
    'use strict';
    var HeaderView = Backbone.View.extend({
        el: '.reg-header',

        initialize: function() {
            this.$activeEls = $('#menu, #site-header, #content-body, #primary-footer');

            // view switcher buttons - TOC, calendar, search
            this.$tocLinks = $('.toc-nav-link');
        },

        events: {
            'click .toc-toggle': 'openDrawer',
            'click .toc-nav-link': 'toggleDrawerTab'
        },

        updateDrawerState: function(state) {
            if (typeof this.$activeEls !== 'undefined') {
                Dispatch.trigger('toc:toggle', state + ' toc');
                $('#panel-link').toggleClass('open');
                this.$activeEls.toggleClass('active');
            }
        },

        openDrawer: function(e) {
            e.preventDefault();

            var $target = $(e.target),
                state = ($target.hasClass('open')) ? 'close' : 'open';

            this.updateDrawerState(state);
        },

        toggleDrawerTab: function(e) {
            e.preventDefault();

            var $target = $(e.target),
                linkValue = _.last($target.closest('a').attr('href').split('#'));

            this.$tocLinks.removeClass('current');
            $target.closest('a').addClass('current');

            if ($('.panel').css('left') === '-200px') {
                this.updateDrawerState('open');
            }

            Dispatch.trigger('drawer:stateChange', linkValue);

        }
    });

    return HeaderView;
});
