define('drawer-view', ['jquery', 'underscore', 'backbone', 'toc-view', 'history-view', 'search-view', 'drawer-tabs-view', 'drawer-events'], function($, _, Backbone, TOCView, HistoryView, SearchView, DrawerTabs, DrawerEvents) {
    'use strict';

    var DrawerView = Backbone.View.extend({
        el: '#menu',

        initialize: function() {
            this.externalEvents = DrawerEvents;

            this.externalEvents.on('pane:change', this.setActivePane, this);
            this.externalEvents.on('pane:init', this.setActivePane, this);

            this.$label = $('.toc-type');
            this.$children = $('.toc-container');

            this.childViews = {};
            this.childViews['table-of-contents'] = new TOCView();
            this.childViews['timeline'] = new HistoryView();
            this.childViews['search'] = new SearchView();

            this.setActivePane('table-of-contents');
        },

        // page types are more diverse and are named differently for
        // semantic reasons, so we need to associate page types
        // with the drawer panes they should be associated with
        pageTypeMap: {
            'diff': 'timeline',
            'reg-section': 'table-of-contents',
            'error': 'table-of-contents',
            'search-results': 'search'
        },

        // activeId = page type or child view type
        setActivePane: function(activeId) {
            if (typeof this.childViews[activeId] === 'undefined') {
                activeId = this.pageTypeMap[activeId]; 
            }

            // hide the content of all drawer sections
            this.$children.addClass('hidden');

            // remove the 'hidden' class from the active drawer section
            this.childViews[activeId].$el.removeClass('hidden');
        }

    });

    var drawer = new DrawerView();
    return drawer;
});
