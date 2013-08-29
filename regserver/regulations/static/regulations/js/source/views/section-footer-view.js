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
            e.preventDefault();
            var sectionId = $(e.target).data('linked-section');
            Dispatch.trigger('openSection:set', sectionId);
        }
    });

    return SectionFooterView;
});
