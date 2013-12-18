define('drawer-events', ['underscore', 'backbone'], function(_, Backbone) {
    'use strict';

    var DrawerEvents = _.clone(Backbone.Events);

    return DrawerEvents;
});
