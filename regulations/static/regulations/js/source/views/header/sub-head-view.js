define('sub-head-view', ['jquery', 'underscore', 'backbone', 'regs-helpers', 'header-events'], function($, _, Backbone, RegsHelpers, HeaderEvents) {
    'use strict';
    var SubHeadView = Backbone.View.extend({
        el: '#content-header',

        initialize: function() {
            this.externalEvents = HeaderEvents;

            this.externalEvents.on('section:open', this._changeTitle, this);
            this.externalEvents.on('search-results:open', this._displayCount, this);
            this.externalEvents.on('clear', this._reset, this);

            // cache inner title DOM node for frequent reference
            this.$activeTitle = this.$el.find('.header-label');
        },

        // populates subhead with new title
        _changeTitle: function(id) {
            this.$activeTitle.html(RegsHelpers.idToRef(id));
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
