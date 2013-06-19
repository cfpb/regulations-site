define('definition-view', ['jquery', 'underscore', 'backbone', 'regs-view', 'regs-data', 'regs-dispatch', 'regs-helpers'], function($, _, Backbone, RegsView, RegsData, Dispatch, RegsHelpers) {
    'use strict';
    var DefinitionView = RegsView.extend({
        className: 'open-definition',
        events: {},

        render: function() {
            Dispatch.once('definition:callRemove', this.remove, this);

            var interp = this.$el.find('.inline-interpretation'),
                keyTerm = this.$el.find('dfn.key-term'),
                dHref = '#' + this.model.id,
                dText = '§ ' + this.model.id,
                classStr = 'continue-link internal',
                $dLink = RegsHelpers.fastLink(dHref, dText, classStr),
                clickTerm = this.model.linkText,
                iHref, iText, $iLink, interpId, keyTerms;

                this.$el.append($dLink);

            //  Remove any highlight
            this.$el.find('.active-term').removeClass('active-term');
            //  Add highlight to the clicked term
            this.$el.find('.defined-term').filter(function() {
                return $(this).text().toLowerCase() === clickTerm;
            }).addClass('active-term');



            if (typeof interp[0] !== 'undefined') {
                interpId = $(interp[0]).data('interpFor');
                this.$el.find('.inline-interpretation').remove();

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

            Dispatch.trigger('definition:render', this.$el);

            return this;
        },

        remove: function() {
            this.stopListening();
            this.$el.remove();
            Dispatch.trigger('definition:remove');

            return this;
        }
    });

    return DefinitionView;
});
