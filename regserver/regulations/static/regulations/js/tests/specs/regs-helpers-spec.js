define(['jquery', 'regs-helpers'], function($, RegsHelpers) {
    describe("Helper functions", function() {
        it("idToRef should turn basic IDs to references", function() {
            expect('§234.4(a)(2)').toEqual(RegsHelpers.idToRef('234-4-a-2'));

            expect('§87324.34(b)(23)(iv)(H)').toEqual(RegsHelpers.idToRef('87324-34-b-23-iv-H'));

            expect('Appendix X to Part 983').toEqual(RegsHelpers.idToRef('983-X-4'));

            expect('Supplement I to Part 13').toEqual(RegsHelpers.idToRef('13-Interp'));

            expect('Supplement I to §13.4').toEqual(RegsHelpers.idToRef('13-4-a-Interp-1'));

            expect('Supplement I to Appendix G').toEqual(RegsHelpers.idToRef('13-G-Interp-1'));

            expect('§100').toEqual(RegsHelpers.idToRef('§100'));
        });
    });
});
