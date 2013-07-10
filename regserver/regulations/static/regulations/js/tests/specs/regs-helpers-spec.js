define(['jquery', 'regs-helpers'], function($, RegsHelpers) {
    describe("Helper functions", function() {
        it("idToRef should turn basic IDs to references", function() {
            expect('§234.4(a)(2)').toEqual(RegsHelpers.idToRef('234-4-a-2'));

            expect('§87324.34(b)(23)(iv)(H)').toEqual(RegsHelpers.idToRef('87324-34-b-23-iv-H'));

            expect('Appendix X to Part 983').toEqual(RegsHelpers.idToRef('983-X-4'));

            expect('Supplement F to Part 13').toEqual(RegsHelpers.idToRef('F-13'));

            expect('§100').toEqual(RegsHelpers.idToRef('§100'));
        });
    });
});
