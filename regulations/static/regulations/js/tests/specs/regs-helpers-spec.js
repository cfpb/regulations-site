define(['jquery', 'regs-helpers'], function($, RegsHelpers) {
    describe("Helper functions", function() {
        it("idToRef should turn basic IDs to references", function() {
            expect('§234.4(a)(2)').to.be(RegsHelpers.idToRef('234-4-a-2'));

            expect('§87324.34(b)(23)(iv)(H)').to.be(RegsHelpers.idToRef('87324-34-b-23-iv-H'));

            expect('Appendix X to Part 983').to.be(RegsHelpers.idToRef('983-X-4'));

            expect('Supplement I to Part 13').to.be(RegsHelpers.idToRef('13-Interp'));

            expect('Supplement I to §13.4').to.be(RegsHelpers.idToRef('13-4-a-Interp-1'));

            expect('Supplement I to Appendix G').to.be(RegsHelpers.idToRef('13-G-Interp-1'));

            expect('§100').to.be(RegsHelpers.idToRef('§100'));
        });

        it("should find base sections of any id", function() {
            expect(RegsHelpers.findBaseSection('1234-2-a-1')).to.be('1234-2');

            expect(RegsHelpers.findBaseSection('I-1234-5')).to.be('I-1234');

            expect(RegsHelpers.findBaseSection('1234-C-1')).to.be('1234-C');
        });
    });
});
