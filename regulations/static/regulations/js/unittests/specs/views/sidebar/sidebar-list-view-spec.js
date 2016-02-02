require('../../../setup');
var sinon = require( 'sinon' );

describe('Sidebar List View:', function() {

  var view, definition, $, SidebarList;

  before(function() {
    $ = require('jquery');
    SidebarList = require('../../../../source/views/sidebar/sidebar-list-view');
  });

  beforeEach(function(){
    // create a new instance of the view
    view = new SidebarList();
  });

  it('should construct a view', function() {
    expect(view).to.be.defined;
  });

});
