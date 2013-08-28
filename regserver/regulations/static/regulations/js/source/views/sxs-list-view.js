define('sxs-list-view', ['jquery', 'underscore', 'backbone', 'sidebar-list-view'], function($, _, Backbone, SidebarListView) {
    'use strict';
    var SxSListView = SidebarListView.extend({
        el: '#sxs-list',

        events: {
            'click a': 'openSxS'
        },

        openSxS: function(e) {
            e.preventDefault();
        }
    });

    return SxSListView;
});
