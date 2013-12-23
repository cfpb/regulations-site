define('breakaway-events', ['underscore', 'backbone'], function(_, Backbone) {
    'use strict';

    var BreakawayEvents = _.clone(Backbone.Events);

    return BreakawayEvents;
});
