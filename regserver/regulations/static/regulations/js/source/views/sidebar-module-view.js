// **Extends** Backbone.View
//
// **Usage** ```require(['sidebar-module-view'], function(SidebarModuleView) { var thing = SidebarModuleView.extend({}); })```
define('sidebar-module-view', ['jquery', 'underscore', 'backbone', 'reg-model'], function($, _, Backbone, RegModel) {
    'use strict';
    var SidebarModuleView = Backbone.View.extend({
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

            this.model.content = RegModel.get(this.model.id);
            this.$el.html(this.model.content);

            this.render();

            return this;
        }
    });

    return SidebarModuleView;
});
