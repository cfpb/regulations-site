define('sxs-view', ['jquery', 'underscore', 'backbone', 'dispatch', './sxs-model'], function($, _, Backbone, Dispatch, SxSModel) {
    'use strict';

    var SxSView = Backbone.View.extend({
        el: '#breakaway-view',

        events: {
            'click .sxs-back-button': 'closeAnalysis'
        },

        initialize: function() {
            var analysis = SxSModel.get(this.options.regParagraph + '/' + this.options.docNumber + '?from_version=' + this.options.fromVersion);

            if (typeof analysis.done !== 'undefined') {
                analysis.done(function(res) {
                    this.render(res);                    
                }.bind(this));
            }
            else {
                this.render(analysis);
            }

        },

        render: function(analysis) {
            this.$el.html(analysis);
            this.$el.addClass('open-sxs');
        },

        closeAnalysis: function(e) {
            e.preventDefault();
            this.$el.removeClass('open-sxs');
        }
    });

    return SxSView;
});
