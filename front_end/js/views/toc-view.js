define("toc-view", ['jquery', 'underscore', 'backbone', 'regs-fixed-el-view'], function($, _, Backbone, RegsFixedElView) {
    "use strict";
    var TOCView = RegsFixedElView.extend({
        initialize: function() {
            Events.on('contract', this.contract, this);
            Events.on('expand', this.expand, this);
        }
    });

    return TOCView;
});
