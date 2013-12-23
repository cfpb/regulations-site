define('search-view', ['jquery', 'underscore', 'backbone', './regs-router', 'main-events'], function($, _, Backbone, Router, MainEvents) {
    'use strict';

    var SearchView = Backbone.View.extend({
        el: '#search',

        events: {
            'submit': 'openSearchResults'
        },

        initialize: function() {
            // if the browser doesn't support pushState, don't 
            // trigger click events for links
            if (Router.hasPushState === false) {
                this.events = {};
            }
        },

        openSearchResults: function(e) {
            sessionStorage.setItem('drawerDefault', 'search');

            e.preventDefault();
            var $form = $(e.target),
                options = {};

            options.query = $form.find('input[name=q]')[0].value;
            options.version = $form.find('select[name=version]')[0].value;
            MainEvents.trigger('search-results:open', null, options, 'search-results');
        }

    });

    return SearchView;
});
