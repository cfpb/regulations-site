define(["underscore", "backbone", "jquery", "regulations", "regs-state", "interpretation-view", "regs-data", 'samplejson'], function(_, Backbone, $, RegsApp, RegsState, InterpretationView, RegsData, testjson) {
  describe("Interpretation views", function() {
    RegsData.parse(testjson);

    $('body')
        .append('<div id="I-2345-10">sdfsd</div>')
        .append('<li id="2345-10"><a href="I-2345-10" class="interpretation-ref">sdfds</a></li>');

    it("should have an initialized view", function() {
        $('.interpretation-ref').click();   

        expect(RegsState.openInterps['I-2345-10']).toBeTruthy();
    });
  });
});
