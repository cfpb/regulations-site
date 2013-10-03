define('main-view', ['jquery', 'underscore', 'backbone', 'dispatch', 'search-results-view', 'reg-view', 'reg-model', 'search-model', 'sub-head-view'], function($, _, Backbone, Dispatch, SearchResultsView, RegView, RegModel, SearchModel, SubHeadView) {
    'use strict';

    var MainView = Backbone.View.extend({
        el: '#content-body',

        initialize: function() {
            this.header = new SubHeadView();

            Dispatch.on('mainContent:change', this.render, this);
            Dispatch.on('regSection:open', this.loadContent, this);
            Dispatch.on('search:submitted', this.assembleSearchURL, this);
            Dispatch.on('content:loading', this.loading, this);
            Dispatch.on('content:loaded', this.loaded, this);
        },

        modelmap: {
            'regSection': RegModel,
            'searchResults': SearchModel
        }, 

        viewmap: {
            'regSection': RegView,
            'searchResults': SearchResultsView
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

            // callback to be sent to model's get method
            // called after ajax resolves sucessfully
            render = function(returned) {
                this.createView(returned, options, type); 
            }.bind(this);

            // simplifies to
            // this.model.get()
            returned = this.modelmap[type].get(id, render)

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
