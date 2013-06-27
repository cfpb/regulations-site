define('analytics-handler', ['jquery', 'underscore', 'backbone', 'regs-dispatch'], function($, _, Backbone, Dispatch) {
    'use strict';

    var AnalyticsHandler = Backbone.View.extend({
        initialize: function() {
            this.bindListeners();

            Dispatch.on('toc:click', this.sendEvent, 'toc');
        },

        sendEvent: function(e) {
            var object, action, context;

            // from jQ event
            if (typeof e === 'object') {
                context = e.data;
                action = context.action;
                object = context.object;

                if (typeof context.action === 'function') {
                    action = context.action.call();
                }

                if (typeof context.object === 'function') {
                    object = context.object.call();    
                }
            }

            // from Dispatch event
            else {
                action = 'click-' + e;
                object = this; 
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
