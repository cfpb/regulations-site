var $ = require('jquery');
var Helpers = require('../../source/helpers');
var expect = require('expect.js');

describe("Helper functions", function() {
    'use strict';

    it('isIterable should tell you if something is iterable', function() {
        expect(Helpers.isIterable([])).to.be.ok();

        expect(Helpers.isIterable({})).to.be.ok();

        expect(Helpers.isIterable('dsdf')).to.be(false);

        expect(Helpers.isIterable(4345)).to.be(false);
    });

    it('interpId should return the correct title for the type of supplement', function() {
        expect(Helpers.interpId(['123'])).to.be('Supplement I to Part ');

        expect(Helpers.interpId(['123', 'G'])).to.be('Supplement I to Appendix ');

        expect(Helpers.interpId(['4', '4'])).to.be('Supplement I to ');

        expect(Helpers.interpId(['3', '4', '5', '6'])).to.be('Supplement I to ');

        expect(Helpers.interpId(['3', 'a', '3'])).to.be('Supplement I to Appendix ');
    });

    it('appendixId should return the proper title', function() {
        expect(Helpers.appendixId('234', 'G')).to.be('Appendix G to Part 234');
    });

    it('idToRef should turn IDs to titles', function() {
        expect('§234.4(a)(2)').to.be(Helpers.idToRef('234-4-a-2'));

        expect('§87324.34(b)(23)(iv)(H)').to.be(Helpers.idToRef('87324-34-b-23-iv-H'));

        expect('Appendix X to Part 983').to.be(Helpers.idToRef('983-X-4'));

        expect('Supplement I to Part 13').to.be(Helpers.idToRef('13-Interp'));

        expect('Supplement I to §13.4(a)').to.be(Helpers.idToRef('13-4-a-Interp-1'));

        expect('Supplement I to Appendix G').to.be(Helpers.idToRef('13-G-Interp-1'));

        expect('§100').to.be(Helpers.idToRef('§100'));

        expect('Supplement I to Part 123').to.be(Helpers.idToRef('123-Subpart-A-Interp'));

        expect('Appendix A1 to Part 345').to.be(Helpers.idToRef('345-A1'));
    });

    it('should find base sections of any id', function() {
        expect(Helpers.findBaseSection('1234-2-a-1')).to.be('1234-2');

        expect(Helpers.findBaseSection('I-1234-5')).to.be('I-1234');

        expect(Helpers.findBaseSection('1234-C-1')).to.be('1234-C');

        expect(Helpers.findBaseSection('123-4-Interp-5')).to.be('123-4-Interp');

        expect(Helpers.findBaseSection('123-Appendices-Interp-4')).to.be('123-Appendices-Interp');

        expect(Helpers.findBaseSection('123-Subpart-A-Interp-4')).to.be('123-Subpart-A-Interp');

        expect(Helpers.findBaseSection('123-Subpart-Interp-4')).to.be('123-Subpart-Interp');

        expect(Helpers.findBaseSection('123-Interp-h1')).to.be('123-Interp-h1');
    });
});
