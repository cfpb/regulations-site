// **Extends** Backbone.View
//
// **Usage** ```require(['sidebar-view'], function(SidebarView) {})```
//
// **Jurisdiction** Right sidebar content section
define('sidebar-view', ['jquery', 'underscore', 'backbone', 'sidebar-head-view', 'sxs-list-view', 'permalink-view', './folder-model', 'main-view', 'breakaway-view', 'sidebar-controller'], function($, _, Backbone, SidebarHeadView, SxSList, PermalinkView, FolderModel, Main, Breakaway, SidebarEvents) {
    'use strict';
    var SidebarView = Backbone.View.extend({
        el: '#sidebar-content',

        events: {
            'click .expandable': 'toggleExpandable'
        },

        initialize: function() {
            SidebarEvents.on('update', this._updateChildViews, this);
            this.childViews = {};
            this.$el.definition = this.$el.find('#definition');
            this.openRegFolders();
            this.sxsModel = new FolderModel({
                supplementalPath: 'sidebar'
            });
        },

        modelMap: {
            'sxs': 'sxsModel'
        },

        // ask:
        // context = {}
        // context.type = page type
        // context.id = id to open

        _updateChildViews: function(context) {
            switch (context.type) {
                case 'reg-section':
                    this.openRegFolders();  
                    this._updateSxSList(context.id);
                    // this._updatePermalinks(context.id);
                    break;
                case 'search':
                    this.closeAllChildren();
                    break;
                default:
                    this.closeAllChildren();
            }

            this.removeLandingSidebar()
        },

        _updateSxSList: function(id) {
            if (typeof this.childViews.sxs === 'undefined') {
                // just init view for existing content
                this.childViews.sxs = new SxSList();
            }
            else {
                // request content and render
                this[this.modelMap.sxs].get(id, this.childViews.sxs.render);
            }
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

            this.childViews.sxs = new SxSList();
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
            this.closeExpandables();

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

    var sidebar = new SidebarView();
    return sidebar;
});
