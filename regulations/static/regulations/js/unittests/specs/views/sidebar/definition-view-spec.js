require('../../../setup');

describe('Definition View:', function () {

  var view, $, DefinitionView;

  before(function () {
    $ = require('jquery');
    DefinitionView = require('../../../../source/views/sidebar/definition-view');
  });

  beforeEach(function(){
      view = new DefinitionView({
        id: '1',
        term: 'Peanut Butter Jelly'
      });

      view.render();
  });

  it('works', function () {
    document.body.innerHTML = '<div>hola</div>';
    expect($("div").html()).eql('hola');
  });

  it('has document', function () {
    var div = document.createElement('div');
    expect(div.nodeName).eql('DIV');
  });

  it('should construct a veiw', function() {
      expect(view).to.be.ok;
  });

});
