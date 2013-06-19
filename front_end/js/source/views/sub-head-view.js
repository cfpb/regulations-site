define('sub-head-view', ['jquery', 'underscore', 'backbone', 'regs-dispatch', 'regs-helpers'], function($, _, Backbone, Dispatch, RegsHelpers) {
    'use strict';
    var SubHeadView = Backbone.View.extend({
        initialize: function() {
            Dispatch.on('activeSection:change', this.changeTitle, this);
        },

        changeTitle: function(id) {
            this.$el.html('<em class="header-label">§' + RegsHelpers.idToRef(id) + '</em>');

            return this;
        }
    });

    return SubHeadView;
});
