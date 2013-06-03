define("regs-fixed-el-view", ['jquery', 'underscore', 'backbone'], function($, _, Backbone) {
    "use strict";
    var RegsFixedElView = Backbone.View.extend({
        expand: function() {
            this.$el.addClass('fixed');
        },

        contract: function() {
            this.$el.removeClass('fixed');
        }
    });

    return RegsFixedElView;
});
