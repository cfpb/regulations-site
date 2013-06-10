define("sidebar-head-view", ["jquery", "underscore", "backbone", "regs-dispatch"], function($, _, Backbone, Dispatch) {
    "use strict";

    var SidebarHeadView = Backbone.View.extend({
        initialize: function() {
            Dispatch.on('definition:render', this.openItem, this);
            Dispatch.on('definition:remove', this.clear, this);
            this.header = this.$el.find('h2');
            this.defaultText = this.header.html();
        },

        openItem: function() {
            this.header.html("Defined Term");
            this.$el.append('<a class="close-button right">Close definition</a>');
        },

        clear: function() {
            this.$el.html(this.header.html(this.defaultText));
        }
    });

    return SidebarHeadView;
});
