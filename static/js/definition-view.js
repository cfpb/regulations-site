define(["jquery", "underscore", "backbone", "regs-data"], function($, _, Backbone, RegsData) {
  var DefinitionView = Backbone.View.extend({
    className: "open-definition",
    events: {},

    initialize: function() {
      console.log(this.options.termId);
      this.termLink = {
      };

      this.model = {
        id: this.options.termId,
        content: RegsData.retrieve(this.options.termId) 
      };

      this.render();
//      this.listenTo(this.termLink, "close", this.remove);
    },

    render: function() {
      this.$el.html(this.model.content);
      $('body').append(this.$el);
    }
  });

  return DefinitionView;
});
