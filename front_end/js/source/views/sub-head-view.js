define('sub-head-view', ['jquery', 'underscore', 'backbone', 'regs-dispatch'], function($, _, Backbone, Dispatch) {
    'use strict';
    var SubHeadView = Backbone.View.extend({
        initialize: function() {
            Dispatch.on('activeSection:change', this.changeTitle, this);
        },

        changeTitle: function(id) {
            this.$el.html('<em class="header-label">§' + id + '</em>');

            return this;
        }
    });

    return SubHeadView;
});
