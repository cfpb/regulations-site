define('breakaway-view', ['jquery', 'underscore', 'backbone', 'sxs-view', './regs-router', 'breakaway-events', 'main-events'], function($, _, Backbone, SxS, Router, BreakawayEvents, MainEvents) {
    'use strict';
    var BreakawayView = Backbone.View.extend({
        childViews: {},

        initialize: function() {
            this.events = BreakawayEvents;
            this.events.on('sxs:open', this.openSxS, this);
        },

        openSxS: function(context) {
            context.url = context.regParagraph + '/' + context.docNumber + '?from_version=' + context.fromVersion;

            this.childViews.sxs = new SxS(context);

            if (Router.hasPushState) {
                Router.navigate('sxs/' + context.url);
            }

            MainEvents.trigger('breakaway:open', _.bind(this.removeChild, this));
        },

        removeChild: function() {
            this.childViews.sxs.remove();
            delete(this.childViews.sxs);
        }
    });

    var breakaway = new BreakawayView();
    return breakaway;
});
