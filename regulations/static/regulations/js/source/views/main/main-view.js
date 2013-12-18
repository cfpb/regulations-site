define('main-view', ['jquery', 'underscore', 'backbone', 'search-results-view', 'reg-view', 'reg-model', 'search-model', 'sub-head-view', './regs-helpers', 'drawer-controller', 'section-footer-view', 'main-controller', 'sidebar-controller', './regs-router', 'drawer-view', 'diff-model', 'diff-view'], function($, _, Backbone, SearchResultsView, RegView, RegModel, SearchModel, SubHeadView, Helpers, DrawerEvents, SectionFooter, MainEvents, SidebarEvents, Router, Drawer, DiffModel, DiffView) {
    'use strict';

    var MainView = Backbone.View.extend({
        el: '#content-body',

        initialize: function() {
            this.render = _.bind(this.render, this);
            this.controller = MainEvents;

            if (Router.hasPushState) {
                this.controller.on('search-results:open', this.createView, this);
                this.controller.on('section:open', this.createView, this);
                this.controller.on('section:remove', this.sectionCleanup, this);
                this.controller.on('diff:open', this.createView, this);
                this.controller.on('breakaway:open', this._breakawayOpen, this);
            }

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
            childViewOptions.regVersion = this.regVersion;

            // find search query
            if (this.contentType === 'search-results') {
                childViewOptions.id = Helpers.parseURL(window.location.href);
                childViewOptions.params = childViewOptions.id.params;
                childViewOptions.query = childViewOptions.id.params.q;
            }

            if (this.contentType === 'landing-page') {
                DrawerEvents.trigger('pane:change', 'table-of-contents');
            }

            // we don't want to ajax in data that the page loaded with
            childViewOptions.rendered = true;

            if (this.sectionId) {
                // store the contents of our $el in the model so that we 
                // can re-render it later
                this.modelmap[this.contentType].set(this.sectionId, this.$el.html());
                childViewOptions.model = this.modelmap[this.contentType];
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
            'diff': DiffModel,
            'appendix': RegModel,
            'interpretation': RegModel
        }, 

        viewmap: {
            'reg-section': RegView,
            'search-results': SearchResultsView,
            'diff': DiffView,
            'appendix': RegView,
            'interpretation': RegView
        },

        createView: function(id, options, type) {
            if (typeof this.breakawayCallback !== 'undefined') {
                this.breakawayCallback();
                delete(this.breakawayCallaback);
            }

            this.contentType = type;
            if (id !== null) {
                this.sectionId = id;
            }

            options.id = id;
            options.type = this.contentType;
            options.regVersion = this.regVersion;
            options.regPart = this.regPart;
            options.model = this.modelmap[this.contentType];
            options.cb = this.render;

            // diffs need some more version context
            if (this.contentType === 'diff') {
                options.baseVersion = this.regVersion;
                options.newerVersion = this.$topSection.data('newer-version');
                if (typeof options.fromVersion === 'undefined') {
                    options.fromVersion = $('#table-of-contents').data('from-version');
                }
            }

            this.loading();

            if (typeof this.childView !== 'undefined') {
                this.childView.remove();
            }

            this.childView = new this.viewmap[this.contentType](options);
        },

        _breakawayOpen: function(cb) {
            this.breakawayCallback = cb;
        },

        render: function(html, options) {
            var offsetTop, $scrollToId;

            if (typeof this.childView !== 'undefined') {
                this.sectionFooter.remove();
            }

            this.$el.html(html);

            MainEvents.trigger('section:rendered');

            this.childView.attachWayfinding();

            SidebarEvents.trigger('update', {
                'type': this.contentType,
                'id': this.sectionId
            });

            if (options && typeof options.scrollToId !== 'undefined') {
                $scrollToId = $('#' + options.scrollToId);
                if ($scrollToId.length > 0) {
                    offsetTop = $scrollToId.offset().top;
                }
            }

            window.scrollTo(0, offsetTop || 0);

            this.loaded();
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
