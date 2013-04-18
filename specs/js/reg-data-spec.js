require(['static/js/regs-data'], function(RegsData) {
  describe("App data", function() {
    beforeEach(function() {
      testjson = {
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

      RegsData.parse(testjson);
    });

    it("should have json", function() {
      expect(this.jsonFixture).toBeTruthy();
    });

    it("should have an inventory", function() {
      expect(RegsData.inventory).toBeTruthy();
    });

    it("should have an inventory with 3 values", function() {
      expect(RegsData.inventory.length).toEqual( 3 );
    });

    it("should have content", function() {
      expect(RegsData.content).toBeTruthy(); 
    });

    it("should have content for 2345-1-b", function() {
      expect(RegsData.content['2345-1-b'].valueOf()).toEqual("sdlkfjslkdfjskldj");
    });

    it("should retrieve 2345-1", function() {
      expect(RegsData.retrieve('2345-1')).toEqual("asdfksjflksjdf"); 
    });

    it("should get children", function() {
      var arr = ["2345-1", "2345-1-b", "2345-1-a"];

      expect(RegsData.getChildren('2345')).toEqual(arr);
    });

    it("should not get children", function() {
      expect(RegsData.getChildren('233')).toEqual([]);
    });

    it("should get parent", function() {
      expect(RegsData.getParent('2345-1-b')).toEqual("asdfksjflksjdf");
    });
  });
});
