define(["underscore", "backbone", "jquery", "definition-view", "regs-data", 'samplejson'], function(_, Backbone, $, DefinitionView, RegsData, testjson) {
  describe("Definitions views", function() {
    RegsData.parse(testjson);

    $('body')
        .append('<div id="2345-6-a">sdfsd</div>')
        .append('<a id="2345-4">sdfds</a>');

    var view = new DefinitionView({
        id: '2345-6-a',
        $anchor: $('#2345-4')
    });

    it("should have the view instance", function() {
        expect(view).toBeTruthy();
    });

    it("should store the definition content", function() {
        expect(view.model.content).toEqual("this is where we'd load the api response for 2345-6-a in json format.");
    });

    it("should store the parent link", function() {
        expect(view.model.$anchor).toEqual($('#2345-4'));
    });

    it("should tell the state obj that its open", function() {
        expect
    });
    
  });
});
