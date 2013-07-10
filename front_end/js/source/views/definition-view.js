// **Extends** RegsView
//
// **TODO** Determine how much sense that still makes ^^
//
// **Usage** ```require(['definition-view'], function(DefinitionView) {})```
//
// A single inline interpretation, child of the sidebar
// As of sprint 6, the only View that is instantiated more than once
define('definition-view', ['jquery', 'underscore', 'backbone', 'regs-view', 'regs-data', 'regs-dispatch', 'regs-helpers'], function($, _, Backbone, RegsView, RegsData, Dispatch, RegsHelpers) {
    'use strict';

    // **Constructor**
    // this.options:
    // 
    // * **id** string, dash-delimited id of definition paragraph
    // * **$anchor** jQobj, the content-view link that opened the def
    //
    // this.options turns into this.model
    var DefinitionView = RegsView.extend({
        className: 'open-definition',
        events: {
            'click .close-button': 'close'
        },

        formatInterpretations: function() {
            var interpretation = this.$el.find('.inline-interpretation'),
                interpretationId;

            if (typeof interpretation[0] !== 'undefined') {
                interpretationId = $('#' + this.model.id).data('interpId');
                interpretation.remove();

                this.$el.append(
                    RegsHelpers.fastLink(
                        '#' + interpretationId, 
                        'Related commentary', 
                        'continue-link internal interp'
                    )
                );
            }
        },

        removeHeadings: function() {
            var keyTerm = this.$el.find('dfn.key-term'),
                keyTerms;

            if (typeof keyTerm[0] !== 'undefined') {
                keyTerms = keyTerm.length;

                for (var i = 0; i < keyTerms; i++) {
                    $(keyTerm[i]).remove(); 
                }
            }
        },

        render: function() {
            // link to definition in content body
            this.$el.append(
                RegsHelpers.fastLink(
                    '#' + this.model.id, 
                    RegsHelpers.idToRef(this.model.id),
                    'continue-link internal'
                )
            );

            // remove inline interpretation, add interpretation link
            this.formatInterpretations();
            this.removeHeadings();

            // make definition tabbable
            this.$el.attr('tabindex', '0')
                // make tab-activeated close button at bottom of definition content
                .append('<a class="close-button" href="#">Close definition</a>');

            // **Event trigger** triggers definition open event
            Dispatch.trigger('definition:render', this.$el);

            // set focus to the open definition
            this.$el.focus();
            return this;
        },

        close: function(e) {
            e.preventDefault();
            Dispatch.remove('definition');
        },

        remove: function() {
            this.stopListening();
            this.$el.remove();
            // **Event trigger** notifies app that definition is removed
            Dispatch.trigger('definition:remove', this.model.id);

            return this;
        }
    });

    return DefinitionView;
});
