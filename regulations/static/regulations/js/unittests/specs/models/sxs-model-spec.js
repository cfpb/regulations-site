require('../../setup');

describe('SxS Model:', function() {
    'use strict';

    var $, Backbone, SxSModel, Resources;

    before(function(){
        Backbone = require('backbone');
        $ = require('jquery');
        Backbone.$ = $;
        SxSModel = require('../../../source/models/sxs-model');
        Resources = require('../../../source/resources');
        window.APP_PREFIX = '/eregulations/';
    });

    beforeEach(function(){
        Resources.versionElements = {
            toc: $('<nav id="toc" data-toc-version="2014-20681"></nav>'),
        };
    });

    it('getAJAXUrl returns the correct URL endpoint with /sxs supplemental path', function() {
        expect(SxSModel.getAJAXUrl('1005-2')).to.equal('/eregulations/partial/sxs/1005-2/2014-20681');


        window.APP_PREFIX = ''; // Test without a urlPrefix
        expect(SxSModel.getAJAXUrl('1005-2')).to.equal('/partial/sxs/1005-2/2014-20681');

        window.APP_PREFIX = '/eregulations/'; //Return to normal

    });
});
