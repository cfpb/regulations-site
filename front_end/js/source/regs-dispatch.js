// **Extends** Backbone.Events
//
// **Usage** require(['regs-dispatch'], function(Dispatch) {}))
define('regs-dispatch', ['jquery', 'underscore', 'backbone'], function($, _, Backbone) {
    'use strict';
    return _.extend({}, Backbone.Events);   
});
