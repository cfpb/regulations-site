require(["jquery", "app-init"], function($, startApp) {

    // global state objects
    window.RegsViews = {
        openDefinitions: {},
        openInterpretations: {}
    }; 

    $(document).ready(function() {
        startApp.init();
    });
});
