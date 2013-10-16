// **Extends Backbone.View
//
// **Jurisdiction** .section-nav, regulation section navigation footer
define('section-footer-view', ['jquery', 'underscore', 'backbone', 'dispatch'], function($, _, Backbone, Dispatch) {
    'use strict';

    var SectionFooterView = Backbone.View.extend({
        events: {
            'click .navigation-link': 'sendNavEvent'
        },

        initialize: function() {
            // if the browser doesn't support pushState, don't 
            // trigger click events for links
            if (Dispatch.hasPushState === false) {
                this.events = {};
            }
        },

        sendNavEvent: function(e) {
            e.preventDefault();
            var sectionId = $(e.currentTarget).data('linked-section');

            Dispatch.trigger('ga-event:sectionnav', sectionId);
            Dispatch.trigger('regSection:open', sectionId, {id:sectionId}, 'regSection');
        },

        remove: function() {
            this.stopListening();
            return this;
        }
    });

    return SectionFooterView;
});
