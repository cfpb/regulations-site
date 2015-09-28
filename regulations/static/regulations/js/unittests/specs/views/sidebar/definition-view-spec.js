var chai = require('chai');
var expect = chai.expect;
var jsdom = require('mocha-jsdom');

describe('Definition View:', function() {
    'use strict';

    var view, $, Backbone, _, DefinitionView, SidebarModuleView, RegModel, Helpers, Router, MainEvents, SidebarEvents, GAEvents;

    jsdom();

    before(function (){
        $ = require('jquery');
        Backbone = require('backbone');
        DefinitionView = require('../../../../source/views/sidebar/definition-view');
    });

    beforeEach(function(){
        view = new DefinitionView();
    });

    it('should construct a veiw', function() {
        expect(view).to.be.ok;
    });
});
