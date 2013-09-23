define('search-view', ['jquery', 'underscore', 'backbone', 'dispatch'], function($, _, Backbone) {
    'use strict';

    var SearchView = Backbone.View.extend({
        el: '#search',

        events: {
            'submit': 'openSearchResults'
        },

        openSearchResults: function(e) {
            if (window.history && window.history.pushState) {
                // Temporarily removing ajax search results
                // e.preventDefault();
                var $form = $(e.target),
                    options = {};

                options.query = $form.find('input[name=q]')[0].value;
                options.version = $form.find('select[name=version]')[0].value;

                // Temporarily removing ajax search results
                // Dispatch.trigger('search:submitted', options, 'searchResults');
            }
        }

    });

    return SearchView;
});
