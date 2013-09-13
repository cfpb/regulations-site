define('main-view', ['jquery', 'underscore', 'backbone', 'dispatch'], function($, _, Backbone, Dispatch) {
    'use strict';

    var MainView = Backbone.View.extend({
        el: '#content-wrapper',

        initialize: function() {
            Dispatch.on('mainContent:change', this.render, this);

            Dispatch.on('loading:start', this.loading, this);
            Dispatch.on('loading:finish', this.loaded, this);
        },

        render: function(html, elClass) {
            this.el.className = elClass;
            this.$el.html(html);
        },

        loading: function() {
            // visually indicate that a new section is loading
            $('.main-content').addClass('loading');

        },

        loaded: function() {
            $('.main-content').removeClass('loading');
        }
    });

    return MainView;
});
