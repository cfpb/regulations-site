define("sidebar-head-view", ["jquery", "underscore", "backbone", "regs-dispatch"], function($, _, Backbone, Dispatch) {
    "use strict";

    var SidebarHeadView = Backbone.View.extend({
        initialize: function() {
            Dispatch.on('definition:render', this.openItem, this);

            this.closeButton = $('.close');
            this.header = this.$el.find('h2');
        },

        openItem: function() {
            this.header.html("Defined Term");
            this.$el.append(this.closeButton);
        }
    });

    return SidebarHeadView;
});
