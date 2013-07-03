// **Extends** Backbone.View
//
// **Usage** ```require(['sidebar-head-view'], function(SidebarHeadView) {})```
//
// **Jurisdiction** gray background sub-header above right sidebar
define('sidebar-head-view', ['jquery', 'underscore', 'backbone', 'regs-dispatch'], function($, _, Backbone, Dispatch) {
    'use strict';

    var SidebarHeadView = Backbone.View.extend({
        events: {
            'click .close-button': 'close'
        },

        initialize: function() {
            // **Event Listeners** 
            //
            // * when an inline definition is opened, render its header here
            Dispatch.on('definition:render', this.openItem, this);
            
            // * when an inline definition is closed, remove the header
            Dispatch.on('definition:remove', this.clear, this);

            // cache the inner h2 of this el 
            // and the initial text so that we can repopulate on close
            this.header = this.$el.find('h2');
            this.defaultText = this.header.html();
        },

        // Handler for a new sidebar child
        //
        // **TODO** Only really knows how to handle definitions right now
        openItem: function() {
            var closeButton, $closeButton;
            this.header.html('Defined Term');
            
            closeButton = document.createElement('a');
            $closeButton = $(closeButton);
            closeButton.className = 'close-button right';
            closeButton.innerHTML = 'Close definition';
            this.$el.append($closeButton);
        },

        // reset contents
        clear: function() {
            this.$el.html(this.header.html(this.defaultText));
        },

        // if the close "x" is clicked, ask app to set about removing sidebar child
        //
        // **TODO** can only really handle definitions
        close: function() {
            Dispatch.trigger('definition:callRemove');
        }
    });

    return SidebarHeadView;
});
