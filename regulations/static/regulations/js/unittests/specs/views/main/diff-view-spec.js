require('../../../setup');
var sinon = require( 'sinon' );

describe('Diff View:', function () {

  var view, $, DiffView;

  before(function () {
    $ = require('jquery');
    DiffView = require('../../../../source/views/main/diff-view');
  });

  beforeEach(function(){

    // create a new instance of the view
    view = new DiffView();

    $('title').text('Comparison of 12 CFR § 1002.4 | eRegulations');
    document.title = 'Comparison of 12 CFR § 1002.4 | eRegulations';
  });

  it('should construct a view', function() {
    expect(view).to.be.defined;
  });

  it('should assemble the title', function() {
    view.id = '§1002.4';
    var title = view.assembleTitle();
    expect(title).to.be.equal('Comparison of §1002.4 | eRegulations');
  });

  it('should assemble the diff url', function() {
    var options = {
      id: '1005-1',
      baseVersion: '2011-12121',
      newerVersion: '2012-11111',
      fromVersion: '2012-11111'
    };
    var constructedUrl = view.assembleDiffURL(options);
    var url = '1005-1/2011-12121/2012-11111?from_version=2012-11111';
    expect(constructedUrl).to.be.equal(url);
  });

});
