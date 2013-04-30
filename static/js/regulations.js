require(["jquery", "app-init"], function($, startApp) {

    // global state objects
    window.RegsViews = {
        openDefinitions: {}
    }; 

    $(document).ready(function() {
        // template stub
        var template = function(b, p) {
            $('#' + p).append(b);
        };

        startApp();
    });
});
