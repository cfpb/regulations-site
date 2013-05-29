define("regs-view", ["jquery", "underscore", "backbone", "regs-data"], function($, _, Backbone, RegsData) {
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
            var xoff = this.model.$anchor.offset().top;
            this.$el.html(this.model.content);
            // remove the open definition on click
            $('.open-definition').remove();
            $('#reg-content').append(this.$el.css('top', xoff - 140 + 'px').css('right', '20px').css('width', '200px').css('position', 'absolute'));

            return this;
        }
    });

    return RegsView;
});
