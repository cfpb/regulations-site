define('main-events', ['underscore', 'backbone'], function(_, Backbone) {
    'use strict';

    var MainEvents = _.clone(Backbone.Events);

    return MainEvents;
});
