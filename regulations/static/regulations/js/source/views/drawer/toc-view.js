define('toc-view', ['jquery', 'underscore', 'backbone', 'regs-helpers', 'drawer-view', './regs-router', 'main-events', 'drawer-events'], function($, _, Backbone, RegsHelpers, Drawer, Router, MainEvents, DrawerEvents) {
    'use strict';
    var TOCView = Backbone.View.extend({
        el: '#table-of-contents',

        events: {
            'click a.diff': 'sendDiffClickEvent',
            'click a:not(.diff)': 'sendClickEvent'
        },

        initialize: function() {
            var openSection = $('section[data-page-type]').attr('id');

            DrawerEvents.on('section:open', this.setActive, this);

            if (openSection) {
                this.setActive(openSection);
            }

            // **TODO** need to work out a bug where it scrolls the content section
            // $('#menu-link:not(.active)').on('click', this.scrollToActive);

            // if the browser doesn't support pushState, don't 
            // trigger click events for links
            if (Router.hasPushState === false) {
                this.events = {};
            }
        },

        // update active classes, find new active based on the reg entity id in the anchor
        setActive: function(id) {
            this.$el.find('.current').removeClass('current');
            this.$el.find('a[data-section-id=' + RegsHelpers.findBaseSection(id) + ']').addClass('current');

            return this;
        },

        // **Event trigger**
        // when a TOC link is clicked, send an event along with the href of the clicked link
        sendClickEvent: function(e) {
            e.preventDefault();

            var sectionId = $(e.currentTarget).data('section-id');
            DrawerEvents.trigger('section:open', sectionId);
            MainEvents.trigger('section:open', sectionId, {}, 'reg-section');
        },

        sendDiffClickEvent: function(e) {
            e.preventDefault();

            var $link = $(e.currentTarget),
                sectionId = $link.data('section-id'),
                config = {},
                $metaSection = $('section[data-base-version]');

            config.newerVersion = $metaSection.data('newer-version');
            config.baseVersion = $metaSection.data('base-version');
            DrawerEvents.trigger('section:open', sectionId);
            MainEvents.trigger('diff:open', sectionId, config, 'diff');            
        },

        // **Inactive** 
        // Intended to keep the active link in view as the user moves around the doc
        scrollToActive: function() {
            var activeLink = document.querySelectorAll('#table-of-contents .current');

            if (activeLink[0]) {
                activeLink[0].scrollIntoView();
            }
        }
    });

    return TOCView;
});
