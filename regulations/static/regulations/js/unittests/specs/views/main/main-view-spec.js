require('../../../setup');
var sinon = require( 'sinon' );

describe('Main View:', function () {

  var view, $, e, MainView, regSection, appendixSection, interpSection;

  before(function () {
    $ = window.jQuery = require('jquery');
    MainView = require('../../../../source/views/main/main-view');
    sandbox = sinon.sandbox.create();
  });

  beforeEach(function(){

    regSection = '<div id="content-body" class="main-content open">' +
      '<section id="content-wrapper" class="reg-text">' +
      '<section id="1026-29" class="reg-section ' +
      'data-permalink-section="" data-base-version="2015-18239" ' +
      'data-page-type="reg-section">' +
      '</section>' +
      '</section>' +
      '</div>';

    appendixSection = '<div id="content-body" class="main-content open">' +
      '<section id="content-wrapper" class="reg-text">' +
      '<section id="1026-J" class="appendix-section" ' +
      'data-base-version="2015-18239" data-page-type="appendix">' +
      '</section>' +
      '</section>' +
      '</div>';


    $( 'body' ).html(regSection);

    // create a new instance of the view
    view = new MainView();
    view.$el = $('#content-body');

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

  it('should check if the content is a reg, appendix, or supplement', function() {
    var check = view.isAppendixOrSupplement();
    expect(check).to.equal(false);

    $('body').html();
    $('body').html(appendixSection);
    view = new MainView();
    view.$el = $('#content-body');
    var check = view.isAppendixOrSupplement();
    expect(check).to.equal('appendix');

  });

});
