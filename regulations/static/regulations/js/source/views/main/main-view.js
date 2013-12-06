define('main-view', ['jquery', 'underscore', 'backbone', 'search-results-view', 'reg-view', 'reg-model', 'search-model', 'sub-head-view', './regs-helpers', 'drawer-controller', 'section-footer-view', 'main-controller', 'sidebar-controller', './regs-router'], function($, _, Backbone, SearchResultsView, RegView, RegModel, SearchModel, SubHeadView, Helpers, DrawerEvents, SectionFooter, MainEvents, SidebarEvents, Router) {
    'use strict';

    var MainView = Backbone.View.extend({
        el: '#content-body',

        initialize: function() {
            this.controller = MainEvents;
            this.controller.on('section:change', this.loadContent, this);
            this.controller.on('section:remove', this.sectionCleanup, this);

            var childViewOptions = {},
                $topSection = this.$el.find('section[data-page-type]'),
                url, params;

            // which page are we starting on?
            this.contentType = $topSection.data('page-type');
            // what version of the reg?
            this.regVersion = $topSection.data('base-version');
            // what section do we have open?
            this.sectionId = $topSection.attr('id');

            // build options object to pass into child view constructor
            childViewOptions.id = this.sectionId;
            childViewOptions.version = this.regVersion;

            // find search query
            if (this.contentType === 'search') {
                url = Helpers.parseURL(window.location.href);
                params = url.params;
                childViewOptions.query = params.q;

                // ask the drawer to set the active pane accordingly
                DrawerEvents.trigger('pane:change', this.contentType);
            }

            if (this.sectionId) {
                // store the contents of our $el in the model so that we 
                // can re-render it later
                this.modelmap[this.contentType].set(this.sectionId, this.$el.html());
            }

            if (this.contentType) {
                // create new child view
                this.childView = new this.viewmap[this.contentType](childViewOptions);
            }

            this.sectionFooter = new SectionFooter({el: this.$el.find('.section-nav')});
        },

        modelmap: {
            'reg-section': RegModel,
            'search': SearchModel
        }, 

        viewmap: {
            'reg-section': RegView,
            'search': SearchResultsView
        },

        sectionCleanup: function() {
            this.sectionFooter.remove();
        },

        _assembleSearchURL: function(options) {
            var url = Dispatch.getRegId();
            url += '?q=' + options.query;
            url += '&version=' + options.version;

            if (typeof options.page !== 'undefined') {
                url += '&page=' + options.page;
            }

            options.url = url;
            this.loadContent(url, options);
        },

        loadContent: function(id, options) {
            var returned, render;

            this.loading();

            // callback to be sent to model's get method
            // called after ajax resolves sucessfully
            render = function(returned) {
                this.sectionId = id;
                // we need to reset this somehow
                this.contentType = this.contentType;
                this.createView(returned, options); 
                this.loaded();
                this.route(options);
            }.bind(this);

            // simplifies to
            // this.model.get()
            returned = this.modelmap[this.contentType].get(id, render);

            return this;
        },

        createView: function(html, options) {
            if (typeof options.scrollToId === 'undefined') {
                options.scrollToId = this.sectionId;
            }

            this.childView.remove();
            this.render(html, options.scrollToId);
            this.childView = new this.viewmap[this.contentType]({id: this.sectionId});
            SidebarEvents.trigger('update', {
                'type': this.contentType,
                'id': this.sectionId
            });
        },

        route: function(options) {
            if (Router.hasPushState) {
                var url = this.sectionId + '/' + this.regVersion,
                    hashPosition;

                // if a hash has been passed in
                if (options && typeof options.scrollToId !== 'undefined') {
                    url = url + '#' + options.scrollToId;
                }
                else {
                    hashPosition = (typeof Backbone.history.fragment === 'undefined') ? -1 : Backbone.history.fragment.indexOf('#');
                    //  Be sure not to lose any hash info
                    if (hashPosition !== -1) {
                        url = url + Backbone.history.fragment.substr(hashPosition);
                    }
                }
                Router.navigate(url);
            }
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
