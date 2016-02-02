require('../../../setup');
var sinon = require( 'sinon' );

describe('Sidebar Module View:', function() {

  var view, definition, $, SidebarList;

  before(function() {
    $ = require('jquery');
    SidebarModule = require('../../../../source/views/sidebar/sidebar-module-view');
    RegModel = require('../../../../source/models/reg-model');
  });

  beforeEach(function(){

    // create a fake RegModel
    RegModel.get = function(){
      return 'supreme pizza';
    };

    //  Adding a simplified version of the thing we want to test.
    $( 'body' ).html(
      '<section id="sidebar-module"></section>'
    );

    // create a new instance of the view
    view = new SidebarModule();
    view.$el = $('#sidebar-module');

  });

  it('should construct a view', function() {
    expect(view).to.be.defined;
  });

  it('should render content in the view', function() {
    view.render();
    expect(view.$el.text()).to.contain('supreme pizza');
  });

});
