// **Extends** Backbone.View
//
// **Usage** ```require(['sidebar-view'], function(SidebarView) {})```
//
// **Jurisdiction** Right sidebar
define('sidebar-view', ['jquery', 'underscore', 'backbone', 'regs-dispatch', 'sidebar-head-view'], function($, _, Backbone, Dispatch, SidebarHeadView) {
    'use strict';
    var SidebarView = Backbone.View.extend({
        events: {
            'click .expandable': 'toggleMeta'
        },

        initialize: function() {
            // **Event Listeners**
            // when a new inline definition is opened, populate the sidebar with it
            Dispatch.on('definition:render', function(el) {
                this.insertChild(el);
            }, this); 

            // When an inline definition is closed, reset sidebar content
            Dispatch.on('definition:remove', this.clear, this);

            // Init a sidebar header instance
            this.header = new SidebarHeadView({el: '#sidebar-subhead'});

            // cache default content for replacement in the future
            this.contactInfo = this.el.innerHTML.toString();
        },

        render: function() {},

        // open whatever content should populate the sidebar
        insertChild: function(el) {
            this.$el.html(el); 
        },

        // resets content of the sidebar
        clear: function() {
            this.$el.html(this.contactInfo);
        },

        // expands the meta info content drop downs
        toggleMeta: function(e) {
            e.stopPropagation();
            $(e.currentTarget)
                .toggleClass('open')
                .next('.chunk').slideToggle();
        }
    });

    return SidebarView;
});
