require('../../../setup');
var sinon = require( 'sinon' );

describe('Section Footer View:', function () {

  var view, $, e, FooterView, Router;

  before(function () {
    $ = require('jquery');
    Router= require('../../../../source/router');
    FooterView = require('../../../../source/views/main/section-footer-view');
    sandbox = sinon.sandbox.create();
  });

  beforeEach(function(){
    //  Adding a simplified version of the thing we want to test.
    $( 'body' ).html(

    );

    // create a new instance of the view
    view = new FooterView();

    Router.hasPushState = false;


  });

  it('should construct a view', function() {
    expect(view).to.be.defined;
    expect(view.events).to.be.defined;
    expect(view.events).to.deep.equal({'click .navigation-link': 'sendNavEvent'});
    expect(view.events['click .navigation-link']).to.equal('sendNavEvent');
  });

});
