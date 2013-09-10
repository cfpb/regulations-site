define('search-results-view', ['jquery', 'underscore', 'backbone', 'dispatch', './search-model', './regs-router'], function($, _, Backbone, Dispatch, SearchModel, Router) {
    'use strict';

    var SearchResultsView = Backbone.View.extend({
        initialize: function() {
            var query = this.options.query,
                version = this.options.version,
                reg = Dispatch.getRegId(),
                url,
                results;

            this.url = reg + '?q=' + query + '&version=' + version;
            results = SearchModel.get(this.url);

            if (typeof results.done !== 'undefined') {
                results.done(function(res) {
                    this.render(res);
                }.bind(this));
            }
            else {
                this.render(results);
            }
        },

        render: function(results) {
            Dispatch.trigger('mainContent:change', results);
            Router.navigate('search/' + this.url);
        } 
    });

    return SearchResultsView;

});
