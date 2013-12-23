define('sxs-view', ['jquery', 'underscore', 'backbone', './sxs-model', 'breakaway-events', 'main-events', './regs-router'], function($, _, Backbone, SxSModel, BreakawayEvents, MainEvents, Router) {
    'use strict';

    var SxSView = Backbone.View.extend({
        el: '#breakaway-view',

        events: {
            'click .sxs-back-button': 'remove',
            'click .footnote-jump-link': 'footnoteHighlight',
            'click .return-link': 'removeHighlight'
        },

        initialize: function() {
            var render;
            this.externalEvents = BreakawayEvents;

            // callback to be sent to model's get method
            // called after ajax resolves sucessfully
            render = function(returned) {
                this.render(returned);
            }.bind(this);

            SxSModel.get(this.options.url, render),

            this.externalEvents.on('sxs:close', this.remove, this);

            // if the browser doesn't support pushState, don't 
            // trigger click events for links
            if (Router.hasPushState === false) {
                this.events = {};
            }
        },

        render: function(analysis) {
            this.$el.html(analysis);
            this.$el.addClass('open-sxs');
        },

        footnoteHighlight: function(e) {
            var target = $(e.target).attr('href');
            // remove existing highlight
            this.removeHighlight();
            // highlight the selected footnote
            $('.footnotes ' + target).toggleClass('highlight');
        },

        removeHighlight: function() {
            $('.footnotes li').removeClass('highlight');
        },

        remove: function(e) {
            if (typeof e !== 'undefined') {
                e.preventDefault();
                window.history.back();
            }

            this.$el.removeClass('open-sxs');
            this.$el.html('');
            this.stopListening();
            this.$el.off();
            return this;
        }
    });

    return SxSView;
});
