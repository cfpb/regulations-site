define('main-view', ['jquery', 'underscore', 'backbone', 'dispatch', 'search-results-view', 'reg-view', 'reg-model', 'search-model', 'sub-head-view'], function($, _, Backbone, Dispatch, SearchResultsView, RegView, RegModel, SearchModel, SubHeadView) {
    'use strict';

    var MainView = Backbone.View.extend({
        el: '#content-body',

        initialize: function() {
            this.header = new SubHeadView();

            Dispatch.on('mainContent:change', this.render, this);
            Dispatch.on('regSection:open', this.loadContent, this);
            Dispatch.on('search:submitted', this.assembleSearchURL, this);

            Dispatch.on('loading:start', this.loading, this);
            Dispatch.on('loading:finish', this.loaded, this);
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

        loadContent: function(getParam, options, type) {
            Dispatch.trigger('loading:start');
            var returned = this.modelmap[type].get(getParam);

            if (typeof returned.done !== 'undefined') {
                // @TODO: error handling
                returned.done(function(response) {
                    this.createView(response, options, type);
                }.bind(this));
            }
            else {
               this.createView(returned, options, type); 
            }
        },

        createView: function(html, options, type) {
            Dispatch.removeContentView();
            this.render(html, options.scrollToId);
            Dispatch.setContentView(new this.viewmap[type](options));
            Dispatch.trigger('loading:finish');
        },

        render: function(html, scrollToId) {
            var offsetTop;

            this.header.reset();
            this.$el.html(html);

            offsetTop = $(scrollToId).offset().top || 0;
            window.scrollTo(0, offsetTop);
        },

        loading: function() {
            // visually indicate that a new section is loading
            $('.main-content').addClass('loading');

        },

        loaded: function() {
            $('.main-content').removeClass('loading');
        }
    });

    return MainView;
});
