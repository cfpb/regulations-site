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

            options.scrollToId = Backbone.history.getHash();

            MainEvents.trigger('section:open', section, options); 
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
// for when search is dynamically loaded again
//            var config = {
//                query: params.q,
//                version: params.version
//            };
//
//            if (typeof params.page !== 'undefined') {
//                config.page = params.page;
//            }
//
//            Dispatch.trigger('search:submitted', config, 'searchResults');
        },

        start:  function() {
            var root = '/';

            // if the site is running under a subdirectory, create urls accordingly
            if (window.APP_PREFIX) {
                root = window.APP_PREFIX.substring(1);
            }

            Backbone.history.start({
                pushState: 'pushState' in window.history,
                silent: true,
                root: root
            });
        },

        hasPushState: 'true'
    });

    if (typeof window.history === 'undefined' && typeof window.history.pushState === 'undefined') {
        RegsRouter = function() {
            this.start = function() {};
            this.navigate = function() {};
            hasPushState = 'false';
        };
    }

    var router = new RegsRouter();
    return router;
});
