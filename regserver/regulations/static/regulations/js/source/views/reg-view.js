// **Extends** Backbone.View
//
// **Jurisdiction** .main-content
//
// **Usage** ```require(['reg-view'], function(RegView) {})```
define('reg-view', ['jquery', 'underscore', 'backbone', 'jquery-scrollstop', 'dispatch', 'definition-view', 'sub-head-view', 'reg-model', 'section-footer-view', 'regs-router'], function($, _, Backbone, jQScroll, Dispatch, DefinitionView, SubHeadView, RegModel, SectionFooterView, Router) {
    'use strict';

    var RegView = Backbone.View.extend({
        el: '.reg-text',

        events: {
            'click .definition': 'termLinkHandler',
            'click .inline-interp-header': 'expandInterp',
            'mouseenter *[data-permalink-section]': 'showPermalink',
            'click .permalink-marker': 'permalinkMarkerHandler',
            'click .definition.active': 'openDefinitionLinkHandler'
        },

        initialize: function() {
            // **Event Listeners**
            //
            // * when a definition is removed, update term links
            Dispatch.on('definition:remove', this.closeDefinition, this);

            Dispatch.on('toc:click', this.loadSection, this);
            Dispatch.on('openSection:set', this.loadSection, this);

            // * when a scroll event completes, check what the active secion is
            $(window).on('scrollstop', (_.bind(this.checkActiveSection, this)));

            // set active section vars
            // @TODO: how do activeSection and Dispatch.get('section') live together?
            this.activeSection = '';
            this.$activeSection = '';
            this.$sections = {};

            this.updateWayfinding();

            // this might be silly?
            this.$window = $(window);

            // new View instance for subheader
            this.header = new SubHeadView();
            Dispatch.set('sectionNav', new SectionFooterView({el: this.$el.find('.section-nav')}));

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

        // ask for section data, when promise is completed,
        // re-render view
        loadSection: function(sectionId) {
            var returned = RegModel.get(sectionId);

            // visually indicate that a new section is loading
            $('.reg-text').addClass('loading');

            if (typeof returned.done !== 'undefined') {
                // @TODO: error handling
                returned.done(function(section) {
                    this.openSection(section, sectionId);
                }.bind(this));
            }
            else {
               this.openSection(returned, sectionId); 
            }
        },

        openSection: function(section, sectionId) {
            Dispatch.set('section', sectionId);

            Dispatch.trigger('mainContent:change', section);
            window.scrollTo(0, 0);
            Dispatch.trigger('section:open', sectionId);

            Dispatch.set('sectionNav', new SectionFooterView({el: this.$el.find('.section-nav')}));
            Router.navigate('regulation/' + sectionId + '/' + Dispatch.getVersion());

            this.updateWayfinding();
        },

        updateWayfinding: function() {
            var i, len;

            // cache all sections in the DOM eligible to be the active section
            // also cache some jQobjs that we will refer to frequently
            this.$contentHeader = this.$contentHeader || $('header.reg-header');

            // sections that are eligible for being the active section
            this.$contentContainer = this.$el.find('.level-1 li[id], .reg-section, .appendix-section, .supplement-section');

            // cache jQobjs of each reg section
            len = this.$contentContainer.length;
            for (i = 0; i < len; i++) {
                this.$sections[i] = $(this.$contentContainer[i]);
            }
        },

        // for a consistent API
        render: function() {
            this.loadSection(Dispatch.getOpenSection());
        },

        // only concerned with resetting DOM, no matter
        // what way the definition was closed
        closeDefinition: function() {
            this.clearActiveTerms();
        },

        // only concerned with sending GA event if the definition
        // is closed via active term link
        openDefinitionLinkHandler: function(e) {
            Dispatch.trigger('ga-event:definition', {
                action: 'clicked key term to close definition',
                context: $(e.target).data('definition')
            });
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
                this.clearActiveTerms();
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
            Dispatch.trigger('definition:open');
            Dispatch.trigger('ga-event:definition', {
                action: 'clicked key term to open definition',
                context: defId
            });
            this.setActiveTerm($link);

            return definition;
        },

        // handler for when inline interpretation is clicked
        expandInterp: function(e) {

            // user can click anywhere in the header of a closed interp
            // for an open interp, they can click "hide" button or header
            e.stopPropagation();
            var header = $(e.currentTarget),
                section = header.parent(),
                button = header.find('.expand-button');

            section.toggleClass('open');
            header.next('.hidden').slideToggle();
            button.toggleClass('open').html(section.hasClass('open') ? 'Hide' : 'Show');

            return this;
        },

        // handler for when a permalink icon should be shown
        showPermalink: function(e) {
            $('.permalink-marker').remove();

            var permalink = document.createElement('a'),
                $section = $(e.currentTarget),
                $permalink;

            permalink.href = '#' + $section[0].id;
            permalink.innerHTML = 'Permalink';
            permalink.className = 'permalink-marker';
            $permalink = $(permalink);

            $section.children().first().prepend($permalink);
        },

        // send GA event when permalink is clicked
        permalinkMarkerHandler: function(e) {
            Dispatch.trigger('ga-event:permalink', $(e.target).attr('href'));
        },

        changeFocus: function(id) {
            $(id).focus();
        },

        // Sets DOM back to neutral state
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

    return RegView;
});
