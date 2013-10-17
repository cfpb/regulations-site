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

            if (Dispatch.hasPushState) {
                Router.navigate('sxs/' + sxsURL);
            }

            Dispatch.trigger('ga-event:sxs', {
                opensxs: this.options.regParagraph + ' ' + this.options.docNumber + ' ' + this.options.fromVersion
            });

            Dispatch.on('sxs:close', this.closeAnalysis, this);


            // if the browser doesn't support pushState, don't 
            // trigger click events for links
            if (Dispatch.hasPushState === false) {
                this.events = {};
            }

        },

        render: function(analysis) {
            this.$el.html(analysis);
            this.$el.addClass('open-sxs');
            Dispatch.trigger('breakaway:open');
        },

        closeAnalysis: function(e) {
            if (typeof e !== 'undefined') {
                e.preventDefault();
                window.history.back();
            }

            this.$el.removeClass('open-sxs');
            Dispatch.trigger('breakaway:close');
            Dispatch.trigger('ga-event:sxsclose', Dispatch.getOpenSection());

            Dispatch.get('sxs-analysis').remove();
        },

        remove: function() {
            this.$el.html('');
            this.stopListening();
            this.$el.off();
            return this;
        }
    });

    return SxSView;
});