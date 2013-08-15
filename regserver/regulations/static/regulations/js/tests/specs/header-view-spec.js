define(['jquery', 'underscore', 'backbone', 'header-view'], function($, _, Backbone, HeaderView) {
    describe("Header view", function() {
        $('body')
            .append('<div id="menu"></div>')
            .append('<div id="site-header"></div>')
            .append('<a href="#history" id="history-link" class="toc-nav-link">History</a>');

        var header = new HeaderView(),
            eventStub = { preventDefault: new Function() };

        it("should have an initialized instance", function() {
            expect(header).toBeDefined();
        });
        
        it("should add the active class to #menu", function() {
            header.openTOC(eventStub);

            expect($('#menu').hasClass('active')).toBeTruthy();
        });

        it("should add the active class to #site-header", function() {
            expect($('#site-header').hasClass('active')).toBeTruthy();
        });

        it("should remove the active class to #menu", function() {
            header.openTOC(eventStub);

            expect($('#menu').hasClass('active')).toBeFalsy();
        });

        it("should remove the active class to #site-header", function() {
            expect($('#site-header').hasClass('active')).toBeFalsy();
        });

        it("should not have the current class by default", function() {
            expect($('a').hasClass('current')).toBeFalsy();
        });

        it("should have the current class when clicked", function() {
            // test for the current class
        });
    }); 
});
