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
              "text": "asdfksjflksjdf\n\n"
          } 
        ]
    }

    RegsApp.model.set(this.jsonFixture);
  });

  it("should have json", function() {
    expect(this.jsonFixture).toBeTruthy();
  });

  it("should have an inventory", function() {
    expect(RegsApp.model.inventory).toBeTruthy();
  });

  it("should have an inventory with 3 values", function() {
    expect(RegsApp.model.inventory.length).toEqual( 3 );
  });

  it("should have content", function() {
    expect(RegsApp.model.content).toBeTruthy(); 
  });

  it("should have content for 2345-1-b", function() {
    expect(RegsApp.model.content['2345-1-b'].valueOf()).toEqual("sdlkfjslkdfjskldj");
  });
});
