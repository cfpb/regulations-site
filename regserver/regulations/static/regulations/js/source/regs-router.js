define('regs-router', ['underscore', 'backbone', './dispatch'], function(_, Backbone, Dispatch) {
    'use strict';

    var RegsRouter = Backbone.Router.extend({
        routes: {
            'regulation/:section/:version': 'backToSection'
        },

        backToSection: function(section) {
            Dispatch.trigger('openSection:set', section); 
            Dispatch.trigger('sxs:close');
        }
    });

    var router = new RegsRouter(),
        root = Dispatch.getURLPrefix() || '/';

    Backbone.history.start({
        pushState: 'pushState' in window.history,
        silent: true,
        root: root
    });

    return router;
});
