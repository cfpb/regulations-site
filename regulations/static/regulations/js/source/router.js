define('regs-router', ['underscore', 'backbone', 'main-events', 'breakaway-events', 'queryparams'], function(_, Backbone, MainEvents, BreakawayEvents) {
    'use strict';

    var RegsRouter;

    if (typeof window.history.pushState === 'undefined') {
        RegsRouter = function() {
            this.start = function() {};
            this.navigate = function() {};
            this.hasPushState = false;
        };
    }
    else {
        RegsRouter = Backbone.Router.extend({
            routes: {
                'sxs/:section/:version': 'loadSxS',
                'search/:reg': 'loadSearchResults',
                'diff/:section/:baseVersion/:newerVersion': 'loadDiffSection',
                ':section/:version': 'loadSection'
            },

            loadSection: function(section) {
                var options = {id: section};

                // to scroll to paragraph if there is a hadh
                options.scrollToId = Backbone.history.getHash();

                // ask the view not to route, its not needed
                options.noRoute = true;

                MainEvents.trigger('section:open', section, options, 'reg-section'); 
            },

            loadDiffSection: function(section, baseVersion, newerVersion, params) {
                var options = {};

                options.id = section;
                options.baseVersion = baseVersion;
                options.newerVersion = newerVersion;
                options.noRoute = true;
                options.fromVersion = params.from_version;

                MainEvents.trigger('diff:open', section, options, 'diff');
            },

            loadSxS: function(section, version, params) {
                /* jshint camelcase: false */
                BreakawayEvents.trigger('sxs:open', {
                    'regParagraph': section,
                    'docNumber': version,
                    'fromVersion': params.from_version
                });
            },

            loadSearchResults: function(reg, params) {
                /* jshint unused: false */
                var config = {
                    query: params.q,
                    regVersion: params.regVersion
                };

                // if there is a page number for the query string
                if (typeof params.page !== 'undefined') {
                    config.page = params.page;
                }

                MainEvents.trigger('search-results:open', null, config, 'search-results');
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

            hasPushState: true
        });
    }

    var router = new RegsRouter();
    return router;
});
