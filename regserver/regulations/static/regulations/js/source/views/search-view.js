define('search-view', ['jquery', 'underscore', 'backbone', 'dispatch'], function($, _, Backbone, Dispatch) {
    'use strict';

    var SearchView = Backbone.View.extend({
        el: '#search',

        events: {
            'submit': 'openSearchResults'
        },

        initialize: function() {
            Dispatch.on('search:submitted', this.populateTextField, this);
            this.populateTextField();
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
        },

        populateTextField: function(/*config*/) {
            var $searchField = this.$el.find('input[name=q]'),
                sliceStart = window.location.search.indexOf('=') + 1,
                sliceEnd = window.location.search.indexOf('&'),
                query = window.location.search.slice(sliceStart, sliceEnd),
                pattern = new RegExp('\\+', 'g');
            //if (typeof config.query !== 'undefined') {
                if ($searchField[0].value === "") {
                    //this.$el.find('input[name=q]')[0].value = config.query;
                    // temporary solution
                    query = decodeURIComponent(query).replace(pattern, ' ');
                    $searchField[0].value = query;
                }
            //}
        }

    });

    return SearchView;
});
