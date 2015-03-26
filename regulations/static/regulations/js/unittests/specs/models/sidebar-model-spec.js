var chai = require('chai');
var expect = chai.expect;
var jsdom = require('mocha-jsdom');

describe('Sidebar Model:', function() {
    'use strict';

    var $, Backbone, SidebarModel, Resources;

    jsdom();

    before(function (){
        Backbone = require('backbone');
        $ = require('jquery');
        Backbone.$ = $;
        SidebarModel = require('../../../source/models/sidebar-model');
        Resources = require('../../../source/resources');
        window.APP_PREFIX = '/eregulations/';
    });

    beforeEach(function(){
        Resources.versionElements = {
            toc: $('<nav id="toc" data-toc-version="2014-20681"></nav>'),
        };
        this.sidebarmodel = new SidebarModel;
    });

    it('run', function() {
        console.log(SidebarModel);
        console.log(this.sidebarmodel);

    });
    xit('getAJAXUrl returns the correct URL endpoint with /sidebar supplemental path', function() {
        expect(SidebarModel.getAJAXUrl('1005-2')).to.equal('/eregulations/partial/sidebar/1005-2/2014-20681');


        window.APP_PREFIX = ''; // Test without a urlPrefix
        expect(SidebarModel.getAJAXUrl('1005-2')).to.equal('/partial/sidebar/1005-2/2014-20681');

        window.APP_PREFIX = '/eregulations/'; //Return to normalt

    });
});