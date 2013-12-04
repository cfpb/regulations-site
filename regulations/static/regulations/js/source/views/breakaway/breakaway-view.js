define('breakaway-view', ['jquery', 'underscore', 'backbone', 'sxs-view', './regs-router', 'super-view'], function($, _, Backbone, SxS, Router, SuperView) {
    'use strict';
    var BreakawayView = SuperView.extend({
        childViews: {},

        contextMap: {
            'open-sxs': '_openSxS'
        },

        ask: function(message, context) {
            if (typeof this.contextMap[message] !== 'undefined') {
                this.contextMap[message].apply(context);
            }
        },

        _openSxS: function(context) {
            context.url = context.regParagraph + '/' + context.docNumber + '?from_version=' + context.fromVersion;

            this.childViews.sxs = new SxS(context);

            if (Router.hasPushState()) {
                Router.navigate('sxs/' + context.url);
            }
        }
    });

    var breakaway = new BreakawayView();
    return breakaway;
});
