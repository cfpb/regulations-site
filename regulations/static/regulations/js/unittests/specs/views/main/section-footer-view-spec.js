require('../../../setup');
var sinon = require( 'sinon' );

describe('Section Footer View:', function () {

  var view, $, e, FooterView, MainEvents;

  before(function () {
    $ = require('jquery');
    FooterView = require('../../../../source/views/main/section-footer-view');
    MainEvents = require('../../../../source/events/main-events');
  });

  beforeEach(function(){
    // create a new instance of the view
    view = new FooterView();

    e = {
      preventDefault: function() {
        return true;
      }
    };

  });

  it('should construct a view', function() {
    expect(view).to.be.defined;
    expect(view.events).to.be.defined;
    expect(view.events).to.deep.equal({'click .navigation-link': 'sendNavEvent'});
    expect(view.events['click .navigation-link']).to.equal('sendNavEvent');
  });

  it('should trigger the nav event when send', function() {
    sinon.spy(MainEvents, 'trigger');
    view.sendNavEvent(e);
    expect(MainEvents.trigger.calledOnce).to.be.true;
  });

  it('should stop listening to the view when remove is called', function() {
    sinon.spy(view, 'stopListening');
    view.remove();
    expect(view.stopListening.calledOnce).to.be.true;
  });

});
