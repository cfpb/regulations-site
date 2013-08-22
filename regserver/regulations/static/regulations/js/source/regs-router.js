define('regs-router', ['underscore', 'backbone'], function(_, Backbone) {
    'use strict';

    var RegsRouter = Backbone.Router.extend({});

    var router = new RegsRouter();

    Backbone.history.start({pushState: 'pushState' in window.history, silent: true});

    return router;
});
