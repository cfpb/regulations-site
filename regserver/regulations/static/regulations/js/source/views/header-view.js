define('header-view', ['jquery', 'underscore', 'backbone', 'dispatch', './regs-helpers'], function($, _, Backbone, Dispatch, Helpers) {
    'use strict';
    var HeaderView = Backbone.View.extend({
        el: '.reg-header',

        idMap: {
            'table-of-contents': '#menu-link',
            'history': '#history-link',
            'search': '#search-link'
        },

        initialize: function() {
            var openDrawer = Helpers.findStartingContent();
            this.$activeEls = $('#menu, #site-header, #content-body, #primary-footer');

            // view switcher buttons - TOC, calendar, search
            this.$tocLinks = $('.toc-nav-link');

            if (openDrawer) {
                this.changeActiveTab(openDrawer);
            }
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

            this.changeActiveTab(linkValue);

            Dispatch.trigger('drawer:stateChange', linkValue);

        },

        changeActiveTab: function(tab) {
            this.$tocLinks.removeClass('current');
            $(this.idMap[tab]).addClass('current');

            if ($('.panel').css('left') === '-200px') {
                this.updateDrawerState('open');
            }
        }
    });

    return HeaderView;
});
