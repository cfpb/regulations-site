// **Extends** Backbone.View
//
// **Usage** ```require(['toc-view'], function(TOCView) {})```
//
// **Jurisdiction** Expandable Table of Contents
define('toc-view', ['jquery', 'underscore', 'backbone', 'regs-dispatch', 'regs-helpers'], function($, _, Backbone, Dispatch, RegsHelpers) {
    'use strict';
    var TOCView = Backbone.View.extend({
        el: '#menu',

        events: {
            'click a': 'sendClickEvent'
        },

        initialize: function() {
            // **Event Listeners**
            // when the active section changes, highlight it in the TOC
            Dispatch.on('activeSection:change', this.setActive, this);

            
            Dispatch.on('toc:stateChange', this.changeContents, this);

            this.$children = $('.toc-container');
            this.childViews = {
                '#table-of-contents': $('#table-of-contents'),
                '#history': $('#history'),
                '#search': $('#search')
            };

            // **TODO** need to work out a bug where it scrolls the content section
            // $('#menu-link:not(.active)').on('click', this.scrollToActive);
        },

        // update active classes, find new active based on the reg entity id in the anchor
        setActive: function(id) {
            this.$el.find('.current').removeClass('current');
            this.$el.find('a[href=#' + RegsHelpers.findBaseSection(id) + ']').addClass('current');

            return this;
        },

        // **Event trigger**
        // when a TOC link is clicked, send an event along with the href of the clicked link
        sendClickEvent: function(e) {
            Dispatch.trigger('toc:click', $(e.target).attr('href'));
        },

        changeContents: function(activeId) {
            this.$children.addClass('hidden');
            this.childViews[activeId].removeClass('hidden');
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
