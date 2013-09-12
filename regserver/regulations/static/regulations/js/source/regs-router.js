define('regs-router', ['underscore', 'backbone', './dispatch'], function(_, Backbone, Dispatch) {
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

        backToSearchResults: function() {
            Dispatch.trigger('searchResults:back');
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
