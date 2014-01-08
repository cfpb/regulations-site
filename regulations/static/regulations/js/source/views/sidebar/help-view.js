define('help-view', ['jquery', 'underscore', 'backbone'], function($, _, Backbone) {
    'use strict';

    var HelpView = Backbone.View.extend({
        el: '#help'
    });

    return HelpView;
});
