// **Extends** Backbone.View
//
// **Usage** ```require(['sub-head-view'], function(SubHeadView) {})```
//
// **Jurisdiction** The gray subheader above the main content section
define('sub-head-view', ['jquery', 'underscore', 'backbone', 'regs-helpers', 'header-controller'], function($, _, Backbone, RegsHelpers, HeaderEvents) {
    'use strict';
    var SubHeadView = Backbone.View.extend({
        el: '#content-header',

        initialize: function() {
            this.controller = HeaderEvents;

            this.controller.on('section:open', this._changeTitle, this);
            // cache inner title DOM node for frequent reference
            this.$activeTitle = this.$el.find('.header-label');
        },

        // populates subhead with new title
        _changeTitle: function(id) {
            this.$activeTitle.html(RegsHelpers.idToRef(id));
            return this;
        },

        _displayCount: function(resultCount) {
            this.$activeTitle.html('Search results — ' + resultCount);
        },

        _reset: function() {
            this.$activeTitle.html('');
        }
    });

    return SubHeadView;
});
