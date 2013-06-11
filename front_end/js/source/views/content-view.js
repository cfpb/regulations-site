define("content-view", ["jquery", "underscore", "backbone", "regs-dispatch", "definition-view"], function($, _, Backbone, Dispatch, DefinitionView) {
    "use strict";

    var ContentView = Backbone.View.extend({
        openDefinition: {
            id: '',
            view: {},
            link: {}
        },

        events: {
            "click .definition": "definitionLink",
            "click .expand-button": "expandInterp"
        },

        initialize: function() {
            Dispatch.on('definition:remove', this.cleanupDefinition, this)
        },

        cleanupDefinition: function() {
            delete(this.openDefinition.id);
            if (this.openDefinition.link) {
                this.openDefinition.link.removeClass('active').removeData('active');
            }
            delete(this.openDefinition.link);

            return this;
        },

        definitionLink: function(e) {
            e.preventDefault();
            var $link = $(e.target),
                defId;

            // if already open, close it
            if ($link.data('active')) {
                this.openDefinition.view.remove();
                return this;
            }

            defId = $link.attr('data-definition');
            $link.addClass('active').data('active', 1);

             // if its the same def, diff link, we're done
            if (defId === this.openDefinition.id) {
                this.openDefinition.link.removeClass('active').removeData('active');
                this.openDefinition.link = $link;           

                return this;
            }

            if (!_.isEmpty(this.openDefinition.view)) {
                this.openDefinition.view.remove();
            }

            this.openDefinition.link = $link;           
            this.openDefinition.id = defId;
            this.openDefinition.view = new DefinitionView({
                id: defId,
                $anchor: $link
            });

            return this;
        },

        expandInterp: function(e) {
            var button = $(e.target);
            button.toggleClass('open').next('.hidden').slideToggle();
            button.html(button.hasClass('open') ? 'Hide' : 'Show');

            return this;
        }

    });

    return ContentView;
});
