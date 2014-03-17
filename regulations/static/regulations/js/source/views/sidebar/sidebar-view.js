define('sidebar-view', ['jquery', 'underscore', 'backbone', 'sxs-list-view', 'help-view', './sidebar-model', 'breakaway-view', 'sidebar-events', 'definition-view', 'meta-model', 'main-events'], function($, _, Backbone, SxSList, HelpView, SidebarModel, Breakaway, SidebarEvents, Definition, MetaModel, MainEvents) {
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
            this.externalEvents.on('section:error', this.loaded, this);
            this.externalEvents.on('breakaway:open', this.hideChildren, this);

            // in order to avoid acrobatics when loading a sidebar partial,
            // the definition container is added here instead of in django tmpl
            this.$el.prepend('<section id="definition"></section>');

            this.childViews = {};
            this.openRegFolders();


            this.model = new SidebarModel();

            this.definitionModel = new MetaModel({
                supplementalPath: 'definition'
            });
        },

        openDefinition: function(config) {
            var createDefView = function(cb, success, res) {
                var errorMsg;

                if (success) {
                    this.childViews.definition.render(res);
                }
                else {
                    errorMsg = 'We tried to load that definition, but something went wrong. ';
                    errorMsg += '<a href="#" class="update-definition inactive internal" data-definition="' + this.childViews.definition.id + '">Try again?</a>';

                    this.childViews.definition.renderError(errorMsg);
                }
            }.bind(this);

            this.childViews.definition = new Definition({
                id: config.id,
                term: config.term
            });

            config.cb = config.cb || null;

            this.definitionModel.get(config.id, _.partial(createDefView, config.cb));
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
                    MainEvents.trigger('definition:carriedOver');
                    break;
                case 'search':
                    this.closeChildren();
                    this.loaded();
                    break;
                case 'diff':
                    this.loaded();
                    break;
                default:
                    this.closeChildren();
                    this.loaded();
            }

            this.removeLandingSidebar();
        },

        openRegFolders: function(success, html) {
            var len;

            // close all except definition
            this.closeChildren('definition');

            if (arguments.length > 1) {
                // if we've already downloaded the sidebar
                this.insertChild(html);
            }
            else {
                this.createPlaceholders();
            }

            // new views to bind to new html
            this.childViews.sxs = new SxSList();
            this.childViews.help = new HelpView();

            this.loaded();
        },

        removeLandingSidebar: function() {
            $('.landing-sidebar').hide();
        },

        createPlaceholders: function() {
            if (this.$el.find('#sxs-list').length === 0) {
                this.$el.append('<section id="sxs-list" class="regs-meta"></section>');
            }

            if (this.$el.find('#help').length === 0) {
                this.$el.append('<section id="help" class="regs-meta"></section>');
            }
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

        closeChildren: function(except) {
            var k;
            for (k in this.childViews) {
                if (this.childViews.hasOwnProperty(k)) {
                    if (!except || except && except !== k) {
                        this.childViews[k].remove();
                    }
                }
            }
        },

        loading: function() {
            this.$el.addClass('loading');
        },

        loaded: function() {
            this.$el.removeClass('loading');
        },

        // when breakaway view loads
        hideChildren: function() {
            this.$el.children().fadeOut(750);
            this.closeChildren();
        }
    });

    return SidebarView;
});
