define('header-view', ['jquery', 'underscore', 'backbone', 'regs-dispatch'], function($, _, Backbone, Dispatch) {
    var HeaderView = Backbone.View.extend({
        el: '.main-head',

        initialize: function() {
            this.$activeEls = $('#menu, #menu-link');
        },

        events: {
            'click .toc-toggle': 'openTOC'
        },

        openTOC: function(e) {
            e.preventDefault();
            if (typeof this.$activeEls !== 'undefined') {
                this.$activeEls.toggleClass('active');
            }
        }
    });

    return HeaderView;
});
