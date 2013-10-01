define(["underscore", "backbone", "jquery", "definition-view", "reg-model", 'samplejson', 'dispatch'], function(_, Backbone, $, DefinitionView, RegModel, testjson, Dispatch) {
  describe("Definitions views", function() {
    RegModel.parse(testjson);

    $('body')
        .append('<div id="2345-6-a" data-interp-id="111-2">sdfsd <div class="inline-interpretation"></div></div>')
        .append('<a id="term-link" href="#2345-6-a" data-definition="2345-6-a">sdfds</a>');

    var view = new DefinitionView({
        id: '2345-6-a',
        $anchor: $('#term-link')
    });

    it("should have the view instance", function() {
        expect(view).to.be.ok();
    });

    it("should store the definition content", function() {
        expect(view.model.content).to.be("definition body");
    });

    it("should store the parent link", function() {
//        expect(view.model.$anchor).to.be($('#term-link'));
    });

    it("should be tabbable", function() {
        expect(view.$el.attr('tabindex')).to.be('0');
    });
  });
});
