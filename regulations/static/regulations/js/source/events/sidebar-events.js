define('sidebar-events', ['underscore', 'backbone'], function(_, Backbone) {
    'use strict';

    var SidebarEvents = _.clone(Backbone.Events);

    return SidebarEvents;
});
