define("sub-head-view", ['jquery', 'underscore', 'backbone', 'regs-fixed-el-view'], function($, _, Backbone, RegsFixedElView) {
    "use strict";
    var SubHeadView = RegsFixedElView.extend({
        initialize: function() {
            this.menuOffset = this.$el.offset().top;
            Events.on('contract', this.contract, this);
            Events.on('expand', this.expand, this);
        }
    });

    return SubHeadView;
});
