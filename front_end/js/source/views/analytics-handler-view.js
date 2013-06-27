define('analytics-handler', ['jquery', 'underscore', 'backbone', 'regs-dispatch'], function($, _, Backbone, Dispatch) {
    'use strict';

    var AnalyticsHandler = Backbone.View.extend({
        initialize: function() {
            this.bindListeners();
        },

        sendEvent: function(e) {
            var object, action;
            action = e.data.action;
            object = e.data.object;

            if (typeof e.data.action === 'function') {
                action = e.data.action.call();
            }

            if (typeof e.data.object === 'function') {
                
            }

            ga('send', 'event', object, action);
        },

        bindListeners: function() {
            $('#menu-link').on('click', {object: 'toc', action: function() {
                return $('#menu').hasClass('active') ? 'close' : 'open';
            }}, this.sendEvent);
            $('#toc-close').on('click', {object: 'toc', action: 'close-bottom'}, this.sendEvent);
        }
    });

    return AnalyticsHandler;
});
