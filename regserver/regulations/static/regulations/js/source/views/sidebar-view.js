// **Extends** Backbone.View
//
// **Usage** ```require(['sidebar-view'], function(SidebarView) {})```
//
// **Jurisdiction** Right sidebar content section
define('sidebar-view', ['jquery', 'underscore', 'backbone', 'dispatch', 'sidebar-head-view', 'sxs-list-view', 'permalink-view'], function($, _, Backbone, Dispatch, SidebarHeadView, SxSListView, PermalinkView) {
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

            Dispatch.on('search:submitted', this.closeAllChildren, this);
            Dispatch.on('regSection:open', this.openRegFolders, this);

            Dispatch.on('regSection:open', this.removeLandingSidebar, this);

            this.childViews = {};
            this.$el.definition = this.$el.find('#definition');
            this.openRegFolders();
        },

        openRegFolders: function() {
            if (this.childViews.sxs) {
                this.childViews.sxs.remove();
            }

            if (this.childViews.permalink) {
                this.childViews.permalink.remove();
            }

            if (this.$el.find('#sxs-list').length === 0) {
                this.$el.append('<section id="sxs-list" class="regs-meta"></section>');
            }

            if (this.$el.find('#permalinks').length === 0) {
                this.$el.append('<section id="permalinks" class="regs-meta"></section>');
            }

            this.childViews.sxs = new SxSListView();
            this.childViews.permalink = new PermalinkView();    
        },

        removeLandingSidebar: function() {
            $('.landing-sidebar').hide();
        },

        // open whatever content should populate the sidebar
        insertChild: function(el) {
            this.$el.append(el); 
        },

        removeChild: function(el) {
            $(el).remove();
        },

        insertDefinition: function(el) {
            if (this.$el.definition.length === 0) {
                // if the page was loaded on the landing, search or 404 page, 
                // it won't have the content sidebar template
                this.$el.prepend('<section id="definition"></section>');
                this.$el.definition = this.$el.find('#definition');
            }

            this.$el.definition.html(el);
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
            var $expandable = $(e.currentTarget);
            if (typeof e.stopPropagation !== 'undefined') {
                e.stopPropagation();
                $expandable = $(e.currentTarget);
            }
            else {
                $expandable = e;
            }

            $expandable.toggleClass('open')
                .next('.chunk').slideToggle();
        },

        closeAllChildren: function() {
            var k;
            for (k in this.childViews) {
                if (this.childViews.hasOwnProperty(k)) {
                    this.childViews[k].remove();
                }
            }
        }
    });

    return SidebarView;
});
