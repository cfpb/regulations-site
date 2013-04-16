describe("App data", function() {
  var FauxReg, JSONObj;
  
  jasmine.getFixtures().fixturesPath = 'specs/js/fixtures';

  jasmine.getJsonFixtures().set('sample-json.js');
  
  FauxReg = RegsApp.model.set(JSONObj); 

  it("should have an inventory", function() {
    expect(RegsApp.model.inventory).not.toBe(null);
  });

  it("should have an inventory with 3 values", function() {
    expect(RegsApp.model.inventory.length).toEqual(3);
  });

});
