define('permalink-view', ['jquery', 'underscore', 'backbone'], function($, _, Backbone) {
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
