describe("App data", function() {
  beforeEach(function() {
    this.jsonFixture = {
       "children": [
          {
              "children": [
                  {
                      "children": [], 
                      "label": {
                          "parts": [
                              "2345", 
                              "1", 
                              "a"
                          ], 
                          "text": "2345-1-a"
                      }, 
                      "text": "sdflkjsdklfjsd"
                  }, 
                  {
                      "children": [], 
                      "label": {
                          "parts": [
                              "2345", 
                              "1", 
                              "b"
                          ], 
                          "text": "2345-1-b"
                      }, 
                      "text": "sdlkfjslkdfjskldj"
                  }
              ], 
              "label": {
                  "parts": [
                      "2345", 
                      "1"
                  ], 
                  "text": "2345-1", 
                  "title": "2345.1 asdlkfjasldkfj"
              }, 
              "text": "asdfksjflksjdf"
          } 
        ]
    }

    Regs.data.parse(this.jsonFixture);
  });

  it("should have json", function() {
    expect(this.jsonFixture).toBeTruthy();
  });

  it("should have an inventory", function() {
    expect(Regs.data.inventory).toBeTruthy();
  });

  it("should have an inventory with 3 values", function() {
    expect(Regs.data.inventory.length).toEqual( 3 );
  });

  it("should have content", function() {
    expect(Regs.data.content).toBeTruthy(); 
  });

  it("should have content for 2345-1-b", function() {
    expect(Regs.data.content['2345-1-b'].valueOf()).toEqual("sdlkfjslkdfjskldj");
  });

  it("should retrieve 2345-1", function() {
    expect(Regs.data.retrieve('2345-1')).toEqual("asdfksjflksjdf"); 
  });

  it("should get children", function() {
    var arr = ["2345-1", "2345-1-b", "2345-1-a"];

    expect(Regs.data.getChildren('2345')).toEqual(arr);
  });

  it("should not get children", function() {
    expect(Regs.data.getChildren('233')).toEqual([]);
  });

  it("should get parent", function() {
    expect(Regs.data.getParent('2345-1-b')).toEqual("asdfksjflksjdf");
  });
});
