define('definition-view', ['jquery', 'underscore', 'backbone', 'sidebar-module-view', 'reg-model', 'regs-helpers', './regs-router', 'main-events', 'sidebar-events', 'ga-events'], function($, _, Backbone, SidebarModuleView, RegModel, Helpers, Router, MainEvents, SidebarEvents, GAEvents) {
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
            'click .close-button': 'close'
        },

        initialize: function() {
            this.externalEvents = SidebarEvents;
            this.externalEvents.on('definition:outOfScope', this.displayScopeMsg, this);
            this.externalEvents.on('definition:inScope', this.removeScopeMsg, this);
            this.externalEvents.on('definition:activate', this.unGrayDefinition, this);
            this.externalEvents.on('definition:deactivate', this.grayOutDefinition, this);

            if (typeof this.options.id !== 'undefined') {
                this.id = this.options.id;
            }

            if (typeof this.options.term !== 'undefined') {
                this.term = this.options.term;
                this.$el.data('defined-term', this.term);
            }

            // insert the spinner header to be replaced
            // by the full def once it loads
            this.renderHeader();

            // for displaying scope warnings
            this.$noticeContainer = this.$el.find('.notice');

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
            GAEvents.trigger('definition:close', {
                type: 'definition',
                by: 'header close button'
            });
            this.remove();
        },

        displayScopeMsg: function(id) {
            var msg = 'This term has a different definition for some portions of ';
            if (id) {
                msg += '§' + id + '.';
            }
            else {
                msg += 'this section.';
            }

            this.$noticeContainer(msg);
        },

        removeScopeMsg: function() {
            if (this.$noticeContainer.length > 0) {
                this.$noticeContainer.html('');
            }
        },

        grayOutDefinition: function(defId) {
            console.log(defId);
            this.$el.addClass('loading');
        },

        unGrayDefinition: function() {
            this.$el.removeClass('loading');
        },

        openFullDefinition: function(e) {
            e.preventDefault();
            var id = this.id || $(e.target).data('linked-section'),
                parentId = Helpers.findBaseSection(id);

            MainEvents.trigger('section:open', parentId, {
                scrollToId: id
            }, 'reg-section'); 

            GAEvents.trigger('definition:followCitation', {
                id: id,
                type: 'definition'
            });
        },

        openInterpretation: function(e) {
            e.preventDefault();
            var $e = $(e.target),
                id = $e.data('linked-section'),
                pid = $e.data('linked-subsection');

            MainEvents.trigger('section:open', id, {
                scrollToId: pid
            });

            GAEvents.trigger('definition:followCitation', {
                id: id,
                type: 'definition'
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
