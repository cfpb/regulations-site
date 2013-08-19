// **Extends Backbone.View
//
// **Jurisdiction** .section-nav, regulation section navigation footer
define('section-footer-view', ['jquery', 'underscore', 'backbone', 'regs-dispatch'], function($, _, Backbone, Dispatch) {
    'use strict';

    var SectionFooterView = Backbone.View.extend({
        events: {
            'click .navigation-link': 'sendNavEvent'
        },

        sendNavEvent: function(e) {
            e.preventDefault();
            Dispatch.trigger('openSection:set', $(e.target).data('linked-section'));
        }
    });

    return SectionFooterView;
});
