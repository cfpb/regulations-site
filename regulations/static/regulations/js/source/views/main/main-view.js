define('main-view', ['jquery', 'underscore', 'backbone', 'search-results-view', 'reg-view', 'reg-model', 'search-model', 'sub-head-view', './regs-helpers', 'drawer-view'], function($, _, Backbone, SearchResultsView, RegView, RegModel, SearchModel, SubHeadView, Helpers, Drawer) {
    'use strict';

    var MainView = Backbone.View.extend({
        el: '#content-body',

        initialize: function() {
            var childViewOptions = {},
                $topSection = this.$el.find('section[data-page-type]'),
                url, params;
            this.header = new SubHeadView();

            Dispatch.on('mainContent:change', this.render, this);
            Dispatch.on('reg-section:open', this.loadContent, this);
            Dispatch.on('search:submitted', this.assembleSearchURL, this);

            // which page are we starting on?
            this.contentType = $topSection.data('page-type');
            // what version of the reg?
            this.regVersion = $topSection.data('base-version');
            // what section do we have open?
            this.sectionId = $topSection.attr('id');

            // ask the drawer to set the active pane accordingly
            Drawer.ask('changeActivePane', this.contentType);

            // build options object to pass into child view constructor
            childViewOptions.id = this.sectionId;
            childViewOptions.version = this.regVersion;

            // find search query
            if (this.contentType === 'search') {
                url = Helpers.parseURL(window.location.href);
                params = url.params;
                childViewOptions.query = params.q;
            }

            // store the contents of our $el in the model so that we 
            // can re-render it later
            this.modelmap[this.contentType].set(sectionId, this.$el.html());

            // create new child view
            this.childView = new this.viewmap[this.contentType](childViewOptions);
        },

        modelmap: {
            'reg-section': RegModel,
            'search': SearchModel
        }, 

        viewmap: {
            'reg-section': RegView,
            'search': SearchResultsView
        },

        assembleSearchURL: function(options, type) {
            var url = Dispatch.getRegId();
            url += '?q=' + options.query;
            url += '&version=' + options.version;

            if (typeof options.page !== 'undefined') {
                url += '&page=' + options.page;
            }

            options.url = url;
            this.loadContent(url, options, type);
        },

        loadContent: function(id, options, type) {
            var returned, render;

            this.loading();

            // callback to be sent to model's get method
            // called after ajax resolves sucessfully
            render = function(returned) {
                this.createView(returned, options, type); 
                this.loaded();
                Dispatch.trigger('sxs:close');
            }.bind(this);

            // simplifies to
            // this.model.get()
            returned = this.modelmap[type].get(id, render);

            return this;
        },

        createView: function(html, options, type) {
            Dispatch.removeContentView();
            this.render(html, options.scrollToId);
            Dispatch.setContentView(new this.viewmap[type](options));
        },

        render: function(html, scrollToId) {
            var offsetTop, $scrollToId;

            this.header.reset();
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

    return MainView;
});
