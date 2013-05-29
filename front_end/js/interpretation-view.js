define("interpretation-view", ['jquery', 'underscore', 'backbone', 'regs-view', 'regs-data'], function($, _, Backbone, RegsView, RegsData) {
    "use strict";
    var InterpretationView = RegsView.extend({
        className: "open-interpretation"
    });

    return InterpretationView;
});
