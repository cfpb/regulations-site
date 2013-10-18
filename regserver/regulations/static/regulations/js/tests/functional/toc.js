var casper = require('casper').create(),
    utils = require('utils'),
    url = casper.cli.get('url');

casper.start();

casper.thenOpen(url + '/1005', function() {
});

casper.waitForSelector('.reg-header.active', function() {
    this.test.assertExists('a#panel-link', 'TOC button is found');
});

casper.then(function() {
    //this.test.assertTrue(this.getElementBounds('#menu')['left'] > 0, "TOC should be visible");
    this.click('a#panel-link');
});

casper.waitForSelector('.reg-header:not(.active)', function() {
    this.test.assertTrue(this.getElementBounds('#menu')['left'] < 0, "TOC should be offscreen");
    this.test.assertExists('a[data-section-id="1005-4"]', 'Find TOC link for 1005-4');
    this.click('a[data-section-id="1005-4"]');
});

casper.wait(5000);

casper.then(function() {
    this.test.assertEquals(url + '/1005-4/2013-06861', this.getCurrentUrl(), 'TOC click loads reg section - routing');
});

casper.run(function() {
    this.test.renderResults(true);
});
