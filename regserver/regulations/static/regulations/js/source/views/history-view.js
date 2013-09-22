define('history-view', ['jquery', 'underscore', 'backbone', 'dispatch'], function($, _, Backbone, Dispatch) {
    'use strict';

    var HistoryView = Backbone.View.extend({

        el: '#history',

        events: {
            'click .version-link': 'setStorageItem'
        },

        initialize: function() {
            Dispatch.on('regSection:open:after', this.updateLinks, this);

            // remove the current class from all .status-list items
            $('.status-list').removeClass('current');
            
            // check the data-base-version attribute of each <li> against the document
            this.$el.find('.status-list[data-base-version=' + Dispatch.getVersion() + ']').addClass('current');

            //  History view may not have been initialized before the section was updated;
            //  update the links now.
            this.updateLinks();
        },

        setStorageItem: function() {
            sessionStorage.setItem('drawerDefault', 'history');
        },

        updateLinks: function() {
            var currentSection = Dispatch.getOpenSection();
            this.$el.find('.version-link').each(function() {
                var $link = $(this);
                $link.attr('href', window.APP_PREFIX + currentSection + '/' + $link.data('version'));
            });
        }
    });

    return HistoryView;
});
