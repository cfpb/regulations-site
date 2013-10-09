var casper = require('casper').create();

casper.start('http://localhost:8000/1005', function() {
    this.test.assertTrue(this.getElementBounds('#menu')['left'] < 0, "TOC should be offscreen");
});

casper.then(function() {
    this.test.assertExists('a#menu-link', 'TOC button is found');
    this.click('a#menu-link');
    this.test.assertVisible('#menu', 'TOC menu is open');
});

casper.run(function() {
    this.test.renderResults(true);
});
