define("regs-view", ["jquery", "underscore", "backbone", "regs-data", "regs-dispatch"], function($, _, Backbone, RegsData, Dispatch) {
    var RegsView = Backbone.View.extend({
        initialize: function() {
            this.model = {};
            for (field in this.options) {
                if (this.options.hasOwnProperty(field)) {
                    this.model[field] = this.options[field];
                }
            }

            if (typeof this.model.id !== "undefined") {
                this.model.content = RegsData.get(this.model.id);
                this.render();
            }

            return this;
        },

        render: function() {
            this.$el.html(this.model.content);
            Dispatch.trigger('definition:render')

            return this;
        }
    });

    return RegsView;
});
