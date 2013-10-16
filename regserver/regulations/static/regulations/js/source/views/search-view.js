define('search-view', ['jquery', 'underscore', 'backbone', './dispatch'], function($, _, Backbone, Dispatch) {
    'use strict';

    var SearchView = Backbone.View.extend({
        el: '#search',

        events: {
            'submit': 'openSearchResults'
        },

        initialize: function() {
            // if the browser doesn't support pushState, don't 
            // trigger click events for links
            if (Dispatch.hasPushState === false) {
                this.events = {};
            }
        },

        openSearchResults: function(e) {
            sessionStorage.setItem('drawerDefault', 'search');

            // Temporarily removing ajax search results
            // e.preventDefault();
            var $form = $(e.target),
                options = {};

            options.query = $form.find('input[name=q]')[0].value;
            options.version = $form.find('select[name=version]')[0].value;
            // Temporarily removing ajax search results
            // Dispatch.trigger('search:submitted', options, 'searchResults');
        }

    });

    return SearchView;
});
