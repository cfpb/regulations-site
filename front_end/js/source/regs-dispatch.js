// **Extends** Backbone.Events
//
// **Usage** require(['regs-dispatch'], function(Dispatch) {}))
define('regs-dispatch', ['jquery', 'underscore', 'backbone'], function($, _, Backbone) {
    'use strict';
    return _.extend({
        open: {},

        set: function(key, val) {
            this.open[key] = val;
        },

        remove: function(key) {
            if (this.open[key]) {
                this.open[key].remove();
                delete(this.open[key]);
            }
        },

        getViewId: function(type) {
            if (typeof this.open[type] === 'object') {
                return this.open[type].model.id;
            }
            return false;
        }

    }, Backbone.Events);   
});
