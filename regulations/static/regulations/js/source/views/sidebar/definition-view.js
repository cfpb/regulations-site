// **Extends** SidebarModuleView
//
// **TODO** Determine how much sense that still makes ^^
//
// **Usage** ```require(['definition-view'], function(DefinitionView) {})```
//
// A single inline interpretation, child of the sidebar
// As of sprint 6, the only View that is instantiated more than once
define('definition-view', ['jquery', 'underscore', 'backbone', 'sidebar-module-view', 'reg-model', 'regs-helpers', './regs-router', 'main-controller', 'sidebar-controller'], function($, _, Backbone, SidebarModuleView, RegModel, Helpers, Router, MainEvents, SidebarEvents) {
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
            this.controller = SidebarEvents;

            if (typeof this.options.id !== 'undefined') {
                this.id = this.options.id;
            }

            // insert the spinner header to be replaced
            // by the full def once it loads
            this.renderHeader();

            // if pushState is supported, attach the
            // appropriate event handlers
            if (Router.hasPushState) {
                this.events['click .continue-link.interp'] = 'openInterpretation';
                this.events['click .continue-link'] = 'openFullDefinition';
                this.delegateEvents(this.events);
            }
        },

        // temporary header w/spinner while definition is loading
        renderHeader: function() {
            this.$el.html('<div class="sidebar-header group spinner"><h4>Defined Term</h4></div>');
        },

        render: function(html) {
            this.$el.html(html);
        },

        close: function(e) {
            e.preventDefault();
            // return focus to the definition link once the definition is removed
            $('.definition.active').focus();

            MainEvents.trigger('definition:close');
            this.remove();
        },

        openFullDefinition: function(e) {
            e.preventDefault();
            var id = this.id || $(e.target).data('linked-section'),
                parentId = Helpers.findBaseSection(id);

            MainEvents.trigger('section:open', parentId, {
                scrollToId: id
            }, 'reg-section'); 
        },

        openInterpretation: function(e) {
            e.preventDefault();
            var $e = $(e.target),
                id = $e.data('linked-section'),
                pid = $e.data('linked-subsection');

            MainEvents.trigger('section:open', id, {
                scrollToId: pid
            });
        },

        remove: function() {
            this.stopListening();
            this.$el.html('');
            
            return this;
        }
    });

    return DefinitionView;
});
