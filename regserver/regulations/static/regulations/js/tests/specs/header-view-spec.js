define(['jquery', 'underscore', 'backbone', 'header-view'], function($, _, Backbone, HeaderView) {
    describe("Header view", function() {
        $('body')
            .append('<div id="menu"></div>')
            .append('<div id="menu-link"></div>');

        var header = new HeaderView(),
            eventStub = { preventDefault: new Function() };

        it("should have an initialized instance", function() {
            expect(header).toBeDefined();
        });
        
        it("should add the active class to #menu", function() {
            header.openTOC(eventStub);

            expect($('#menu').hasClass('active')).toBeTruthy();
        });

        it("should add the active class to #menu-link", function() {
            expect($('#menu-link').hasClass('active')).toBeTruthy();
        });

        it("should remove the active class to #menu", function() {
            header.openTOC(eventStub);

            expect($('#menu').hasClass('active')).toBeFalsy();
        });

        it("should remove the active class to #menu-link", function() {
            expect($('#menu-link').hasClass('active')).toBeFalsy();
        });
    }); 
});
