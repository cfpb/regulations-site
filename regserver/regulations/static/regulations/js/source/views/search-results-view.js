define('search-results-view', ['jquery', 'underscore', 'backbone', 'dispatch', './search-model', './regs-router'], function($, _, Backbone, Dispatch, SearchModel, Router) {
    'use strict';

    var SearchResultsView = Backbone.View.extend({
        events: {
            'click .search-nav a': 'paginate'
        },

        initialize: function() {
            var reg = Dispatch.getRegId(),
                results;

            this.query = this.options.query;
            this.version = this.options.version;

            this.url = reg + '?q=' + this.query + '&version=' + this.version;

            if (typeof this.options.page !== 'undefined') {
                this.url += '&page=' + this.options.page;
            }

            this.page = this.options.page || 0;

            results = SearchModel.get(this.url);

            if (typeof results.done !== 'undefined') {
                results.done(function(res) {
                    this.render(res);
                }.bind(this));
            }
            else {
                this.render(results);
            }

            Dispatch.on('searchResults:back', this.createSibling);
        },

        render: function(results) {
            this.$el.html(results);
            Dispatch.trigger('mainContent:change', this.$el, 'search-results');
            Dispatch.trigger('searchResults:open');
            Router.navigate('search/' + this.url);
        },

        paginate: function(e) {
            e.preventDefault();

            var page = $(e.target).hasClass('previous') ? this.page - 1 : this.page + 1,
                config = {
                    query: this.query,
                    version: this.version,
                    page: page
                };

            this.createSibling(config);
        },

        createSibling: function(configObj) {
            Dispatch.setContentView(
                new SearchResultsView(configObj)
            );
        },

        remove: function() {
            this.$el.remove();
            this.stopListening();
            return this;
        }
    });

    return SearchResultsView;

});
