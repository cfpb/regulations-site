// Module called on app load, once doc.ready
//
/* jshint unused: false */
define(['jquery', 'underscore', 'backbone', 'main-view', './regs-router', 'sidebar-view', 'header-view', 'drawer-view'], function($, _, Backbone, MainView, Router, SidebarView, HeaderView, DrawerView) {
    'use strict';
    return {
        // Purgatory for DOM event bindings that should happen in a View
        bindEvents: function() {

            // disable/hide an alert
            $('.disable-link').on( 'click', function(e) {
                e.preventDefault();
                $(this).closest('.displayed').addClass('disabled');
            });
        },

        init: function() {
            Router.start();
            this.bindEvents();
            var main = new MainView(),
                sidebar = new SidebarView(),
                drawer = new DrawerView(),
                header = new HeaderView();
            setTimeout(function() {
                $('html').addClass('selenium-start');
            }, 5000);
        }
    };
});
