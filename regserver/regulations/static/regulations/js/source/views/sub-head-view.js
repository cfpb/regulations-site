// **Extends** Backbone.View
//
// **Usage** ```require(['sub-head-view'], function(SubHeadView) {})```
//
// **Jurisdiction** The gray subheader above the main content section
define('sub-head-view', ['jquery', 'underscore', 'backbone', 'regs-dispatch', 'regs-helpers'], function($, _, Backbone, Dispatch, RegsHelpers) {
    'use strict';
    var SubHeadView = Backbone.View.extend({
        el: '#content-header',

        initialize: function() {
            // **Event listeners**
            // when the active section changes, change the contents of the header
            Dispatch.on('activeSection:change', this.changeTitle, this);

            // cache inner title DOM node for frequent reference
            this.$activeTitle = this.$el.find('#active-title');
        },

        // populates subhead with new title
        changeTitle: function(id) {
            this.$activeTitle.html('<em class="header-label">' + RegsHelpers.idToRef(id) + '</em>');

            return this;
        }
    });

    return SubHeadView;
});
