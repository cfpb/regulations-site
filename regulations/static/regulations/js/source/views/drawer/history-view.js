define('history-view', ['jquery', 'underscore', 'backbone', 'main-events'], function($, _, Backbone, MainEvents) {
    'use strict';

    var HistoryView = Backbone.View.extend({

        el: '#timeline:not(.diff-history)',

        events: {
            'click .version-link': 'setStorageItem'
        },

        initialize: function() {
            var currentVersion = $('section[data-base-version]').data('base-version');

            MainEvents.on('section:open', this.updateLinks, this);

            // remove the current class from all .status-list items
            this.$el.find('.status-list').removeClass('current');

            // check the data-base-version attribute of each <li> against the document
            this.$el.find('.status-list[data-base-version=' + currentVersion + ']').addClass('current');

            //  History view may not have been initialized before the section was updated;
            //  update the links now.
            this.updateLinks();
        },

        setStorageItem: function() {
            sessionStorage.setItem('drawerDefault', 'timeline');
        },

        updateLinks: function(section) {
            var prefix = window.APP_PREFIX;
            if (typeof prefix !== 'undefined' && prefix.substr(prefix.length - 1) !== '/') {
                prefix = prefix + '/';
            }
            // section may not be defined (e.g. on the landing page)
            if (typeof section !== 'undefined') {
                this.$el.find('.version-link').each(function() {
                    var $link = $(this);
                    $link.attr('href', prefix + section + '/' + $link.data('version'));
                });
            }
        }
    });

    return HistoryView;
});
