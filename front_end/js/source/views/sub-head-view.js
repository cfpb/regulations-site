define("sub-head-view", ['jquery', 'underscore', 'backbone', 'regs-fixed-el-view', "regs-dispatch", "sidebar-head-view"], function($, _, Backbone, RegsFixedElView, Dispatch, SidebarHeadView) {
    "use strict";
    var SubHeadView = RegsFixedElView.extend({
        initialize: function() {
            // phantomjs workaround
            if (this.$el.length === 0) {
                this.$el = $('body').append('#sub-head');
            }

            this.menuOffset = this.$el.offset().top;
            Dispatch.on('header:contract', this.contract, this);
            Dispatch.on('header:expand', this.expand, this);
        }
    });

    return SubHeadView;
});
