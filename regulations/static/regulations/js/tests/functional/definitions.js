var casper = require('casper').create(),
    utils = require('utils'),
    url = casper.cli.get('url');

casper.start();

casper.thenOpen(url + '1005-1/2012-12121');

casper.waitForSelector();

casper.run(function() {
    this.test.renderResults(true);
});
