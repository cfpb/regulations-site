// **Extends** Backbone.View
//
// **Usage** ```require(['drawer-view'], function(DrawerView) {})```
//
// **Jurisdiction** Left panel drawer container
define('drawer-view', ['jquery', 'underscore', 'backbone', 'jquery-cookie', 'dispatch', 'toc-view', 'history-view', 'search-view'], function($, _, Backbone, jQCookie, Dispatch, TOCView, HistoryView, SearchView) {
    'use strict';

    var DrawerView = Backbone.View.extend({
        el: '#menu',

        initialize: function() {
            // the cookieValue defaults to the table of contents, else the value of the cookie set within changeContents
            var cookieValue = $.cookie('Drawer_State') || 'table-of-contents';
            
            Dispatch.on('drawer:stateChange', this.changeContents, this);

            this.$label = $('.toc-type');
            this.$children = $('.toc-container');
            this.childViews = {
                'table-of-contents': {
                    'selector': $('#table-of-contents'),
                    'constructor': TOCView
                },
                'history': {
                    'selector': $('#history'),
                    'constructor': HistoryView
                },
                'search': {
                    'selector': $('#search'),
                    'constructor': SearchView
                }
            };
            
            // initialize child view to populate drawer
            this.changeContents(cookieValue); 
        },

        changeContents: function(activeId) {
            var $expiration = new Date(),
                minutes = 60;
            //set date to 60 minutes for cookie expiration    
            $expiration.setTime($expiration.getTime() + (minutes * 60 * 1000));
            // hide the content of all drawer sections
            this.$children.addClass('hidden');
            // remove the 'hidden' class from the active drawer section
            this.childViews[activeId]['selector'].removeClass('hidden');
            // create a new childView if a view doesn't already exist
            this.childViews[activeId].view = this.childViews[activeId].view || new this.childViews[activeId].constructor();
            Dispatch.set('drawerState', activeId);
            // set a cookie value equal to the active drawer id
            $.cookie('Drawer_State', activeId, { expires: $expiration });
        }

    });

    return DrawerView;
});
