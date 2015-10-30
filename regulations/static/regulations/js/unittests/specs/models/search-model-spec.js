require('../../setup');

describe('Search Model:', function() {
    'use strict';

    var $, Backbone, SearchModel, Resources;

    before(function (){
        Backbone = require('backbone');
        $ = require('jquery');
        Backbone.$ = $;
        SearchModel = require('../../../source/models/search-model');
        Resources = require('../../../source/resources');
        window.APP_PREFIX = '/eregulations/';
    });

    beforeEach(function(){
        Resources.versionElements = {
            toc: $('<nav id="toc" data-toc-version="2014-20681"></nav>'),
        };
    });

    // A Twist on the normal getAJAXUrl test: This shouldn't return a date on the URL.
    it('getAJAXUrl returns the correct URL endpoint with /search supplemental path', function() {
        expect(SearchModel.getAJAXUrl('1005-2')).to.equal('/eregulations/partial/search/1005-2');


        window.APP_PREFIX = ''; // Test without a urlPrefix
        expect(SearchModel.getAJAXUrl('1005-2')).to.equal('/partial/search/1005-2');

        window.APP_PREFIX = '/eregulations/'; //Return to normal

    });
});
