define('main-view', ['jquery', 'underscore', 'backbone', 'dispatch', './reg-view'], function($, _, Backbone, Dispatch, RegView) {
    'use strict';

    var MainView = Backbone.View.extend({
        el: '.main-content',

        initialize: function() {
            this.setState();            

            if (this.state === 'regulation') {
                this.child = new RegView();
            }

            Dispatch.on('mainContent:change', this.render, this);
        },

        render: function(html) {
            this.$el.html(html);
        },

        setState: function() {
            var path = _.compact(window.location.pathname.split('/'));
            this.state = path[0];
        }
    });

    return MainView;
});
