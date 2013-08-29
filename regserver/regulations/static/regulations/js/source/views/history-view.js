define('history-view', ['jquery', 'underscore', 'backbone', 'dispatch'], function($, _, Backbone, Dispatch) {
    'use strict';

    var HistoryView = Backbone.View.extend({

        el: '#history',

       initialize: function() {
            var $statusList = $('.status-list');
            // check the data-base-version attribute of each <li> against the document
            $statusList.each(function() {
                if ($(this).data('base-version') === Dispatch.getVersion()) {
                    $statusList.removeClass('current');
                    // for the matching <li> add a class of 'current'
                    $(this).addClass('current');
                }
            });
        }


    });

    return HistoryView;
});
