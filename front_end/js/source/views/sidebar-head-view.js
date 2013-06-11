define("sidebar-head-view", ["jquery", "underscore", "backbone", "regs-dispatch"], function($, _, Backbone, Dispatch) {
    "use strict";

    var SidebarHeadView = Backbone.View.extend({
        events: {
            "click .close-button": "close"
        },

        initialize: function() {
            Dispatch.on('definition:render', this.openItem, this);
            Dispatch.on('definition:remove', this.clear, this);
            this.header = this.$el.find('h2');
            this.defaultText = this.header.html();
        },

        openItem: function() {
            var closeButton, $closeButton;
            this.header.html("Defined Term");
            
            closeButton = document.createElement('a');
            $closeButton = $(closeButton);
            closeButton.className = "close-button right";
            closeButton.innerHTML = "Close definition";
            this.$el.append($closeButton);
        },

        clear: function() {
            this.$el.html(this.header.html(this.defaultText));
        },

        close: function() {
            Dispatch.trigger('definition:callRemove');
        }
    });

    return SidebarHeadView;
});
