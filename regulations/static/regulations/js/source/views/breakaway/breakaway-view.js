define('breakaway-view', ['jquery', 'underscore', 'backbone', 'sxs-view', './regs-router', 'breakaway-controller'], function($, _, Backbone, SxS, Router, BreakawayEvents) {
    'use strict';
    var BreakawayView = Backbone.View.extend({
        childViews: {},

        initialize: function() {
            this.controller = BreakawayEvents;
            this.controller.on('sxs:open', this._openSxS, this);
        },

        _openSxS: function(context) {
            context.url = context.regParagraph + '/' + context.docNumber + '?from_version=' + context.fromVersion;

            this.childViews.sxs = new SxS(context);

            if (Router.hasPushState) {
                Router.navigate('sxs/' + context.url);
            }
        }
    });

    var breakaway = new BreakawayView();
    return breakaway;
});
