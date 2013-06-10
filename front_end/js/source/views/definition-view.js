define("definition-view", ["jquery", "underscore", "backbone", "regs-view", "regs-data", "regs-dispatch"], function($, _, Backbone, RegsView, RegsData, Dispatch) {
    "use strict";
    var DefinitionView = RegsView.extend({
        className: "open-definition",
        events: {},

        render: function() {
            Dispatch.trigger('definition:render', this.$el);

            return this;
        }
    });

    return DefinitionView;
});
