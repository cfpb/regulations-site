require('../../../setup');
var sinon = require( 'sinon' );

describe('Header View:', function() {

  var view, $, e, HeaderView;

  before(function() {
    $ = require('jquery');
    HeaderView = require('../../../../source/views/header/header-view');
    sandbox = sinon.sandbox.create();
  });

  beforeEach(function(){
    //  Adding a simplified version of the thing we want to test.
    $( 'body' ).html(
      '<header id="site-header" class="reg-header chrome-header open" role="banner">' +
        '<div class="main-head">' +
          '<div class="title">' +
            '<h1 class="site-title"><a href="/"><span class="e">e</span>Regulations</a></h1>' +
            '<h2 class="reg-title"><a href="/#">Pizza Standards</a></h2>' +
          '</div>' +
          '<nav class="app-nav">' +
            '<a href="#" class="mobile-nav-trigger">' +
             '<span class="cf-icon cf-icon-menu"></span>' +
             '<span class="icon-text">Mobile navigation</span>' +
            '</a>' +
              '<ul class="app-nav-list">' +
                '<li class="app-nav-list-item"><a href="/">Regulations</a></li>' +
                '<li class="app-nav-list-item"><a href="/about">About</a></li>' +
                '<li class="app-nav-list-item org-title">' +
                  '<a href="http://pizz.gov">pizza.gov</a>' +
                '</li>' +
              '</ul>' +
          '</nav>' +
        '</div>' +
      '</header>'
    );

    // create a new instance of the view
    view = new HeaderView();

    view.el = $('.reg-header');

  });

  it('should construct a view', function() {
    expect(view).to.be.defined;
  });

});
