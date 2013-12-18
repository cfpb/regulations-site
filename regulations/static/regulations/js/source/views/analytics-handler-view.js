define('analytics-handler', ['jquery', 'underscore', 'backbone', 'ga-events'], function($, _, Backbone, GAEvents) {
    'use strict';

    var AnalyticsHandler = Backbone.View.extend({
        initialize: function() {
            this.events = GAEvents;
            this.bindListeners();

            this.events.on('section:open', this.sendEvent, 'open');
        },

        sendEvent: function(context) {
            var object, objectParts = [];

            if (typeof window.ga === 'undefined') {
                return;
            }

            if (typeof context.type !== 'undefined') {
                objectParts.push(context.type);
            }

            // diffs preserve ids in sectionId because
            // id has the url in order to keep a unique
            // instance cached in the model
            if (typeof context.sectionId !== 'undefined') {
                objectParts.push(context.sectionId);
            }
            else if (typeof context.id !== 'undefined' && context.id !== null) {
                objectParts.push(context.id);
            }

            if (typeof context.regVersion !== 'undefined') {
                objectParts.push('version:' + context.regVersion);
            }

            if (typeof context.baseVersion !== 'undefined' && typeof context.newerVersion !== 'undefined') {
                objectParts.push('comparing:' + context.baseVersion);
                objectParts.push(context.newerVersion);
            }

            object = objectParts.join(' ');

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
