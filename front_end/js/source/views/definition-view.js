define("definition-view", ["jquery", "underscore", "backbone", "regs-view", "regs-data", "regs-dispatch"], function($, _, Backbone, RegsView, RegsData, Dispatch) {
    "use strict";
    var DefinitionView = RegsView.extend({
        className: "open-definition",
        events: {},

        render: function() {
            Dispatch.once('definition:callRemove', this.remove, this);

            var interp = this.$el.find('.inline-interpretation'),
                interpId, interpLink, $interpLink,
                defLink, $defLink;

                defLink = document.createElement("a");
                $defLink = $(defLink);
                defLink.href = "#" + this.model.id;
                defLink.innerHTML = 'Go to definition in § ' + this.model.id;
                defLink.className = "continue-link";
                this.$el.append($defLink);

            if (typeof interp[0] !== 'undefined') {
                interpId = $(interp[0]).data('interpFor');
                this.$el.find('.inline-interpretation').remove();

                interpLink = document.createElement("a");
                $interpLink = $(interpLink);
                interpLink.href = "#" + interpId;
                interpLink.innerHTML = "Go to related interpretations";
                interpLink.className = "continue-link";
                this.$el.append($interpLink);
            }
            Dispatch.trigger('definition:render', this.$el);

            return this;
        },

        remove: function() {
            this.stopListening();
            this.$el.remove();
            Dispatch.trigger('definition:remove');

            return this;
        }
    });

    return DefinitionView;
});
