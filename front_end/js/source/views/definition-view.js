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

        render: function() {
            var interp = this.$el.find('.inline-interpretation'),
                keyTerm = this.$el.find('dfn.key-term'),
                dHref = '#' + this.model.id,
                dText = RegsHelpers.idToRef(this.model.id),
                classStr = 'continue-link internal',
                $dLink = RegsHelpers.fastLink(dHref, dText, classStr),
                clickTerm = this.model.linkText,
                iHref, iText, $iLink, interpId, keyTerms;

                this.$el.append($dLink);

            //  Add highlight to the clicked term
            this.$el.find('.defined-term').filter(function() {
                return $(this).text().toLowerCase() === clickTerm;
            }).addClass('active-term');

            if (typeof interp[0] !== 'undefined') {
                interpId = $('#' + this.model.id).data('interpId');
                interp.remove();

                iHref = '#' + interpId;
                iText = 'Related commentary';
                $iLink = RegsHelpers.fastLink(iHref, iText, classStr);
                this.$el.append($iLink);
            }

            if (typeof keyTerm[0] !== 'undefined') {
                keyTerms = keyTerm.length;

                for (var i = 0; i < keyTerms; i++) {
                    $(keyTerm[i]).remove(); 
                }
            }

            this.$el.attr('tabindex', '0').append('<a class="close-button" href="#">Close definition</a>');

            // **Event trigger** triggers definition open event
            Dispatch.trigger('definition:render', this.$el);
            this.$el.focus();

            return this;
        },

        close: function(e) {
            e.preventDefault();
            // **Event trigger** asks for definition to be closed
            // **TODO** architectural complexity required an additional close event be created
            // to prevent cyclical event
            Dispatch.trigger('definition:callRemove');
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
