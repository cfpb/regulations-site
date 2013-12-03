define(['jquery', 'underscore', 'backbone', 'drawer-view'], function($, _, Backbone, Drawer) {
    'use strict';
    var DrawerTabsView = Backbone.View.extend({
        el: '.toc-head',

        events: {
            'click .toc-toggle': 'openDrawer',
            'click .toc-nav-link': 'updatePaneTabs'
        },

        idMap: {
            'table-of-contents': '#menu-link',
            'timeline': '#timeline-link',
            'search': '#search-link'
        },

        initialize: function() {
            this.activeEls = $('#menu, #site-header, #content-body, #primary-footer');

            // view switcher buttons - TOC, calendar, search
            this.$tocLinks = $('.toc-nav-link');
            this.$toggleArrow = $('#panel-link');

            // For browser widths above 1100px apply the 'open' class
            if (document.documentElement.clientWidth > 1100) {
                this.$toggleArrow.addClass('open');
            }

            // set initial drawer state
            this.drawerState = (this.$toggleArrow.hasClass('open')) ? 'open' : 'closed';
        },

        _changeActiveTab: function(tab) {
            this.$tocLinks.removeClass('current');
            $(this.idMap[tab]).addClass('current');

            if ($('.panel').css('left') === '-200px') {
                this.updateDrawerState('open');
            }
        },

        // this.$activeEls are structural els that need to have
        // CSS applied to work with the drawer conditionally based
        // on its state
        reflowUI: function(state) {
            if (typeof this.$activeEls !== 'undefined') {
                this.$activeEls.toggleClass('active');
            }
        },

        openDrawer: function(e) {
            e.preventDefault();
            this._toggleDrawerState();
        },

        // figure out whether drawer should open/close
        // tell surrounding elements to update accordingly
        // update the open/close arrow
        // set state
        _toggleDrawerState: function() {
            var state = (this.$toggleArrow.hasClass('open')) ? 'close' : 'open';
            this.reflowUI(state);
            this.$toggleArrow.toggleClass('open');
            this.drawerState = state;
        },

        // update active pane based on click or external input
        updatePaneTabs: function(e) {
            e.preventDefault();

            var $target = $(e.target),
                linkValue = _.last($target.closest('a').attr('href').split('#'));
            this._changeActiveTab(linkValue);
            this.activePane = linkValue;

            Drawer.notify('pane-change', linkValue);
        }
    });

    var drawerTabs = new DrawerTabsView();
    return drawerTabs;
});
