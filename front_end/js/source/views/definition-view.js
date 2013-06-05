define("definition-view", ["jquery", "underscore", "backbone", "regs-view", "regs-data"], function($, _, Backbone, RegsView, RegsData) {
    "use strict";
    var DefinitionView = RegsView.extend({
        className: "open-definition",
        events: {}
    });

    return DefinitionView;
});
