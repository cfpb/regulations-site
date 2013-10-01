define(['jquery', 'underscore', 'backbone', 'drawer-view'], function($, _, Backbone, DrawerView) {
    describe("Drawer view", function() {
        var drawerView = new DrawerView(),
            drawerView2; 

        it("should default to having the TOC active", function() {
            expect(drawerView.childViews['table-of-contents'].view).to.be.ok();
        });

        it("should hide all drawer panes besides TOC", function() {
            $('.toc-container:not(#table-of-contents)').each(function(el) {
                expect($(el).hasClass('hidden')).to.be.ok();
            });
        });

        it("should hide all drawer panes besides history", function() {
            $('.toc-container:not(#history)').each(function(el) {
                expect($(el).hasClass('hidden')).to.be.ok();
            });
        });
    });
});

