define('analytics-handler', ['jquery', 'underscore', 'backbone'], function($, _, Backbone) {
    'use strict';

    var AnalyticsHandler = Backbone.View.extend({
        initialize: function() {
            this.bindListeners();

            Dispatch.on('ga-event:definition', this.sendEvent, 'Inline Definition');
            Dispatch.on('regSection:open', this.sendEvent, 'Table of Contents');
            Dispatch.on('interpretation:toggle', this.sendEvent, 'Inline interpretation');
            Dispatch.on('ga-event:permalink', this.sendEvent, 'Permalink');
            Dispatch.on('search:submitted', this.sendEvent);
            Dispatch.on('ga-event:sxs', this.sendEvent);
            Dispatch.on('ga-event:sxsclose', this.sendEvent, 'close SxS by back link');
            Dispatch.on('ga-event:sectionnav', this.sendEvent, 'navigate to section by footer pagination');
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
                // from search event
                else if (typeof e.query !== 'undefined') {
                    action = 'submitted search';
                    object = e.query + ' ' + e.version;
                }
                else if (typeof e.opensxs !== 'undefined') {
                    action = 'opened SxS';
                    object = e.opensxs;
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
