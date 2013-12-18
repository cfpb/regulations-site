define('sidebar-head-view', ['jquery', 'underscore', 'backbone'], function($, _, Backbone) {
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

            // cache the actual header tag
            this.$header = this.$el.find('h2');
        },

        // Handler for a new sidebar child
        //
        // **TODO** Only really knows how to handle definitions right now
        openItem: function() {
            var closeButton, $closeButton;
            this.$header.html('Defined Term');
            
            closeButton = document.createElement('a');
            $closeButton = $(closeButton);
            closeButton.className = 'close-button right';
            closeButton.innerHTML = 'Close definition';
            this.$el.append($closeButton);
        },

        // reset contents
        clear: function() {
            this.$el.html(this.$header.html(''));
        },

        // if the close "x" is clicked, ask app to set about removing sidebar child
        //
        // **TODO** can only really handle definitions
        close: function() {
            Dispatch.remove('definition');
            Dispatch.trigger('ga-event:definition', 'close by header button');
        }
    });

    return SidebarHeadView;
});
