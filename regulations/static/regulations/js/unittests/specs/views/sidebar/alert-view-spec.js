require('../../../setup');
var sinon = require( 'sinon' );

describe('Alert View:', function() {

  var view, definition, $, AlertView;

  before(function() {
    $ = require('jquery');
    AlertView = require('../../../../source/views/sidebar/alert-view');
  });

  beforeEach(function(){
    // create a new instance of the view
    view = new AlertView();
  });

  it('should construct a view', function() {
    expect(view).to.be.defined;
  });

});
