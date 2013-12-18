define('drawer-view', ['jquery', 'underscore', 'backbone', 'toc-view', 'history-view', 'search-view', 'drawer-tabs-view', 'drawer-events'], function($, _, Backbone, TOCView, HistoryView, SearchView, DrawerTabs, DrawerEvents) {
    'use strict';

    var DrawerView = Backbone.View.extend({
        el: '#menu',

        initialize: function() {
            DrawerEvents.on('pane:change', this.setActivePane, this);

            this.$label = $('.toc-type');
            this.$children = $('.toc-container');
            this.childViews = {
                'table-of-contents': {
                    'selector': $('#table-of-contents'),
                    'constructor': TOCView
                },
                'timeline': {
                    'selector': $('#timeline'),
                    'constructor': HistoryView
                },
                'search': {
                    'selector': $('#search'),
                    'constructor': SearchView
                }
            };
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
            this.childViews[activeId]['selector'].removeClass('hidden');

            // create a new childView if a view doesn't already exist
            this.childViews[activeId].view = this.childViews[activeId].view || new this.childViews[activeId].constructor();
        }

    });

    var drawer = new DrawerView();
    return drawer;
});
