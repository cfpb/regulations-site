// Module called on app load, once doc.ready
//
/* jshint unused: false */
/* jshint camelcase: false */
define(['jquery', 'underscore', 'backbone', 'main-view', './regs-router', 'sidebar-view', 'header-view', 'drawer-view', 'konami'], function($, _, Backbone, MainView, Router, SidebarView, HeaderView, DrawerView, __konami__) {
    'use strict';
    return {
        // Purgatory for DOM event bindings that should happen in a View
        bindEvents: function() {
            // disable/hide an alert
            $('.disable-link').on( 'click', function(e) {
                e.preventDefault();
                $(this).closest('.displayed').addClass('disabled');
            });

            // sssshhhhhhh
            /* jshint camelcase: false */
            __konami__.enable(function() {
                var $body = $('body').prepend('<div id="modal-overlay" class="loading"></div><div id="modal"><div id="modal-intro">Made for <span class="love">Tom Kearney</span>.</div> <div id="sig"><span class="love">Love</span>,</div><ul><li>Jen Ehlers</li><li>Shashank Khandelwal</li><li>CM Lubinski</li><li>Adam Scott</li><li>Theresa Summa</li><li>John Yuda</li><div id="x">x</div></div>'),
                    topval = document.documentElement.clientHeight / 2 - 200;

                if (topval < 50) {
                    topval = 50;
                }

                $('#modal-overlay')
                    .css('height', $body.height())
                    .css('width', document.documentElement.clientWidth);

                $('#modal')
                    .css('top',  topval)
                    .css('left', document.documentElement.clientWidth / 2 - 200);

                $('#x').on('click', function() {
                    $('#modal-overlay').remove();
                    $('#modal').remove();
                });
            }, { replay: true });
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
