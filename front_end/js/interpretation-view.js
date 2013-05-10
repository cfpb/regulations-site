define("interpretation-view", ['jquery', 'underscore', 'backbone', 'regs-data'], function($, _, Backbone, RegsData) {
    "use strict";
    var InterpretationView = Backbone.View.extend({
        className: "open-interpretation",

        initialize: function() {
            this.model = {
                id: this.options.id,
                content: RegsData.retrieve(this.options.id),
                $domContext: this.options.$domContext     
            }; 

            this.render();
        },

        render: function() {
            var xoff = this.model.$domContext.offset().top;
            this.$el.html(this.model.content);

            $('#reg-content').append(this.$el.css('top', xoff + 'px').css('left', '10px').css('width', '300px').css('position', 'absolute'));

            return this;
        }
    });

    return InterpretationView;
});
