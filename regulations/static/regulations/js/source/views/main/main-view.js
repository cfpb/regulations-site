define('main-view', ['jquery', 'underscore', 'backbone', 'search-results-view', 'reg-view', 'reg-model', 'search-model', 'sub-head-view', './regs-helpers', 'drawer-controller', 'section-footer-view', 'main-controller', 'sidebar-controller', './regs-router', 'drawer-view', 'diff-model', 'diff-view'], function($, _, Backbone, SearchResultsView, RegView, RegModel, SearchModel, SubHeadView, Helpers, DrawerEvents, SectionFooter, MainEvents, SidebarEvents, Router, Drawer, DiffModel, DiffView) {
    'use strict';

    var MainView = Backbone.View.extend({
        el: '#content-body',

        initialize: function() {
            this.controller = MainEvents;
            this.controller.on('search-results:open', this._assembleSearchURL, this);
            this.controller.on('section:open', this.loadContent, this);
            this.controller.on('section:remove', this.sectionCleanup, this);

            var childViewOptions = {},
                url, params;
            this.$topSection = this.$el.find('section[data-page-type]');

            // which page are we starting on?
            this.contentType = this.$topSection.data('page-type');
            // what version of the reg?
            this.regVersion = this.$topSection.data('base-version');
            // what section do we have open?
            this.sectionId = this.$topSection.attr('id');
            this.regPart = $('#menu').data('reg-id');

            // build options object to pass into child view constructor
            childViewOptions.id = this.sectionId;
            childViewOptions.version = this.regVersion;

            // find search query
            if (this.contentType === 'search-results') {
                childViewOptions.id = Helpers.parseURL(window.location.href);
                childViewOptions.params = childViewOptions.id.params;
                childViewOptions.query = childViewOptions.id.params.q;
            }

            if (this.contentType === 'landing-page') {
                DrawerEvents.trigger('pane:change', 'table-of-contents');
            }

            if (this.sectionId) {
                // store the contents of our $el in the model so that we 
                // can re-render it later
                this.modelmap[this.contentType].set(this.sectionId, this.$el.html());
            }

            if (this.contentType && typeof this.viewmap[this.contentType] !== 'undefined') {
                // create new child view
                this.childView = new this.viewmap[this.contentType](childViewOptions);
            }

            this.sectionFooter = new SectionFooter({el: this.$el.find('.section-nav')});
        },

        modelmap: {
            'reg-section': RegModel,
            'search-results': SearchModel,
            'diff': DiffModel
        }, 

        viewmap: {
            'reg-section': RegView,
            'search-results': SearchResultsView,
            'diff': DiffView
        },

        _assembleSearchURL: function(options) {
            var url = this.regPart;
            url += '?q=' + options.query;
            url += '&version=' + options.version;

            if (typeof options.page !== 'undefined') {
                url += '&page=' + options.page;
            }

            options.url = url;
            this.loadContent(url, options, 'search-results');
        },

        loadContent: function(id, options, type) {
            var returned, render;

            this.loading();

            // callback to be sent to model's get method
            // called after ajax resolves sucessfully
            render = function(returned) {
                // update current subview settings
                this.contentType = type;
                this.sectionId = id;

                this.createView(returned, options); 

                // remove overlay
                this.loaded();
            }.bind(this);

            if (typeof this.modelmap[type] !== 'undefined') {
                // simplifies to
                // this.model.get()
                returned = this.modelmap[type].get(id, render);
            }

            return this;
        },

        createView: function(html, options) {
            if (typeof options.scrollToId === 'undefined' && this.contentType === 'reg-section') {
                options.scrollToId = this.sectionId;
            }

            if (typeof this.childView !== 'undefined') {
                this.childView.remove();
                this.sectionFooter.remove();
            }

            this.render(html, options.scrollToId);
            this.childView = new this.viewmap[this.contentType](_.extend({
                id: this.sectionId,
                regVersion: this.regVersion
            }, options));
            SidebarEvents.trigger('update', {
                'type': this.contentType,
                'id': this.sectionId
            });
        },

        render: function(html, scrollToId) {
            var offsetTop, $scrollToId;

            this.$el.html(html);

            if (typeof scrollToId !== 'undefined') {
                $scrollToId = $('#' + scrollToId);
                if ($scrollToId.length > 0) {
                    offsetTop = $scrollToId.offset().top;
                }
            }

            window.scrollTo(0, offsetTop || 0);
        },

        loading: function() {
            // visually indicate that a new section is loading
            $('.main-content').addClass('loading');

        },

        loaded: function() {
            $('.main-content').removeClass('loading');

            // change focus to main content area when new sections are loaded
            $('.section-focus').focus();
        }
    });
    var main = new MainView();
    return main;
});
