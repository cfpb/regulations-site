define("sub-head-view", ['jquery', 'underscore', 'backbone', 'regs-fixed-el-view', "regs-dispatch"], function($, _, Backbone, RegsFixedElView, Dispatch) {
    "use strict";
    var SubHeadView = RegsFixedElView.extend({
        initialize: function() {
            // phantomjs workaround
            if (this.$el.length === 0) {
                this.$el = $('body').append('#sub-head');
            }

            this.menuOffset = this.$el.offset().top;
            Dispatch.on('contract', this.contract, this);
            Dispatch.on('expand', this.expand, this);
        }
    });

    return SubHeadView;
});
