define('regs-router', ['underscore', 'backbone', 'main-controller', 'queryparams'], function(_, Backbone, MainEvents) {
    'use strict';

    var RegsRouter = Backbone.Router.extend({
        routes: {
            'sxs/:section/:version': 'toSxS',
            'search/:reg': 'backToSearchResults',
            ':section/:version': 'loadSection'
        },

        loadSection: function(section) {
            var options = {id: section};

            // to scroll to paragraph if there is a hadh
            options.scrollToId = Backbone.history.getHash();

            MainEvents.trigger('section:open', section, options, 'reg-section'); 
        },

        toSxS: function(section, version, params) {
            /* jshint camelcase: false */
            Dispatch.trigger('sxs:route', {
                'regParagraph': section,
                'docNumber': version,
                'fromVersion': params.from_version
            });
        },

        backToSearchResults: function(reg, params) {
            /* jshint unused: false */
            var config = {
                query: params.q,
                version: params.version
            };

            // if there is a page number for the query string
            if (typeof params.page !== 'undefined') {
                config.page = params.page;
            }

            MainEvents.trigger('search-results:open', config);
        },

        start:  function() {
            var root = '/';

            // if the site is running under a subdirectory, create urls accordingly
            if (window.APP_PREFIX.length > 1) {
                root = window.APP_PREFIX.substring(1);
            }

            Backbone.history.start({
                pushState: 'pushState' in window.history,
                silent: true,
                root: root
            });
        },

e       hasPushState: true
    });

    if (typeof window.history === 'undefined' && typeof window.history.pushState === 'undefined') {
        RegsRouter = function() {
            this.start = function() {};
            this.navigate = function() {};
            this.hasPushState = false;
        };
    }

    var router = new RegsRouter();
    return router;
});
