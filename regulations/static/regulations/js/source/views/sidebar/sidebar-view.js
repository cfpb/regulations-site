define('sidebar-view', ['jquery', 'underscore', 'backbone', 'sxs-list-view', 'permalink-view', './folder-model', 'main-view', 'breakaway-view', 'sidebar-events', 'definition-view', 'meta-model'], function($, _, Backbone, SxSList, PermalinkView, FolderModel, Main, Breakaway, SidebarEvents, Definition, MetaModel) {
    'use strict';
    var SidebarView = Backbone.View.extend({
        el: '#sidebar-content',

        events: {
            'click .expandable': 'toggleExpandable'
        },

        initialize: function() {
            this.events = SidebarEvents;
            this.events.on('update', this._updateChildViews, this);
            this.events.on('definition:open', this._openDefinition, this);
            this.events.on('definition:close', this._closeDefinition, this);

            this.childViews = {};
            this.openRegFolders();
            this.sxsModel = new FolderModel({
                supplementalPath: 'sidebar'
            });

            this.definitionModel = new MetaModel({
                supplementalPath: 'definition'
            });
        },

        _openDefinition: function(id) {
            var createDefView = function(res) {
                this.childViews.definition.render(res);
            }.bind(this);

            this.childViews.definition = new Definition({
                id: id
            });

            this.definitionModel.get(id, createDefView);
        },

        _closeDefinition: function() {
            if (typeof this.childViews.definition !== 'undefined') {
                this.childViews.definition.remove();
            }
        },

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

            this.removeLandingSidebar();
        },

        _updateSxSList: function(id) {
            if (typeof this.childViews.sxs === 'undefined') {
                // just init view for existing content
                this.childViews.sxs = new SxSList();
            }
            else {
                // request content and render
                this.sxsModel.get(id, this.childViews.sxs.render);
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
