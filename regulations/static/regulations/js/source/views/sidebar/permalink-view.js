define('permalink-view', ['jquery', 'underscore', 'backbone'], function($, _, Backbone) {
    'use strict';

    var PermalinkView = Backbone.View.extend({
        el: '#permalinks'
    });

    return PermalinkView;
});
