define('main-view', ['jquery', 'underscore', 'backbone', 'dispatch', './reg-view'], function($, _, Backbone, Dispatch, RegView) {
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
