define('regs-router', ['underscore', 'backbone', 'dispatch', 'queryparams'], function(_, Backbone, Dispatch) {
    'use strict';

    var RegsRouter = Backbone.Router.extend({
        routes: {
            'regulation/:section/:version': 'backToSection',
            'search/:reg': 'backToSearchResults'
        },

        backToSection: function(section) {
            Dispatch.trigger('openSection:set', section); 
            Dispatch.trigger('sxs:close');
        },

        backToSearchResults: function(reg, params) {
            var config = {
                query: params.q,
                version: params.version
            };

            if (typeof params.page !== 'undefined') {
                config.page = params.page;
            }

            Dispatch.trigger('searchResults:back', config);
        },

        start:  function() {
            var root = Dispatch.getURLPrefix() || '/';

            Backbone.history.start({
                pushState: 'pushState' in window.history,
                silent: true,
                root: root
            });
        }
    });

    var router = new RegsRouter();
    return router;
});
