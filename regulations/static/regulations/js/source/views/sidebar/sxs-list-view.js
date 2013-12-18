define('sxs-list-view', ['jquery', 'underscore', 'backbone', 'sidebar-list-view', './folder-model', 'sxs-view', './regs-router', 'sidebar-view', 'breakaway-events', 'ga-events'], function($, _, Backbone, SidebarListView, FolderModel, SxSView, Router, Sidebar, BreakawayEvents, GAEvents) {
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

            var $sxsLink = $(e.target),
                id = $sxsLink.data('sxs-paragraph-id'),
                docNumber = $sxsLink.data('doc-number'),
                version = $('section[data-base-version]').data('base-version');

            BreakawayEvents.trigger('sxs:open', {
                'regParagraph': id,
                'docNumber': docNumber,
                'fromVersion': version
            });

            GAEvents.trigger('sxs:open', {
                id: id,
                docNumber: docNumber,
                regVersion: version,
                type: 'sxs' 
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
