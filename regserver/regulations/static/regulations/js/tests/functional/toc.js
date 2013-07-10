casper.start(casper.cli.get('testUrl'), function() {
    this.test.assertTrue(this.getElementBounds('nav#menu')['left'] < 0, "TOC should be offscreen");
});

casper.then(function() {
    this.test.assertExists('a#menu-link', 'TOC button is found');
    this.click('a#menu-link');
    this.test.assertVisible('nav#menu', 'TOC menu is open');
});

casper.run(function() {
    this.test.renderResults(true);
});
