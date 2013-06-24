define('toc-view', ['jquery', 'underscore', 'backbone', 'regs-dispatch', 'regs-helpers'], function($, _, Backbone, Dispatch, RegsHelpers) {
    'use strict';
    var TOCView = Backbone.View.extend({
        events: {
            'click a': 'sendClickEvent'
        },

        initialize: function() {
            Dispatch.on('activeSection:change', this.setActive, this);
            $('#menu-link:not(.active)').on('click', this.scrollToActive);
        },

        setActive: function(id) {
            this.$el.find('.current').removeClass('current');
            this.$el.find('a[href=#' + RegsHelpers.findBaseSection(id) + ']').addClass('current');

            return this;
        },

        sendClickEvent: function(e) {
            Dispatch.trigger('toc:click', $(e.target).attr('href'));
        },

        scrollToActive: function() {
            var activeLink = document.querySelectorAll('#table-of-contents .current');

            if (activeLink[0]) {
                activeLink[0].scrollIntoView();
            }
        }
    });

    return TOCView;
});
