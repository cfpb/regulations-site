// **Extends** Backbone.View
//
// **Usage** ```require(['sidebar-view'], function(SidebarView) {})```
//
// **Jurisdiction** Right sidebar content section
define('sidebar-view', ['jquery', 'underscore', 'backbone', 'dispatch', 'sidebar-head-view', 'sxs-list-view'], function($, _, Backbone, Dispatch, SidebarHeadView, SxSListView) {
    'use strict';
    var SidebarView = Backbone.View.extend({
        el: '#sidebar-content',

        events: {
            'click .expandable': 'toggleMeta'
        },

        initialize: function() {
            // **Event Listeners**
            Dispatch.on('sidebarModule:render', function(el) {
                this.insertChild(el);
            }, this); 

            Dispatch.on('sidebarModule:close', function(el) {
                this.removeChild(el);
            }, this);

            this.childViews = {};

            // Init a sidebar header instance
            this.childViews.header = new SidebarHeadView({el: '#sidebar-header'});

            this.childViews.sxs = new SxSListView();
        },

        render: function() {},

        // open whatever content should populate the sidebar
        insertChild: function(el) {
            this.$el.append(el); 
        },

        removeChild: function(el) {
            $(el).remove();
        },

        toggleMeta: function(e) {
            e.stopPropagation();
            $(e.currentTarget)
                .toggleClass('open')
                .next('.chunk').slideToggle();
        }
    });

    return SidebarView;
});
