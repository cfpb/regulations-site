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
            'click .inline-interp-header': 'expandInterp',
            'click .inline-interpretation:not(.open)': 'expandInterp',
            'mouseenter p': 'showPermalink',
            'mouseenter h2.section-number': 'showPermalink'
        },

        initialize: function() {
            var len, i;

            Dispatch.on('definition:remove', this.cleanupDefinition, this);
            Dispatch.on('toc:click', this.changeFocus, this);
            $(window).on('scrollstop', (_.bind(this.checkActiveSection, this)));

            this.$sections = {};
            this.$contentHeader = $('header.reg-header');
            this.$contentContainer = this.$el.find('.level-1 li[id], .reg-section, .appendix-section, .supplement-section');
            this.activeSection = '';
            this.$activeSection = '';
            this.$window = $(window);

            len = this.$contentContainer.length;
            for (i = 0; i < len; i++) {
                this.$sections[i] = $(this.$contentContainer[i]);
            }
        },

        checkActiveSection: function() {
            var len = this.$contentContainer.length - 1;

            for (var i = 0; i <= len; i++) {
                if (this.$sections[i].offset().top + this.$contentHeader.height() >= this.$window.scrollTop()) {
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
            delete(this.openDefinition.linkText);

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

             // if its the same def, diff link (with same text), we're done
            if (defId === this.openDefinition.id && $link.text().toLowerCase() === this.openDefinition.linkText) {
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
            this.openDefinition.linkText = $link.text().toLowerCase();
            this.openDefinition.id = defId;
            this.openDefinition.view = new DefinitionView({
                id: defId,
                $anchor: $link,
                linkText: this.openDefinition.linkText
            });
        },

        expandInterp: function(e) {
            e.stopPropagation();
            var button;

            if (e.currentTarget.tagName.toUpperCase() === 'SECTION') {
                button = $(e.currentTarget).find('.expand-button');
            }
            else if (e.currentTarget.tagName.toUpperCase() === 'H4'){
                button = $(e.currentTarget).siblings('.expand-button');
            }
            else {
                button = $(e.currentTarget);
            }

            button.parent().toggleClass('open');
            button.toggleClass('open').next('.hidden').slideToggle();
            button.html(button.hasClass('open') ? 'Hide' : 'Show');

            return this;
        },

        showPermalink: function(e) {
            $('.permalink-marker').remove();

            var permalink = document.createElement('a'),
                currentLocal = $(e.currentTarget),
                currentId, $permalink, parent;

            if (e.currentTarget.tagName.toUpperCase() === 'H2') {
                parent = currentLocal.parent('.reg-section');
            }
            else {
                parent = currentLocal.closest('li');
            }

            if (typeof parent[0] !== 'undefined') {
                currentId = parent[0].id;

                permalink.href = '#' + currentId;
                permalink.innerHTML = 'Permalink';
                $permalink = $(permalink);

                $(currentLocal).prepend($permalink);
                $permalink.addClass('permalink-marker');
            }
        },

        changeFocus: function(id) {
            $(id).focus();
        }
    });

    return ContentView;
});
