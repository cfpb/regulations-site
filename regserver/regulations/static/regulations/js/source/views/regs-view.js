// **Extends** Backbone.View
//
// **Usage** ```require(['regs-view'], function(RegsView) { var thing = RegsView.extend({}); })```
//
// should be renamed sidebar-content-view or something
define('regs-view', ['jquery', 'underscore', 'backbone', 'regs-data'], function($, _, Backbone, RegsData) {
    'use strict';
    var RegsView = Backbone.View.extend({
        initialize: function() {
            var field;
            this.model = {};
            // looks like it basically populates the model for this view
            //
            // **TODO** have to remember why or if its even in use anymore
            for (field in this.options) {
                if (this.options.hasOwnProperty(field)) {
                    this.model[field] = this.options[field];
                }
            }

            this.model.content = RegsData.get(this.model.id);
            this.$el.html(this.model.content);

            this.render();

            return this;
        }
    });

    return RegsView;
});
