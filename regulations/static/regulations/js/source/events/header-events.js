define('header-events', ['underscore', 'backbone'], function(_, Backbone) {
    'use strict';

    var HeaderEvents = _.clone(Backbone.Events);

    return HeaderEvents;
});
