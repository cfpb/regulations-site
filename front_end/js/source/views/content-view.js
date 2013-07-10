// **Extends** Backbone.View
//
// **Jurisdiction** .main-content
//
// **Usage** ```require(['content-view'], function(ContentView) {})```
define('content-view', ['jquery', 'underscore', 'backbone', 'jquery-scrollstop', 'regs-dispatch', 'definition-view', 'sub-head-view'], function($, _, Backbone, jQScroll, Dispatch, DefinitionView, SubHeadView) {
    'use strict';

    var ContentView = Backbone.View.extend({
        events: {
            'click .definition': 'termLinkHandler',
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
            // * when a definition is removed, update term links
            Dispatch.on('definition:remove', this.closeDefinition, this);

            // * when a table of contents link is clicked, make sure browser focus updates
            Dispatch.on('toc:click', this.changeFocus, this);

            // * when a scroll event completes, check what the active secion is
            $(window).on('scrollstop', (_.bind(this.checkActiveSection, this)));

            // cache all sections in the DOM eligible to be the active section
            // also cache some jQobjs that we will refer to frequently
            this.$sections = {};
            this.$contentHeader = $('header.reg-header');

            // sections that are eligible for being the active section
            this.$contentContainer = this.$el.find('.level-1 li[id], .reg-section, .appendix-section, .supplement-section');

            // set active section vars
            this.activeSection = '';
            this.$activeSection = '';

            // this might be silly?
            this.$window = $(window);

            // cache jQobjs of each reg section
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

        closeDefinition: function() {
            this.clearActiveTerms();
        },

        toggleDefinition: function($link) {
            this.setActiveTerm($link); 

            return this;
        },

        // content section key term link click handler
        termLinkHandler: function(e) {
            e.preventDefault();
            var $link = $(e.target),
                defId = $link.attr('data-definition');

            // if this link is already active, toggle def shut
            if ($link.data('active')) {
                Dispatch.remove('definition');
            }
            else {
                // if its the same definition, diff term link
                if (Dispatch.getViewId('definition') === defId) {
                    this.toggleDefinition($link);
                }
                else {
                    // close old definition, if there is one
                    Dispatch.remove('definition');
                    // open new definition
                    this.openDefinition(defId, $link);
                }
            }

            return this;
        },

        openDefinition: function(defId, $link) {
            var definition = new DefinitionView({
                id: defId,
                $anchor: $link
            });

            Dispatch.set('definition', definition);
            this.setActiveTerm($link);

            return definition;
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
        },

        clearActiveTerms: function() {
            this.$el.find('.active.definition')
                .removeClass('active')
                .removeData('active');
        },

        setActiveTerm: function($link) {
            this.clearActiveTerms();
            $link.addClass('active').data('active', 1);
        }
    });

    return ContentView;
});
