define('sxs-list-view', ['jquery', 'underscore', 'backbone', 'dispatch', 'sidebar-list-view', './folder-model'], function($, _, Backbone, Dispatch, SidebarListView, FolderModel) {
    'use strict';
    var SxSListView = SidebarListView.extend({
        el: '#sxs-list',

        events: {
            'click a': 'openSxS'
        },

        initialize: function() {
            var analyses = this.$el.find('.chunk');
            this.model = new FolderModel({supplementalPath: 'sidebar'});

            this.model.set(Dispatch.getOpenSection(), analyses);

            Dispatch.on('section:open', this.getAnalyses, this);
        },

        openSxS: function(e) {
            e.preventDefault();
        },

        getAnalyses: function(sectionId) {
debugger;
            this.model.get(sectionId);
        }
    });

    return SxSListView;
});
