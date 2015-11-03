require('../../../setup');
var sinon = require( 'sinon' );

describe('Main View:', function () {

  var view, $, e, MainView;

  before(function () {
    $ = require('jquery');
    MainView = require('../../../../source/views/main/main-view');
    sandbox = sinon.sandbox.create();
  });

  beforeEach(function(){
    // create a new instance of the view
    view = new MainView();

    e = {
      preventDefault: function() {
        return true;
      }
    };

  });

  it('should construct a view', function() {
    expect(view).to.be.defined;
    expect(view.el).to.be.defined;
  });

  // it('should', function() {
  //   var childViewOptions = {
  //     subContentType: false
  //   }
  //   sinon.stub(view, 'isAppendixOrSupplement').returns('appendix');
  //   expect(childViewOptions.subContentType).to.equal('appendix');
  // });

  it('should check if the content is an appendix or supplement', function() {
    var check = view.isAppendixOrSupplement();
    expect(check).to.equal(false);
  });

});
