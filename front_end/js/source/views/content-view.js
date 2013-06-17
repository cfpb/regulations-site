define('content-view', ['jquery', 'underscore', 'backbone', 'jquery-scrollstop', 'regs-dispatch', 'definition-view'], function($, _, Backbone, jQScroll, Dispatch, DefinitionView) {
    'use strict';

    var ContentView = Backbone.View.extend({
        openDefinition: {
            id: '',
            view: {},
            link: {}
        },

        events: {
            'click .definition': 'definitionLink',
            'click .expand-button': 'expandInterp',
            'mouseenter p': 'showPermalink'
        },

        initialize: function() {
            var len, i;

            Dispatch.on('definition:remove', this.cleanupDefinition, this);
            $(window).on('scrollstop', (_.bind(this.checkActiveSection, this)));

            this.$sections = {};
            this.$contentHeader = $('#content-subhead');
            this.$contentContainer = this.$el.children().last().children();
            this.activeSection = '';
            this.$activeSection = '';

            len = this.$contentContainer.length;
            for (i = 0; i < len; i++) {
                this.$sections[i] = $(this.$contentContainer[i]);
            }
        },

        checkActiveSection: function() {
            var headerLoc = this.$contentHeader.offset().top,
                len = this.$contentContainer.length;
            for (var i = 0; i < len; i++) {
                if (this.$sections[i].offset().top >= headerLoc) {
                    i = i - 1;
                    if (_.isEmpty(this.activeSection) || (this.activeSection !== this.$sections[i].id)) {
                        this.activeSection = this.$sections[i][0].id;
                        this.$activeSection = this.$sections[i][0];
                        Dispatch.trigger('activeSection:change', this.activeSection);
                        return;
                    }
                }
            }
                 
            return this;
        },

        cleanupDefinition: function() {
            delete(this.openDefinition.id);
            delete(this.openDefinition.view);
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

            this.storeDefinition($link, defId);

            return this;
        },

        storeDefinition: function($link, defId) {
            this.openDefinition.link = $link;           
            this.openDefinition.id = defId;
            this.openDefinition.view = new DefinitionView({
                id: defId,
                $anchor: $link
            });
        },

        expandInterp: function(e) {
            var button = $(e.target);
            button.toggleClass('open').next('.hidden').slideToggle();
            button.html(button.hasClass('open') ? 'Hide' : 'Show');

            return this;
        },

        showPermalink: function(e) {

            $('.permalink-marker').remove();

            var permalink = document.createElement('a'),
                currentLocal = $(e.currentTarget),
                parent = currentLocal.closest("li"),
                currentId = parent.attr('id');

            permalink.href = '#' + currentId;
            permalink.textContent = '∞';

            var $permalink = $(permalink);

            if (currentId !== undefined) {
                $(currentLocal).before($permalink);
                $permalink.addClass('permalink-marker');
            }
        }
    });

    return ContentView;
});
