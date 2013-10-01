define(['reg-model', 'samplejson'], function(RegModel, testjson) {
  describe("RegModel module", function() {
    RegModel.parse(testjson);

    it("should have a structure array", function() {
      expect(RegModel.structure).to.be.ok();
    });

    it("should have a structure array with 9 values", function() {
      expect(RegModel.structure.length).to.be( 9 );
    });

    it("should have content", function() {
      expect(RegModel.content).to.be.ok(); 
    });

    it("should have content for 2345-9-a", function() {
      var content = "<p><dfn>placerat in egestas.</dfn> Sed erat enim, hendrerit mollis tempus et, consequat et ante. Donec imperdiet orci eget nisi lobortis molestie. Nullam pellentesque scelerisque hendrerit</p>";
      expect(RegModel.content['2345-9-a'].valueOf()).to.be(content);
    });

    it("should get 2345-9", function() {
      expect(RegModel.get('2345-9')).to.be("asdfksjflksjdf"); 
    });

    it("should get children", function() {
      var arr = ["2345-9-a-2", "2345-9-a-1"];

      expect(RegModel.getChildren('2345-9-a')).to.be(arr);
    });

    it("should not get children", function() {
      expect(RegModel.getChildren('233')).to.be([]);
    });

    it("should get parent", function() {
      expect(RegModel.getParent('2345-9-b')).to.be("asdfksjflksjdf");
    });

    it("should differentiate between structure presence and being loaded", function() {
      expect(RegModel.has("2345-9-b-1")).to.be(false);
    });

  });
});
