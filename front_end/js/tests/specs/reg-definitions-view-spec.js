define(["underscore", "backbone", "jquery", "definition-view", "regs-data", 'samplejson'], function(_, Backbone, $, DefinitionView, RegsData, testjson) {
  describe("Definitions views", function() {
    RegsData.parse(testjson);

    $('body')
        .append('<div id="2345-9-a">sdfsd</div>')
        .append('<a id="2345-4">sdfds</a>');

    var view = new DefinitionView({
        termId: '2345-9-a',
        termLink: document.getElementById("2345-4")
    });

    it("should have the view instance"), function() {
        expect(view).toBeTruthy();
    };

    it("should store the definition content"), function() {
        expect(view.get('content')).toEqual('sdfsd');
    };

    it("should store the parent link"), function() {
        expect(view.get('$termLink').toEqual($('#2345-4')));
    };
    
  });
});
