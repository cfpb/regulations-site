define('definition-view', ['jquery', 'underscore', 'backbone', 'regs-view', 'regs-data', 'regs-dispatch', 'regs-helpers'], function($, _, Backbone, RegsView, RegsData, Dispatch, RegsHelpers) {
    'use strict';
    var DefinitionView = RegsView.extend({
        className: 'open-definition',
        events: {},

        render: function() {
            Dispatch.once('definition:callRemove', this.remove, this);

            var interp = this.$el.find('.inline-interpretation'),
                dfnTerm = this.$el.find('dfn.key-term'),
                dHref = '#' + this.model.id,
                dText = '§ ' + this.model.id,
                classStr = 'continue-link internal',
                $dLink = RegsHelpers.fastLink(dHref, dText, classStr),
                iHref, iText, $iLink, interpId, dfnTerms;

                this.$el.append($dLink);

            if (typeof interp[0] !== 'undefined') {
                interpId = $(interp[0]).data('interpFor');
                this.$el.find('.inline-interpretation').remove();

                iHref = '#' + interpId;
                iText = 'Related commentary';
                $iLink = RegsHelpers.fastLink(iHref, iText, classStr);
                this.$el.append($iLink);
            }

            if (typeof dfnTerm[0] !== 'undefined') {
                dfnTerms = dfnTerm.length;

                for (var i = 0; i < dfnTerms; i++) {
                    $(dfnTerm[i]).remove(); 
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
