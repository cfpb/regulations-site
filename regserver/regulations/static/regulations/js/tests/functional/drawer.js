var casper = require('casper').create(),
    utils = require('utils'),
    url = casper.cli.get('url');

casper.start();

casper.thenOpen(url + '/1005', function() {
});

// all drawer tabs are present
casper.waitForSelector('#site-header', function() {
    this.test.assertExists(
        '#menu-link',
        'TOC drawer tab is present'
    );

    this.test.assertExists(
        '#timeline-link',
        'Timeline drawer tab is present'
    );

    this.test.assertExists(
        '#search-link',
        'Search drawer tab is present'
    );
});

casper.then(function() {
    // activate timeline pane
    this.click('#timeline-link');
});

casper.wait(5000);

// timeline pane should be showing
casper.then(function() {
    this.test.assertExists(
        '#table-of-contents.hidden',
        'TOC pane is hidden'
    );

    this.test.assertExists(
        '#search.hidden',
        'Search pane is hidden'
    );

    this.test.assertDoesntExist(
        '#timeline.hidden',
        'Timeline pane is visible'
    );
});

// make sure timeline tab is highlighted
casper.then(function() {
    this.test.assertExists(
        '#timeline-link.current',
        'Timeline drawer tab is highlighted'
    );
});

casper.run(function() {
    this.test.renderResults(true);
});
