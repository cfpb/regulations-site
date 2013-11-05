define('permalink-view', ['jquery', 'underscore', 'backbone', 'dispatch'], function($, _, Backbone, Dispatch) {
    'use strict';

    var PermalinkView = Backbone.View.extend({
        el: '#permalinks',

        initialize: function() {
            Dispatch.on('sidebar:update', this.update, this);
        },

        update: function(html) {
            this.$el.html(html);
        }
    });

    return PermalinkView;
});
