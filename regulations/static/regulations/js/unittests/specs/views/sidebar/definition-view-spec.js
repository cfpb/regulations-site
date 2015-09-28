require('../../../setup');
var sinon = require( 'sinon' );

describe('Definition View:', function () {

  var view, definition, content, $, DefinitionView;

  before(function () {
    $ = require('jquery');
    DefinitionView = require('../../../../source/views/sidebar/definition-view');
    sandbox = sinon.sandbox.create();
  });

  beforeEach(function(){

    //  Adding a simplified version of the thing we want to test.
    $( 'body' ).html(
      '<section id="definition"></section>'
    );

    // some HTML to insert into the definition
    content = '<div id="1005-2-a-1" class="open-definition">'+
        '<div class="sidebar-header group">' +
            '<h4>Defined Term <a class="right close-button" href="#">Close definition</a></h4>' +
        '</div>' +
        '<div class="definition-warning hidden group">' +
            '<span class="cf-icon cf-icon-error icon-warning"></span>' +
            '<div class="msg">' +
            '</div>' +
        '</div>' +
        '<div class="definition-text">' +
            '<p>Sustainable quinoa lo-fi, cray leggings plaid Intelligentsia hoodie ' +
            'forage tofu. 90s narwhal vegan artisan, Shoreditch cornhole sustainable ' +
            'distillery Brooklyn. </p>' +
            '<a href="/1005-2/2014-20681#1005-2-a-1" class="continue-link full-def internal"' + 'data-linked-section="1005-2-a-1">§ 1005.2(a)(1)</a>' +
            '<a class="close-button tab-activated" href="#">Close definition</a>' +
        '</div>' +
    '</div>';

    // create a new instance of the view
    view = new DefinitionView();

    view.el = $('#definition');
  });

  it('should construct a view', function() {
    expect(view).to.be.defined;
  });

  describe('Render methods:', function () {

    it('renders the header with loading indicator', function () {
      view.renderHeader();
      expect(view.$el.html()).to.eql(
        '<div class="sidebar-header group spinner"><h4>Defined Term</h4></div>'
      );
    });

    it('renders definition HTML', function() {
      view.render(content);
      expect(view.$el.html()).to.contain('90s narwhal vegan artisan');
    });

  });

});
