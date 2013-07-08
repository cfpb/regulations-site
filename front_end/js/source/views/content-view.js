// **Extends** Backbone.View
//
// **Jurisdiction** .main-content
//
// **Usage** ```require(['content-view'], function(ContentView) {})```
define('content-view', ['jquery', 'underscore', 'backbone', 'jquery-scrollstop', 'regs-dispatch', 'definition-view', 'sub-head-view'], function($, _, Backbone, jQScroll, Dispatch, DefinitionView, SubHeadView) {
    'use strict';

    var ContentView = Backbone.View.extend({

        // caches the openDefinition so that main-content links can reflect status        
        openDefinition: {
            id: '',
            view: {},
            link: {}
        },

        events: {
            'click .definition': 'clickDefinitionLink',
            'click .expand-button': 'expandInterp',
            'click .inline-interp-header': 'expandInterp',
            'click .inline-interpretation:not(.open)': 'expandInterp',
            'mouseenter p': 'showPermalink',
            'mouseenter h2.section-number': 'showPermalink'
        },

        initialize: function() {
            var len, i;

            // **Event Listeners**
            //
            // * when a definition is removed, cleanup related data
            Dispatch.on('definition:remove', this.cleanupDefinition, this);

            // * when a table of contents link is clicked, make sure browser focus updates
            Dispatch.on('toc:click', this.changeFocus, this);

            // * when a scroll event completes, check what the active secion is
            $(window).on('scrollstop', (_.bind(this.checkActiveSection, this)));

            // cache all sections in the DOM eligible to be the active section
            // also cache some jQobjs that we will refer to frequently
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

            // new View instance for subheader
            this.header = new SubHeadView({el: '#content-subhead'});

        },

        // naive way to update the active table of contents link and wayfinding header
        // once a scroll event ends, we loop through each content section DOM node
        // the first one whose offset is greater than the window scroll position, accounting
        // for the fixed position header, is deemed the active section
        checkActiveSection: function() {
            var len = this.$contentContainer.length - 1;

            for (var i = 0; i <= len; i++) {
                if (this.$sections[i].offset().top + this.$contentHeader.height() >= this.$window.scrollTop()) {
                    if (_.isEmpty(this.activeSection) || (this.activeSection !== this.$sections[i].id)) {
                        this.activeSection = this.$sections[i][0].id;
                        this.$activeSection = this.$sections[i][0];
                        // **Event** trigger active section change
                        Dispatch.trigger('activeSection:change', this.activeSection);
                        return;
                    }
                }
            }
                 
            return this;
        },

        // remove cached items once a definition is closed, adjust link classes accordingly
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

        // content section key term link click handler
        // **TODO** this is too long to be good
        clickDefinitionLink: function(e) {
            e.preventDefault();
            var $link = $(e.target),
                defId;

            // if this definition is already open, close it
            if ($link.data('active')) {
                this.openDefinition.view.remove();
                return this;
            }

            defId = $link.attr('data-definition');
            $link.addClass('active').data('active', 1);

             // if its the same def, diff link (with same text), update the active link and we're done
            if (defId === this.openDefinition.id && $link.text().toLowerCase() === this.openDefinition.linkText) {
                this.openDefinition.link.removeClass('active').removeData('active');
                this.openDefinition.link = $link;           

                return this;
            }

            // if this is a definition that is different from one already open, close the open one
            if (!_.isEmpty(this.openDefinition.view)) {
                this.openDefinition.view.remove();
            }

            // create a new open definition
            this.storeDefinition($link, defId);

            return this;
        },

        // creates a new Definition View
        // TODO: I'm guessing this could be more concise, depend less on DOM
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

        // handler for when inline interpretation is clicked
        expandInterp: function(e) {
            e.stopPropagation();
            var button;

            // user can click on the gray space, "show" button or header on a closed interp
            // for an open interp, they can click "hide" button or header
            // **TODO** markup rethink?
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

        // handler for when a permalink icon should be shown
        showPermalink: function(e) {
            $('.permalink-marker').remove();

            var permalink = document.createElement('a'),
                currentLocal = $(e.currentTarget),
                currentId, $permalink, parent;

            /* inline interps don't have permalinks */
            if (currentLocal.parents().hasClass('inline-interpretation')) {
                return;
            }

            // **TODO**: markup refactor
            // Use data attributes instead of of tag and location to determine flow
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
