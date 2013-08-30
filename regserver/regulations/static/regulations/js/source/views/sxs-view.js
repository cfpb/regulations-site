define('sxs-view', ['jquery', 'underscore', 'backbone', 'dispatch', './sxs-model'], function($, _, Backbone, Dispatch, SxSModel) {
    'use strict';

    var SxSView = Backbone.View.extend({
        el: '#breakaway-view',

        initialize: function() {
            var analysis = SxSModel.get(this.options.regParagraph + '/' + this.options.version);

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
        } 
    });

    return SxSView;
});
