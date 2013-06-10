define("toc-view", ['jquery', 'underscore', 'backbone', 'regs-fixed-el-view', 'regs-dispatch'], function($, _, Backbone, RegsFixedElView, Dispatch) {
    "use strict";
    var TOCView = RegsFixedElView.extend({
        initialize: function() {
            Dispatch.on('contract', this.contract, this);
            Dispatch.on('expand', this.expand, this);
        }
    });

    return TOCView;
});
