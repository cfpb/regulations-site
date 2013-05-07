define("definition-view", ["jquery", "underscore", "backbone", "regs-data"], function($, _, Backbone, RegsData) {
    "use strict";
    var DefinitionView = Backbone.View.extend({
        className: "open-definition",
        events: {},

        initialize: function() {
            this.model = {
                id: this.options.termId,
                content: RegsData.retrieve(this.options.termId),
                $termLink: $(this.options.termLink)
            };

            this.render();
        },

        render: function() {
            var xoff = this.model.$termLink.offset().top;
            this.$el.html(this.model.content);
            $('#reg-content').append(this.$el.css('top', xoff + 'px').css('left', '10px').css('width', '100px').css('position', 'absolute'));

            return this;
        }

    });

    return DefinitionView;
});
