// **Extends** SidebarModuleView
//
// **TODO** Determine how much sense that still makes ^^
//
// **Usage** ```require(['definition-view'], function(DefinitionView) {})```
//
// A single inline interpretation, child of the sidebar
// As of sprint 6, the only View that is instantiated more than once
define('definition-view', ['jquery', 'underscore', 'backbone', 'sidebar-module-view', 'reg-model', 'regs-helpers', './regs-router'], function($, _, Backbone, SidebarModuleView, RegModel, Helpers, Router) {
    'use strict';

    // **Constructor**
    // this.options:
    // 
    // * **id** string, dash-delimited id of definition paragraph
    // * **$anchor** jQobj, the reg-view link that opened the def
    //
    // this.options turns into this.model
    var DefinitionView = SidebarModuleView.extend({
        el: '#definition',

        events: {
            'click .close-button': 'close',
        },

        initialize: function() {
            if (typeof this.options.id !== 'undefined') {
                this.id = this.options.id;
            }

            if (typeof this.options.id !== 'undefined') {
                this.render(this.options.html);
            }

            // if pushState is supported, attach the
            // appropriate event handlers
            if (Router.hasPushState) {
                this.events['click .definition'] = 'sendDefinitionLinkEvent';
                this.events['click .continue-link'] = 'sendContinueLinkEvent';
                this.delegateEvents(this.events);
            }
        },

        render: function(html) {
            this.$el.html(html);
        },

        close: function(e) {
            e.preventDefault();
            // return focus to the definition link once the definition is removed
            $('.definition.active').focus();

            MainEvents.trigger('definition:close');
        },

        remove: function() {
            this.stopListening();
            this.$el.remove();
            
            return this;
        }
    });

    return DefinitionView;
});
