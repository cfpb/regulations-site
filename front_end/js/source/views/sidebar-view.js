define('sidebar-view', ['jquery', 'underscore', 'backbone', 'regs-dispatch', 'sidebar-head-view'], function($, _, Backbone, Dispatch, SidebarHeadView) {
    'use strict';
    var SidebarView = Backbone.View.extend({
        events: {
            'click .expandable': 'toggleMeta'
        },

        initialize: function() {
            Dispatch.on('definition:render', function(el) {
                this.insertChild(el);
            }, this); 

            Dispatch.on('definition:remove', this.clear, this);

            this.header = new SidebarHeadView({el: '#sidebar-subhead'});

            this.contactInfo = this.el.innerHTML.toString();
        },

        render: function() {},

        insertChild: function(el) {
            this.$el.html(el); 
        },

        clear: function() {
            this.$el.html(this.contactInfo);
        },

        toggleMeta: function(e) {
            e.stopPropagation();
            $(e.currentTarget)
                .toggleClass('open')
                .next('.chunk').slideToggle();
        }
    });

    return SidebarView;
});
