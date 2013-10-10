define(['jquery', 'underscore', 'backbone', 'dispatch'], function($, _, Backbone, Dispatch) {
    describe("Dispatch", function() {
        it("should house view instances that need to be accessed cross-module", function() {
            var view = {id: 3};
            Dispatch.set('definition', view);

            expect(Dispatch.open.definition).to.be(view);
        });

        it("should call the remove method of stored items on remove", function() {
            var thing = {remove: function() { VAL = 'yes' }}; 
            Dispatch.set('thing', thing);
            Dispatch.remove('thing');

            expect(VAL).to.be('yes');
        });

        it("should remove cached object", function() {
            expect(Dispatch.open.thing).to.not.be.ok();
        });

        it("should return the id of view objects", function() {
            var id = Dispatch.getViewId('definition');

            expect(id).to.be(3);
        });
    });
});
