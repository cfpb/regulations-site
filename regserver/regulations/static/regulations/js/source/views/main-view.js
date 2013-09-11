define('main-view', ['jquery', 'underscore', 'backbone', 'dispatch'], function($, _, Backbone, Dispatch) {
    'use strict';

    var MainView = Backbone.View.extend({
        el: '#content-wrapper',

        initialize: function() {
            Dispatch.on('mainContent:change', this.render, this);
        },

        render: function(html, elClass) {
            this.el.className = elClass;
            this.$el.html(html);
        }
    });

    return MainView;
});
