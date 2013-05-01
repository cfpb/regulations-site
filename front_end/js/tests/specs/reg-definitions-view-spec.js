define(["definition-view", "regs-data", 'samplejson'], function(DefinitionView, RegsData, testjson) {
  describe("Definitions views", function() {
    RegsData.parse(testjson);

    it("test", function() {
      expect(true).toBeTruthy();
    });

  });
});
