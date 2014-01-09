define('header-view', ['jquery', 'underscore', 'backbone', 'sub-head-view'], function($, _, Backbone, SubHead) {
    'use strict';
    var HeaderView = Backbone.View.extend({
        el: '.reg-header',

        initialize: function() {
            this.subHeadView = new SubHead();
        },

        events: {
            'click .mobile-nav-trigger': 'toggleNav'
        },

        toggleNav: function(e) {
            e.preventDefault();

            var $toggleEl = $('.app-nav-list, .mobile-nav-trigger');
            
            $toggleEl.toggleClass('open');
        },

        contextMap: {
            'changeSubHeadText': '_updateSubHead'
        },

        ask: function(message, context) {
            if (typeof this.contextMap[message] !== 'undefined') {
                this.contextMap[message].apply(context);
            }
        },

        // type = wayfinding or search
        // content = new content
        _updateSubHead: function(context) {
            this.subHeadView.change(
                context.type,
                context.content
            );
        }
    });

    var header = new HeaderView();
    return header;
});
