// Module called on app load, once doc.ready
//
/* jshint unused: false */
/* jshint camelcase: false */
'use strict';

var $ = require('jquery');
var _ = require('underscore');
var Backbone = require('backbone');
var MainView = require('./views/main/main-view');
var Router = require('./router');
var SidebarView = require('./views/sidebar/sidebar-view');
var HeaderView = require('./views/header/header-view');
var DrawerView = require('./views/drawer/drawer-view');
var Konami = require('konami');
var AnalyticsHandler = require('./views/analytics-handler-view');
Backbone.$ = $;

 module.exports = {
    // Purgatory for DOM event bindings that should happen in a View
    bindEvents: function() {
        // disable/hide an alert
        $('.disable-link').on( 'click', function(e) {
            e.preventDefault();
            $(this).closest('.displayed').addClass('disabled');
        });

        // sssshhhhhhh
        var heart = new Konami(function() {
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
        });
    },

    init: function() {
        Router.start();
        this.bindEvents();
        var gaview = new AnalyticsHandler(),
            main = new MainView(),
            sidebar = new SidebarView(),
            header = new HeaderView(),  // Header before Drawer as Drawer sends Header events
            drawer = new DrawerView();
        setTimeout(function() {
            $('html').addClass('selenium-start');
        }, 5000);
    }
};
