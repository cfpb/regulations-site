define("definition-view", ["jquery", "underscore", "backbone", "regs-data"], function($, _, Backbone, RegsData) {
  var DefinitionView = Backbone.View.extend({
    className: "open-definition",
    events: {},

    initialize: function() {
      this.$termLink = $(this.options.termLink);

      this.model = {
        id: this.options.termId,
        content: RegsData.retrieve(this.options.termId) 
      };

      this.render();
    },

    render: function() {
      this.$el.html(this.model.content);
      $('body').append(this.$el);

      return this;
    }

  });

  return DefinitionView;
});
