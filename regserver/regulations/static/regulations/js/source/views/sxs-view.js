define('sxs-view', ['jquery', 'underscore', 'backbone', 'dispatch', './sxs-model', './regs-router'], function($, _, Backbone, Dispatch, SxSModel, Router) {
    'use strict';

    var SxSView = Backbone.View.extend({
        el: '#breakaway-view',

        events: {
            'click .sxs-back-button': 'closeAnalysis'
        },

        initialize: function() {
            var sxsURL = this.options.regParagraph + '/' + this.options.docNumber + '?from_version=' + this.options.fromVersion,
                analysis = SxSModel.get(sxsURL);

            if (typeof analysis.done !== 'undefined') {
                analysis.done(function(res) {
                    this.render(res);                    
                }.bind(this));
            }
            else {
                this.render(analysis);
            }

            Router.navigate(sxsURL);

            Dispatch.on('sxs:close', this.closeAnalysis, this);
        },

        render: function(analysis) {
            this.$el.html(analysis);
            this.$el.addClass('open-sxs');
        },

        closeAnalysis: function(e) {
            if (typeof e !== 'undefined') {
                e.preventDefault();
                window.history.back();
            }

            this.$el.removeClass('open-sxs');
        }
    });

    return SxSView;
});
