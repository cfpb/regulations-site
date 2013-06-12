define(['jquery', 'underscore', 'backbone', 'content-view', 'definition-view'], function($, _, Backbone, ContentView, DefinitionView) {
    describe("Content view", function() {
        Dispatch = {
            on: function() {}
        };

        $('body').append('<div id="content"></div>');

        contentView = new ContentView({el: '#content'});

        $link = $('<a href="#123-2" class="definition"></a>');

        contentView.storeDefinition($link, '123-2');

        it("should have a content view instance", function() {
            expect(contentView).toBeTruthy();
        });

        it("should have the def id stored", function() {
            expect(contentView.openDefinition.id).toEqual('123-2');
        });

        it("should have a def view instance stored", function() {
            expect(contentView.openDefinition.view.cid).toBeDefined();
            expect(contentView.openDefinition.view.$el).toBeDefined();
        });

        it("should have the associated model", function() {
            expect(contentView.openDefinition.view.model.id).toEqual("123-2");
        });

        it("should teardown the definition", function() {
            contentView.openDefinition.view.remove();

            expect(contentView.openDefinition.view).toBeUndefined();
            expect(contentView.openDefinition.id).toBeUndefined();
            expect(contentView.openDefinition.link).toBeUndefined();
        });
    });
});
