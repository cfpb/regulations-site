define(["jquery", "underscore", "backbone"], function($, _, Backbone) {
  var DefinitionView = Backbone.View.extend({
    className: "open-definition",
    events: {},

    initialize: function() {
      console.log(this.model);
//      this.listenTo(this.termLink, "close", this.remove);
    },

    render: function() {
      // find context from this.termLink
    }
  });

  return DefinitionView;
});
