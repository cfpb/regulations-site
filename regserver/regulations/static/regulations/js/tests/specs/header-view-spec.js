define(['jquery', 'underscore', 'backbone', 'header-view'], function($, _, Backbone, HeaderView) {
    describe("Header view", function() {
        $('body')
            .append('<div id="menu"></div>')
            .append('<div id="site-header"></div>')
            .append('<a href="#history" id="history-link" class="toc-nav-link">History</a>');

        var headerview = new HeaderView(),
            eventStub;

        eventStub = { 
            preventDefault: new Function(),
            target: document.getElementById('history-link')
        };

        it("should have an initialized instance", function() {
            expect(headerview).to.be.ok();
        });
        
        it("should add the active class to #menu", function() {
            headerview.openDrawer(eventStub);

            expect($('#menu').hasClass('active')).to.be.ok();
        });

        it("should add the active class to #site-headerview", function() {
            expect($('#site-header').hasClass('active')).to.be.ok();
        });

        it("should remove the active class to #menu", function() {
            headerview.openDrawer(eventStub);

            expect($('#menu').hasClass('active')).to.not.be.ok();
        });

        it("should remove the active class to #site-headerview", function() {
            expect($('#site-header').hasClass('active')).to.not.be.ok();
        });

        it("should not have the current class by default", function() {
            expect($('a').hasClass('current')).to.not.be.ok();
        });

        it("should have the current class when clicked", function() {
            headerview.toggleDrawerTab(eventStub);

            expect($('a').hasClass('current')).to.be.ok();
        });
    }); 
});
