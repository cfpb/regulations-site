define('child-view', ['underscore', 'backbone'], function(_, Backbone) {
    'use strict';
    var ChildView = Backbone.View.extend({
        initialize: function() {
            var returned, render;

            this.model = this.options.model;

            // callback to be sent to model's get method
            // called after ajax resolves sucessfully
            render = function(returned) {
                this.render(returned, this.options, this.options.cb); 
            }.bind(this);

            if (typeof this.model !== 'undefined') {
                // simplifies to
                // this.model.get()
                returned = this.model.get(this.options.id, render);
            }

            return this;
        },

        render: function(html, options, cb) {
            cb(html, options);
        }
    });

    return ChildView;
});
