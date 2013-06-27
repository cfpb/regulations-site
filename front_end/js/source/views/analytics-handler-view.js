define('analytics-handler', ['jquery', 'underscore', 'backbone', 'regs-dispatch'], function($, _, Backbone, Dispatch) {
    'use strict';

    var AnalyticsHandler = Backbone.View.extend({
        initialize: function() {
            this.bindListeners();
        },

        sendTOCEvent: function() {
            ga('send', 'event', 'toc', 'clicked');
        },

        bindListeners: function() {
            var toc;

            toc = document.getElementById('menu-link');
            toc.addEventListener('click', this.sendTOCEvent, false);
        }
    });

    return AnalyticsHandler;
});
