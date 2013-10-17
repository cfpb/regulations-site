var casper = require('casper').create(),
    utils = require('utils'),
    url = casper.cli.get('url');

casper.start();

casper.thenOpen(url + '/1005', function() {
});

casper.waitForSelector('#site-header', function() {
    this.test.assertExists(
        '#table-of-contents',
        'TOC drawer tab is present'
    );

    this.test.assertExists(
        '#timeline',
        'Timeline drawer tab is present'
    );

    this.test.assertExists(
        '#search',
        'Search drawer tab is present'
    );

});

casper.then(function() {
    this.click('#timeline');
});

casper.run(function() {
    this.test.renderResults(true);
});
