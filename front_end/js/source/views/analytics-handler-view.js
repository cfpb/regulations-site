define('analytics-handler', ['jquery', 'underscore', 'backbone', 'regs-dispatch'], function($, _, Backbone, Dispatch) {
    'use strict';

    var AnalyticsHandler = Backbone.View.extend({
        initialize: function() {
            this.bindListeners();

            Dispatch.on('toc:click', this.sendEvent, 'Table of Contents');
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
                action = 'clicked link to ' + e;
                object = this; 
            }

            ga('send', 'event', object, action);
        },

        bindListeners: function() {
            $('#menu-link').on('click', { 
                object: 'Table of Contents', 
                action: function() {
                    return $('#menu').hasClass('active') ? 'close' : 'open';
                }
            }, this.sendEvent);

            $('#toc-close').on('click', {object: 'Table of Contents', action: 'close (bottom link)'}, this.sendEvent);
        }
    });

    return AnalyticsHandler;
});
