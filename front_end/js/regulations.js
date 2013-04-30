require(["jquery", "app-init"], function($, startApp) {

    // global state objects
    window.RegsViews = {
        openDefinitions: {}
    }; 

    $(document).ready(function() {
        startApp.init();
    });
});
