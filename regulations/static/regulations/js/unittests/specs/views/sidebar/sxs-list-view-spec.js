require('../../../setup');
var sinon = require( 'sinon' );

describe('SxS List View:', function () {

  var view, definition, $, SxSList;

  before(function () {
    $ = require('jquery');
    SxSList = require('../../../../source/views/sidebar/sxs-list-view');
  });

  beforeEach(function(){
    // create a new instance of the view
    view = new SxSList();

  });

  it('should construct a view', function() {
    expect(view).to.be.defined;
  });

});
