// **Extends Backbone.View
//
// **Jurisdiction** .section-nav, regulation section navigation footer
define('section-footer-view', ['jquery', 'underscore', 'backbone', 'dispatch'], function($, _, Backbone, Dispatch) {
    'use strict';

    var SectionFooterView = Backbone.View.extend({
        events: {
            'click .navigation-link': 'sendNavEvent'
        },

        sendNavEvent: function(e) {
            if (window.history && window.history.pushState) {
                e.preventDefault();
                var sectionId = $(e.currentTarget).data('linked-section');
                Dispatch.trigger('regSection:open', sectionId, {id:sectionId}, 'regSection');
            }
        },

        remove: function() {
            this.stopListening();
            return this;
        }
    });

    return SectionFooterView;
});
