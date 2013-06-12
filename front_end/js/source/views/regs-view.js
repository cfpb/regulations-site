define('regs-view', ['jquery', 'underscore', 'backbone', 'regs-data'], function($, _, Backbone, RegsData) {
    'use strict';
    // should be renamed sidebar-content-view or something
    var RegsView = Backbone.View.extend({
        initialize: function() {
            var field;
            this.model = {};
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
