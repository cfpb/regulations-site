define('ga-events', ['underscore', 'backbone'], function(_, Backbone) {
    'use strict';

    var GAEvents = _.clone(Backbone.Events);

    return GAEvents;
});
