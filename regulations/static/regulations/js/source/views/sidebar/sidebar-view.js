define('sidebar-view', ['jquery', 'underscore', 'backbone', 'sxs-list-view', 'permalink-view', './sidebar-model', 'main-view', 'breakaway-view', 'sidebar-events', 'definition-view', 'meta-model'], function($, _, Backbone, SxSList, PermalinkView, SidebarModel, Main, Breakaway, SidebarEvents, Definition, MetaModel) {
    'use strict';
    var SidebarView = Backbone.View.extend({
        el: '#sidebar-content',

        events: {
            'click .expandable': 'toggleExpandable'
        },

        initialize: function() {
            this.openRegFolders = _.bind(this.openRegFolders, this);
            this.externalEvents = SidebarEvents;
            this.externalEvents.on('update', this.updateChildViews, this);
            this.externalEvents.on('definition:open', this.openDefinition, this);
            this.externalEvents.on('definition:close', this.closeDefinition, this);
            this.externalEvents.on('section:loading', this.loading, this);

            this.childViews = {};
            this.openRegFolders();
            this.model = new SidebarModel();

            this.definitionModel = new MetaModel({
                supplementalPath: 'definition'
            });
        },

        openDefinition: function(id) {
            var createDefView = function(res) {
                this.childViews.definition.render(res);
            }.bind(this);

            this.childViews.definition = new Definition({
                id: id
            });

            this.definitionModel.get(id, createDefView);
        },

        closeDefinition: function() {
            if (typeof this.childViews.definition !== 'undefined') {
                this.childViews.definition.remove();
            }
        },

        updateChildViews: function(context) {
            switch (context.type) {
                case 'reg-section':
                    this.model.get(context.id, this.openRegFolders);
                    break;
                case 'search':
                    this.closeAllChildren();
                    this.loaded();
                    break;
                case 'diff':
                    this.loaded();
                    break;
                default:
                    this.closeAllChildren();
                    this.loaded();
            }

            this.removeLandingSidebar();
        },

        openRegFolders: function(html) {
            this.closeAllChildren();

            if (arguments.length > 0) {
                this.insertChild(html);
            }
            else {
                this.createPlaceholders();
            }

            this.childViews.sxs = new SxSList();
            this.childViews.permalink = new PermalinkView();    

            this.loaded();
        },

        removeLandingSidebar: function() {
            $('.landing-sidebar').hide();
        },

        createPlaceholders: function() {
            if (this.$el.find('#sxs-list').length === 0) {
                this.$el.append('<section id="sxs-list" class="regs-meta"></section>');
            }

            if (this.$el.find('#permalinks').length === 0) {
                this.$el.append('<section id="permalinks" class="regs-meta"></section>');
            }
        },

        // open whatever content should populate the sidebar
        insertChild: function(el) {
            this.$el.prepend(el); 
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
        },

        loading: function() {
            this.$el.addClass('loading');
        },

        loaded: function() {
            this.$el.removeClass('loading');
        }
    });

    var sidebar = new SidebarView();
    return sidebar;
});
