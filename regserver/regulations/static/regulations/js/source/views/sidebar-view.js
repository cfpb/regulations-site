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
            'click .expandable': 'toggleExpandable'
        },

        initialize: function() {
            // **Event Listeners**
            Dispatch.on('sidebarModule:render', function(el) {
                this.insertChild(el);
            }, this); 

            Dispatch.on('sidebarModule:close', function(el) {
                this.removeChild(el);
            }, this);

            Dispatch.on('definition:open', this.closeExpandables, this);
            Dispatch.on('definition:render', this.insertDefinition, this);

            this.childViews = {};

            this.childViews.sxs = new SxSListView();
        },

        // open whatever content should populate the sidebar
        insertChild: function(el) {
            this.$el.append(el); 
        },

        removeChild: function(el) {
            $(el).remove();
        },

        insertDefinition: function(el) {
            this.$el.prepend(el);
        },

        closeExpandables: function() {
            this.$el.find('.expandable').each(function(i, folder) {
                var $folder = $(folder);
                if ($folder.hasClass('open')) {
                    this.toggleExpandable($folder);
                }
            }.bind(this));
        },

        toggleExpandable: function(e) {
            var $expandable;
            if (typeof e.stopPropagation !== 'undefined') {
                e.stopPropagation();
                $expandable = $(e.currentTarget);
            }
            else {
                $expandable = e;
            }

            $expandable.toggleClass('open')
                .next('.chunk').slideToggle();
        }
    });

    return SidebarView;
});
