define('regs-router', ['underscore', 'backbone', './dispatch'], function(_, Backbone, Dispatch) {
    'use strict';

    var RegsRouter = Backbone.Router.extend({
        routes: {
            'regulation/:section/:version': 'backToSection'
        },

        backToSection: function(section) {
           Dispatch.trigger('openSection:set', section); 
        }
    });

    var router = new RegsRouter();

    Backbone.history.start({pushState: 'pushState' in window.history, silent: true});

    return router;
});
