define('definition-view', ['jquery', 'underscore', 'backbone', 'regs-view', 'regs-data', 'regs-dispatch', 'regs-helpers'], function($, _, Backbone, RegsView, RegsData, Dispatch, RegsHelpers) {
    'use strict';
    var DefinitionView = RegsView.extend({
        className: 'open-definition',
        events: {},

        render: function() {
            Dispatch.once('definition:callRemove', this.remove, this);

            var interp = this.$el.find('.inline-interpretation'),
                dHref = '#' + this.model.id,
                dText = 'Go to definition in § ' + this.model.id,
                classStr = 'continue-link',
                $dLink = RegsHelpers.fastLink(dHref, dText, classStr),
                iHref, iText, $iLink, interpId;

                this.$el.append($dLink);

            if (typeof interp[0] !== 'undefined') {
                interpId = $(interp[0]).data('interpFor');
                this.$el.find('.inline-interpretation').remove();

                iHref = '#' + interpId;
                iText = 'Go to related interpretations';
                $iLink = RegsHelpers.fastLink(iHref, iText, classStr);
                this.$el.append($iLink);
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
