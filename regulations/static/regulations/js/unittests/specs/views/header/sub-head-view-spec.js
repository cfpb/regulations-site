require('../../../setup');
var sinon = require( 'sinon' );

describe('Sub Head View:', function() {

  var view, $, e, SubHeadView;

  before(function() {
    $ = require('jquery');
    SubHeadView = require('../../../../source/views/header/sub-head-view');
    sandbox = sinon.sandbox.create();
  });

  beforeEach(function(){
    //  Adding a simplified version of the thing we want to test.
    $( 'body' ).html(
      '<div id="content-header" class="header-main group open">' +
        '<div class="wayfinding">' +
          '<span class="subpart"></span>' +
          '<span id="active-title"><em class="header-label"></em></span>' +
        '</div>' +
        '<span class="effective-date">' +
        '<h2></h2>' +
      '</div>' +
      '<section id="1999-1" class="reg-section" data-base-version="2013-22752_20140118" data-page-type="reg-section"> </section>' +
      '<div class="select-content">' +
        '<form>' +
          '<select name="new_version" onChange="this.form.submit();">' +
            '<option value="default" disabled="disabled" selected="selected">regulation effective</option>' +
            '<option value="2013-22752_20140110">1/10/2014</option>' +
          '</select>' +
        '</form>' +
      '</div>'
    );

    // create a new instance of the view
    view = new SubHeadView();

    view.el = $('#content-header');
    view.$activeTitle = $('.header-label');
  });

  it('should construct a view', function() {
    expect(view).to.be.defined;
  });

  it('populates subhead with new title', function() {
    view.changeTitle('1999-1');
    expect(view.$activeTitle.html()).to.contain('§1999.1');
  });

  it('displays a search result count', function() {
    view.displayCount('42');
    expect(view.$activeTitle.text()).to.contain('Search results 42');
  });

  it('changes the effective data', function() {
    view.changeDate();
    expect($('.effective-date').text()).to.have.string('Effective date: ');
  });

  it('adds the wayfinding id to the wayfinding class', function() {
    view.addWayfindID('1999-1');
    expect($('.wayfinding')).to.have.$attr('id', 'wayfind-1999-1');
  });

  it('adds a class around subparagraphs when the user scrolls', function(){
    view.changeTitle('1004-2-a-3');
    expect($('.header-label span').text()).to.contain('(a)(3)');
    expect($('.header-label span')).to.have.$attr('class', 'wayfinding-paragraph');
  });

  it('should render the subpart', function() {
    view.renderSubpart('pepperoni');
    var $classes = view.$activeTitle.attr('class');
    expect($('.subpart').text()).to.have.string('pepperoni');
    expect($classes).to.eql('header-label with-subpart');
  });

  it('should remove the subpart', function() {
    view.renderSubpart('mushroom');
    view.removeSubpart();
    var $classes = view.$activeTitle.attr('class');
    expect($('.subpart').text()).to.not.have.string('mushroom');
    expect($classes).to.eql('header-label');
  });

});
