define('analytics-handler', ['jquery', 'underscore', 'backbone', 'ga-events'], function($, _, Backbone, GAEvents) {
    'use strict';

    var AnalyticsHandler = Backbone.View.extend({
        initialize: function() {
            this.externalEvents = GAEvents;

            this.externalEvents.on('section:open', this.sendEvent, 'open');
            this.externalEvents.on('definition:open', this.sendEvent, 'open');
            this.externalEvents.on('definition:close', this.sendEvent, 'close');
            this.externalEvents.on('interp:expand', this.sendEvent, 'expand');
            this.externalEvents.on('interp:collapse', this.sendEvent, 'collapse');
            this.externalEvents.on('interp:followCitation', this.sendEvent, 'click citation');
            this.externalEvents.on('definition:followCitation', this.sendEvent, 'click citation');
            this.externalEvents.on('sxs:open', this.sendEvent, 'open');
            this.externalEvents.on('drawer:open', this.sendEvent, 'open');
            this.externalEvents.on('drawer:close', this.sendEvent, 'close');
            this.externalEvents.on('drawer:switchTab', this.sendEvent, 'switch tab');

            // not sure if this works
            $('#timeline .stop-button').on('click', function() {
                this.sendEvent({type: 'diff'}).bind('click stop comparing');
            }.bind(this));
        },

        sendEvent: function(context) {
            var object, objectParts = [];

            if (typeof window.ga === 'undefined') {
                return;
            }

            if (typeof context.type !== 'undefined') {
                objectParts.push(context.type);

                if (_.contains(['reg-section', 'definition', 'inline-interp', 'sxs', 'drawer'], context.type)) {
                    if (typeof context.id !== 'undefined' && context.id !== null) {
                        objectParts.push(context.id);
                    }
                }
            }

            // diffs preserve ids in sectionId because
            // id has the url in order to keep a unique
            // instance cached in the model
            if (typeof context.sectionId !== 'undefined') {
                objectParts.push(context.sectionId);
            }

            if (typeof context.regVersion !== 'undefined') {
                objectParts.push('version:' + context.regVersion);
            }

            if (typeof context.baseVersion !== 'undefined' && typeof context.newerVersion !== 'undefined') {
                objectParts.push('comparing:' + context.baseVersion);
                objectParts.push(context.newerVersion);
            }

            if (typeof context.query !== 'undefined') {
                objectParts.push('query:' + context.query);
            }

            if (typeof context.page !== 'undefined') {
                objectParts.push('results page:' + context.page);
            }

            if (typeof context.from !== 'undefined') {
                objectParts.push('from:' + context.from);
            }

            if (typeof context.by !== 'undefined') {
                objectParts.push('by:' + context.by);
            }

            if (typeof context.to !== 'undefined') {
                objectParts.push('to:' + context.to);
            }

            if (typeof context.docNumber !== 'undefined') {
                objectParts.push('doc:' + context.docNumber);
            }

            object = objectParts.join(' ');

            window.ga('send', 'event', object, this);
        }
    });

    var gaHandler = new AnalyticsHandler();
    return gaHandler;
});
