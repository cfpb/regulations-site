define('analytics-handler', ['jquery', 'underscore', 'backbone', 'ga-events'], function($, _, Backbone, GAEvents) {
    'use strict';

    var AnalyticsHandler = Backbone.View.extend({
        initialize: function() {
            this.events = GAEvents;
            this.bindListeners();

            this.events.on('section:open', this.sendEvent, 'open');
        },

        // TODO: standardize context on this.events events
        sendEvent: function(context) {
            var object;

            if (typeof window.ga === 'undefined') {
                return;
            }

            if (typeof context.type !== 'undefined') {
                object = context.type;
            }

            if (typeof context.id !== 'undefined' && context.id !== null) {
                object += ' ' + context.id;
            }

            window.ga('send', 'event', object, this);
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

    var gaHandler = new AnalyticsHandler;
    return gaHandler;
});
