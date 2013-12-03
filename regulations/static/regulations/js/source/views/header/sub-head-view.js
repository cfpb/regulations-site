// **Extends** Backbone.View
//
// **Usage** ```require(['sub-head-view'], function(SubHeadView) {})```
//
// **Jurisdiction** The gray subheader above the main content section
define('sub-head-view', ['jquery', 'underscore', 'backbone', 'regs-helpers'], function($, _, Backbone, RegsHelpers) {
    'use strict';
    var SubHeadView = Backbone.View.extend({
        el: '#content-header',

        initialize: function() {
            // **Event listeners**
            // when the active section changes, change the contents of the header
            Dispatch.on('activeSection:change', this.changeTitle, this);
            Dispatch.on('searchResults:open', this.displayCount, this);

            // cache inner title DOM node for frequent reference
            this.$activeTitle = this.$el.find('.header-label');
        },

        // populates subhead with new title
        changeTitle: function(id) {
            this.$activeTitle.html(RegsHelpers.idToRef(id));
            return this;
        },

        displayCount: function(resultCount) {
            this.$activeTitle.html('Search results — ' + resultCount);
        },

        reset: function() {
            this.$activeTitle.html('');
        }
    });

    return SubHeadView;
});
