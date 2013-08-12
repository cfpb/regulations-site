define(["underscore", "backbone", "jquery", "definition-view", "regs-data", 'samplejson'], function(_, Backbone, $, DefinitionView, RegsData, testjson) {
  describe("Definitions views", function() {
    RegsData.parse(testjson);

    $('body')
        .append('<div id="2345-6-a" data-interp-id="111-2">sdfsd <div class="inline-interpretation"></div></div>')
        .append('<a id="term-link" href="#2345-6-a" data-definition="2345-6-a">sdfds</a>');

    var view = new DefinitionView({
        id: '2345-6-a',
        $anchor: $('#term-link')
    });

    it("should have the view instance", function() {
        expect(view).toBeTruthy();
    });

    it("should store the definition content", function() {
        expect(view.model.content).toEqual("this is where we'd load the api response for 2345-6-a in json format.");
    });

    it("should store the parent link", function() {
        expect(view.model.$anchor).toEqual($('#term-link'));
    });

    it("should be tabbable", function() {
        expect(view.$el.attr('tabindex')).toEqual('0');
    });
  });
});
