define('analytics-handler', ['jquery', 'underscore', 'backbone', 'dispatch'], function($, _, Backbone, Dispatch) {
    'use strict';

    var AnalyticsHandler = Backbone.View.extend({
        initialize: function() {
            this.bindListeners();

            Dispatch.on('ga-event:definition', this.sendEvent, 'Inline Definition');
            Dispatch.on('regSection:open', this.sendEvent, 'Table of Contents');
            Dispatch.on('interpretation:toggle', this.sendEvent, 'Inline interpretation');
            Dispatch.on('ga-event:permalink', this.sendEvent, 'Permalink');
        },

        // TODO: standardize context on Dispatch events
        sendEvent: function(e) {
            var object, action, context;

            if (typeof window.ga === 'undefined') {
                return;
            }

            if (typeof e === 'object') {
                // from jQ event
                if (typeof e.data !== 'undefined') {
                    context = e.data;
                    action = context.action;
                    object = context.object;

                    if (typeof context.action === 'function') {
                        action = context.action.call();
                    }
                }
                // from Dispatch event
                else {
                    action = e.action + ' ' + e.context;
                    object = this;
                }
            }

            // also from Dispatch event
            else if (typeof e === 'string') {
                action = e;
                object = this; 
            }

            window.ga('send', 'event', object, action);
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
