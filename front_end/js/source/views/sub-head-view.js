define('sub-head-view', ['jquery', 'underscore', 'backbone', 'regs-dispatch', 'regs-helpers'], function($, _, Backbone, Dispatch, RegsHelpers) {
    'use strict';
    var SubHeadView = Backbone.View.extend({
        initialize: function() {
            Dispatch.on('activeSection:change', this.changeTitle, this);
            this.$activeTitle = this.$el.find('#active-title');
        },

        changeTitle: function(id) {
            this.$activeTitle.html('<em class="header-label">' + RegsHelpers.idToRef(id) + '</em>');

            return this;
        }
    });

    return SubHeadView;
});
