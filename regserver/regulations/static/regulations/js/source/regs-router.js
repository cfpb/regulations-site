define('regs-router', ['underscore', 'backbone'], function(_, Backbone) {
    'use strict';

    var RegsRouter = Backbone.Router.extend({});

    var router = new RegsRouter();

    Backbone.history.start({pushState: true, silent: true});

    return router;
});
