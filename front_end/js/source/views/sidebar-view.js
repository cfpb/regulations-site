define("sidebar-view", ["jquery", "underscore", "backbone", "regs-state", "regs-dispatch", "sidebar-head-view"], function($, _, Backbone, RegsState, Dispatch, SidebarHeadView) {
    "use strict";
    var SidebarView = Backbone.View.extend({
        initialize: function() {
            Dispatch.on('definition:render', function(el) {
                this.insertChild(el);
            }, this); 

            this.header = new SidebarHeadView({el: '#sidebar-subhead'});
        },
        render: function() {},

        insertChild: function(el) {
            this.$el.html(el); 
        }
    });

    return SidebarView;
});
