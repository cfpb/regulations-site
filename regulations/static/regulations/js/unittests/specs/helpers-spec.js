require('../setup');

describe('Non-DOM Helper functions:', function() {
    'use strict';

    var $, Helpers;

    before(function(){
        $ = require('jquery');
        Helpers = require('../../source/helpers');
    });

    beforeEach(function(){

    });

    it('isIterable should tell you if something is iterable', function() {
        expect(Helpers.isIterable([])).to.be.ok;

        expect(Helpers.isIterable({})).to.be.ok;

        expect(Helpers.isIterable('dsdf')).to.not.be.ok;

        expect(Helpers.isIterable(4345)).to.not.be.ok;
    });

    it('interpId should return the correct title for the type of supplement', function() {
        expect(Helpers.interpId(['123'])).to.equal('Supplement I to Part ');

        expect(Helpers.interpId(['123', 'G'])).to.equal('Supplement I to Appendix ');

        expect(Helpers.interpId(['4', '4'])).to.equal('Supplement I to ');

        expect(Helpers.interpId(['3', '4', '5', '6'])).to.equal('Supplement I to ');

        expect(Helpers.interpId(['3', 'a', '3'])).to.equal('Supplement I to Appendix ');
    });

    it('appendixId should return the proper title', function() {
        expect(Helpers.appendixId('234', 'G')).to.equal('Appendix G to Part 234');
    });

    it('idToRef should turn IDs to titles', function() {
        expect('Supplement I to Part 123').to.equal(Helpers.idToRef('123-Subpart-A-Interp'));

        expect('Appendix A1 to Part 345').to.equal(Helpers.idToRef('345-A1'));

        expect('§234.4(a)(2)').to.equal(Helpers.idToRef('234-4-a-2'));

        expect('§87324.34(b)(23)(iv)(H)').to.equal(Helpers.idToRef('87324-34-b-23-iv-H'));

        expect('Appendix X to Part 983').to.equal(Helpers.idToRef('983-X-4'));

        expect('Supplement I to Part 13').to.equal(Helpers.idToRef('13-Interp'));

        expect('Supplement I to §13.4(a)').to.equal(Helpers.idToRef('13-4-a-Interp-1'));

        expect('Supplement I to Appendix G').to.equal(Helpers.idToRef('13-G-Interp-1'));

        expect('§100').to.equal(Helpers.idToRef('§100'));

        expect('Supplement I to Part 123').to.equal(Helpers.idToRef('123-Subpart-A-Interp'));

        expect('Appendix A1 to Part 345').to.equal(Helpers.idToRef('345-A1'));

        expect ('Supplement I to Appendices').to.equal(Helpers.idToRef('Appendices-1'));
    });

    it('findBaseSection should find base sections of any id', function() {
        expect(Helpers.findBaseSection('1234-2-a-1')).to.equal('1234-2');

        expect(Helpers.findBaseSection('I-1234-5')).to.equal('I-1234');

        expect(Helpers.findBaseSection('1234-C-1')).to.equal('1234-C');

        expect(Helpers.findBaseSection('123-4-Interp-5')).to.equal('123-4-Interp');

        expect(Helpers.findBaseSection('123-Appendices-Interp-4')).to.equal('123-Appendices-Interp');

        expect(Helpers.findBaseSection('123-Subpart-A-Interp-4')).to.equal('123-Subpart-A-Interp');

        expect(Helpers.findBaseSection('123-Subpart-Interp-4')).to.equal('123-Subpart-Interp');

        expect(Helpers.findBaseSection('123-Interp-h1')).to.equal('123-Interp-h1');

        expect(Helpers.findBaseSection('123')).to.equal('123');

        expect(Helpers.findBaseSection('123-A')).to.equal('123-A');
    });

    it('isSupplement should be able to tell if it\'s a supplement', function() {
        expect(Helpers.isSupplement('13-Interp')).isTrue;

        expect(Helpers.isSupplement('123-Appendices-Interp')).isTrue;

        expect(Helpers.isSupplement('87324-34-b-23-iv-H')).isFalse;

        expect(Helpers.isSupplement('50')).isFalse;

    });

    it('isAppendix should find Appendices', function() {
        expect(Helpers.isAppendix('13-Interp')).isFalse;

        expect(Helpers.isAppendix('123-Appendices-Interp')).isTrue;

        expect(Helpers.isAppendix('87324-34-b-23-iv-H')).isFalse;

        expect(Helpers.isAppendix('50')).isFalse;
    });

    it('formatSubpartLabel should format correctly', function(){

        expect(Helpers.formatSubpartLabel('123-Subpart-C')).to.equal('Subpart C');

        expect(Helpers.formatSubpartLabel('13-Interp')).to.equal('Subpart ');
    });
});

describe('Version Finder Helper Functions:', function() {
    'use strict';

    var $, Helpers;

    var navMenu, navMenu_blank, section, section_blank, timeline, timeline_blank;

    before(function() {
        $ = require('jquery');
        Helpers = require('../../source/helpers');
    });

    it('should return version when "nav#toc" present on the element', function() {

        var tocTest = {
            toc: $('<nav id="toc" data-toc-version="nav-date"></nav>')
        };

        var sectionTest = {
            toc: $('<nav id="toc"></nav>'),
            regLandingPage: $('<section data-base-version="section-date"></section>')
        };

        var timelineTest = {
            toc: $('<nav id="toc"></nav>'),
            timelineList: $('<a id="timeline"><li class="current"><a class="stop-button" data-version="timeline-date"></a></li></a>')
        };

        expect(Helpers.findVersion(tocTest)).to.equal('nav-date');
        expect(Helpers.findVersion(sectionTest)).to.equal('section-date');
        expect(Helpers.findVersion(timelineTest)).to.equal('timeline-date');

        //Add a different date somewhere. It should grab the date in the Nav first.
        tocTest.regLandingPage = $('<section data-base-version="section-date"></section>');

        expect(Helpers.findVersion(tocTest)).to.not.equal('section-date');
    });

    it('should find version on section when "nav#toc" is not present', function() {

        var sectionTest = {
            toc: $('<nav id="toc"></nav>'),
            regLandingPage: $('<section data-base-version="section-date"></section>')
        };

        var timelineTest = {
            toc: $('<nav id="toc"></nav>'),
            regLandingPage: $('<section data-base-version="section-date"></section>'),
            timelineList: $('<a id="timeline"><li class="current"><a class="stop-button" data-version="timeline-date"></a></li></a>')
        };

        expect(Helpers.findVersion(sectionTest)).to.equal('section-date');
        expect(Helpers.findVersion(timelineTest)).to.not.equal('timeline-date');

    });

    it('should find version on timeline if version isn\'t available anywhere else', function() {

        var timelineTest = {
            toc: $('<nav id="toc"></nav>'),
            regLandingPage: $('<section data-base-version="section-date"></section>'),
            timelineList: $('<a id="timeline"><li class="current"><a class="stop-button" data-version="timeline-date"></a></li></a>')
        };

        // It searches for the stop button because of the diff version.
        var diffVersion = {
            timelineList: $('<a id="timeline"><li class="current"><a data-version="timeline-date"></a></li></a>')
        };

        expect(Helpers.findVersion(timelineTest)).to.not.equal('timeline-date');
        expect(Helpers.findVersion(diffVersion)).to.not.be.ok;
    });

    it('works with findDiffVersion', function() {

        var tocTest = {
            toc: $('<nav id="toc" data-toc-version="nav-date"></nav>'),
            diffToc: $('<div id="table-of-contents" data-from-version="diff-toc-date"></div>'),
            timelineList: $('<div id="timeline"><li class="current"><a class="version-link" data-version="version-link-date"></a></li></div>')
        };

        expect(Helpers.findDiffVersion(tocTest)).to.equal('diff-toc-date');

    });

    it('returns the right data when diffVersion = version', function(){
        var diffTest = {
            toc: $('<nav id="toc" data-toc-version="same-date"></nav>'),
            diffToc: $('<div id="table-of-contents" data-from-version="same-date"></div>'),
            timelineList: $('<div id="timeline"><li class="current"><a class="version-link" data-version="diff-date">Regulation</a></li></div>')
        };

        expect(Helpers.findDiffVersion(diffTest, 'same-date')).to.equal('diff-date');
        expect(Helpers.findDiffVersion(diffTest)).to.equal('diff-date');
    });

});

describe('Other Helper Functions:', function() {

    'use strict';

    xit('parseURL should parse correctly', function() {
        // This method requires the DOM
    });


});
