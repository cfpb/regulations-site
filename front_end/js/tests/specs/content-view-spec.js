define(['jquery', 'underscore', 'backbone', 'content-view'], function($, _, Backbone, ContentView) {
    describe("Content view", function() {
        Dispatch = {
            on: function() {}
        };

        $('body').append('<div id="content"></div>');

        contentView = new ContentView({el: '#content'});

        $link = $('<a href="#123-2" class="definition"></a>');

        contentView.create($link, '123-2');

        it("should have a view instance", function() {
            expect(contentView).toBeTruthy();
        });

        it("should open the definition", function() {
            expect(contentView.openDefinition.id).toEqual('123-2');
        });
    });
});
