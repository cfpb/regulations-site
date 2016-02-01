require('../../../setup');
var sinon = require( 'sinon' );

describe('Help View:', function() {

  var view, definition, $, HelpView;

  before(function() {
    $ = require('jquery');
    HelpView = require('../../../../source/views/sidebar/help-view');
  });

  beforeEach(function(){
    // create a new instance of the view
    view = new HelpView();
  });

  it('should construct a view', function() {
    expect(view).to.be.defined;
  });

});
