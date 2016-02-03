require('../../setup');

describe('Diff Model:', function() {
    'use strict';

    var $, Backbone, DiffModel, Resources;

    before(function(){
        Backbone = require('backbone');
        $ = require('jquery');
        Backbone.$ = $;
        DiffModel = require('../../../source/models/diff-model');
        Resources = require('../../../source/resources');
        window.APP_PREFIX = '/eregulations/';
    });

    beforeEach(function(){
        Resources.versionElements = {
            toc: $('<nav id="toc" data-toc-version="2014-20681"></nav>'),
        };
    });

    it('getAJAXUrl returns the correct URL endpoint with /diff supplemental path', function() {
        expect(DiffModel.getAJAXUrl('1005-2')).to.equal('/eregulations/partial/diff/1005-2/2014-20681');


        window.APP_PREFIX = ''; // Test without a urlPrefix
        expect(DiffModel.getAJAXUrl('1005-2')).to.equal('/partial/diff/1005-2/2014-20681');

        window.APP_PREFIX = '/eregulations/'; //Return to normalt

    });
});
