define('sxs-list-view', ['jquery', 'underscore', 'backbone', 'sidebar-list-view', './folder-model', 'sxs-view', './regs-router', 'sidebar-view', 'breakaway-controller'], function($, _, Backbone, SidebarListView, FolderModel, SxSView, Router, Sidebar, BreakawayEvents) {
    'use strict';
    var SxSListView = SidebarListView.extend({
        el: '#sxs-list',

        events: {
            'click .sxs-link': 'openSxS'
        },

        initialize: function() {
            this.render = _.bind(this.render, this);
            this.modifyListDisplay();

            // if the browser doesn't support pushState, don't 
            // trigger click events for links
            if (Router.hasPushState === false) {
                this.events = {};
            }
        },

        openSxS: function(e) {
            e.preventDefault();

            var $sxsLink = $(e.target);

            BreakawayEvents.trigger('sxs:open', {
                'regParagraph': $sxsLink.data('sxs-paragraph-id'),
                'docNumber': $sxsLink.data('doc-number'),
                'fromVersion': $('section[data-base-version]').data('base-version')
            });
        },

        render: function(html) {
            var $html = $(html),
                list = $html.find('#sxs-list').html();
            this.$el.html(list);

            this.modifyListDisplay();
        },

        modifyListDisplay: function() {
            var $folderContent = this.$el.find('.expand-drawer');
            if ($folderContent.children().length > 0) {
                this.highlightHeader();
            }
        },

        highlightHeader: function() {
            this.$el.find('header').addClass('has-content');
        }

    });

    return SxSListView;
});
