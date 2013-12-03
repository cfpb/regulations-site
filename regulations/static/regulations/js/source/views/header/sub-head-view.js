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
            // cache inner title DOM node for frequent reference
            this.$activeTitle = this.$el.find('.header-label');
        },

        contextMap: {
            'wayfinding': '_changeTitle',
            'search': '_displayCount'
        },

        change: function(type, content) {
            if (typeof this.contextMap[type] !== 'undefined') {
                this.contextMap[type](content);
            }
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
