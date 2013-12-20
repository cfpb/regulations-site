define('history-view', ['jquery', 'underscore', 'backbone', 'main-events'], function($, _, Backbone, MainEvents) {
    'use strict';

    var HistoryView = Backbone.View.extend({

        el: '#timeline',

        events: {
            'click .version-link': 'setStorageItem'
        },

        initialize: function() {
            MainEvents.on('section:open', this.updateLinks, this);
            MainEvents.on('diff:open', this.updateLinks, this);
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
                this.$el.find('.version-link, .stop-button').each(function() {
                    var $link = $(this);
                    $link.attr('href', prefix + section + '/' + $link.data('version'));
                });

                // update diff dropdown
                this.$el.find('.select-content form').each(function() {
                    var $form = $(this),
                        actionParts;
                    
                    // form action = diff_redirect/section/version
                    actionParts = _.compact($form.attr('action').split('/'));
                    $form.attr('action', '/' + actionParts[0] + '/' + section + '/' + actionParts[2]);
                });
            }
        }
    });

    return HistoryView;
});
