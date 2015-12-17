require('../../../setup');
var sinon = require( 'sinon' );

describe('Sidebar View:', function () {

  var view, definition, $, SidebarView;

  before(function () {
    $ = require('jquery');
    SidebarView = require('../../../../source/views/sidebar/sidebar-view');
  });

  beforeEach(function(){

    $( 'body' ).html(
      '<div id="sidebar-content"></div>'
    );

    function sidebarModelMock () {

    }


    // create a new instance of the view
    view = new SidebarView();

  });

  it('should construct a view', function() {
    expect(view).to.be.defined;
  });

});
