define('diff-view', ['jquery', 'underscore', 'backbone', 'main-controller', './regs-router', 'drawer-controller'], function($, _, Backbone, MainEvents, Router, DrawerEvents) {
    'use strict';
    var DiffView = Backbone.View.extend({
        initialize: function() {
            DrawerEvents.trigger('pane:change', 'timeline');
        }
    });

    return DiffView;
});
