define(['jquery', 'underscore', 'backbone', 'content-view', 'definition-view'], function($, _, Backbone, ContentView, DefinitionView) {
    describe("Content view", function() {
        Dispatch = {
            on: function() {}
        };

        $('body').append('<div id="content"></div>');

        contentView = new ContentView({el: '#content'});

        $link = $('<a href="#123-2" class="definition"></a>');

        contentView.openDefinition('123-2', $link);

        it("should have a content view instance", function() {
            expect(contentView).toBeTruthy();
        });

    });
});
