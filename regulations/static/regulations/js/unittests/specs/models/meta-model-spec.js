var expect = require('chai').expect;
var jsdom = require('mocha-jsdom');

describe('MetaModel', function() {
    'use strict';

    var $, Backbone, MetaModel;

    jsdom();

    before(function (){
        Backbone = require('backbone');
        $ = require('jquery');
        Backbone.$ = $;
        MetaModel = require('../../../source/models/meta-model');
    });

    beforeEach(function(){

    });

    it('.has returns a boolean correctly', function() {
        var has = MetaModel.prototype.has.Function;
        expect(has).to.be.ok;
        console.log(has);//.to.be.not.ok;
        //console.log(MetaModel.__super__.has);
        //console.log(MetaModel.prototype.has);
    });

});

