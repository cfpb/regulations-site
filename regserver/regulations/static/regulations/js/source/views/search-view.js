define('search-view', ['jquery', 'underscore', 'backbone', 'dispatch', 'search-results-view'], function($, _, Backbone, Dispatch, SearchResultsView) {
    'use strict';

    var SearchView = Backbone.View.extend({
        el: '#search',

        events: {
            'submit': 'openSearchResults'
        },

        openSearchResults: function(e) {
            e.preventDefault();
            var $form = $(e.target);
            new SearchResultsView({
                query: $form.find('input[name=q]')[0].value,
                version: $form.find('select[name=version]')[0].value
            }); 

            Dispatch.set('contentClass', 'search-results');
        }

    });

    return SearchView;
});
