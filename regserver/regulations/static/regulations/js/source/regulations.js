// Launches app via RequireJS load
require(['jquery', 'app-init'], function($, app) {
    'use strict';
    $(document).ready(function() {
        app.init();
    });

});
