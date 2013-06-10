define("sidebar-view", ["jquery", "underscore", "backbone", "regs-state", "regs-dispatch"], function($, _, Backbone, RegsState, Dispatch) {
    var SidebarView = Backbone.View.extend({
        initialize: function() {
            Dispatch.on('definition:render', this.insertChild, this); 
        },
        render: function() {},

        insertChild: function() {
            this.$el.html(RegsState.openDef.view.$el); 
        }
    });

    return SidebarView;
});
