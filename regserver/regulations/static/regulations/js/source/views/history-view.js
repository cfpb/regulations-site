define('history-view', ['jquery', 'underscore', 'backbone', 'dispatch'], function($, _, Backbone, Dispatch) {
    'use strict';

    var HistoryView = Backbone.View.extend({

        el: '#history',

        events: {
            'click .version-link': 'setStorageItem'
        },

        initialize: function() {
            // remove the current class from all .status-list items
            $('.status-list').removeClass('current');
            
            // check the data-base-version attribute of each <li> against the document
            this.$el.find('.status-list[data-base-version=' + Dispatch.getVersion() + ']').addClass('current');
        },

        setStorageItem: function() {
            sessionStorage.setItem('drawerDefault', 'history');
        }
    });

    return HistoryView;
});
