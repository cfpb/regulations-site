require('../../setup');
var sinon = require('sinon'); // Run npm install for this.
var sinonChai = require('sinon-chai');

chai.use(sinonChai);

describe('MetaModel:', function() {
    'use strict';

    var $, Backbone, MetaModel, Resources;

    before(function(){
        Backbone = require('backbone');
        $ = require('jquery');
        Backbone.$ = $;
        MetaModel = require('../../../source/models/meta-model');
        Resources = require('../../../source/resources');
        window.APP_PREFIX = '/eregulations/';
    });

    beforeEach(function(){
        this.metamodel = new MetaModel({
            content: {
              '1005-2-a': '<li id="1005-2-a">Paragraph content</li>',
              '1005-3-a': '<li id="1005-3-a">Paragraph content</li>'
            }
        });

        Resources.versionElements = {
            toc: $('<nav id="toc" data-toc-version="2014-20681"></nav>'),
        };
    });

    it('has is called correctly.', function() {
        expect(this.metamodel.has).to.be.ok; // Returns ok
        expect(this.metamodel.has()).to.be.not.ok; // Returns ok
    });

    it('has can tell if an id exists', function() {
        expect(this.metamodel.has('1005-2-a')).to.be.ok; // Returns true. '1005-2-a' is in the content.
        expect(this.metamodel.has('foo')).to.be.not.ok; // Returns false. Can't find foo in content.
    });

    it('set returns true for cached & formatted reg content', function() {
        expect(this.metamodel.set('1005-2-a', '<li id="1005-2-a">Paragraph content</li>')).to.be.ok;
        expect(this.metamodel.set('1005-4-a', '<li id="1005-4-a">Paragraph content</li>')).to.be.ok;
        expect(this.metamodel.set('', '')).to.be.not.ok;
    });

    it('getAJAXUrl returns the correct URL endpoint', function() {
        expect(this.metamodel.getAJAXUrl('1005-2')).to.equal('/eregulations/partial/1005-2/2014-20681');


        window.APP_PREFIX = ''; // Test without a urlPrefix
        expect(this.metamodel.getAJAXUrl('1005-2')).to.equal('/partial/1005-2/2014-20681');

        window.APP_PREFIX = '/eregulations/'; //Return to normal

    });

    it('retrieve returns true with a promise', function() {
        expect(this.metamodel.retrieve('1005-2-a')).to.be.ok;
        expect(this.metamodel.retrieve('1005-2-a')).to.have.property('promise');
    });

    it('request returns promise', function() {
        expect(this.metamodel.request('1005-2-a')).to.be.ok;
        expect(this.metamodel.request('1005-2-a')).to.have.property('promise');
    });

    it('get calls the callback correctly', function() {
        var cb = sinon.spy();
        var cbfail = sinon.spy();

        expect(this.metamodel.get('1005-2-a', cb)).to.be.ok; // Test a cached regulation
        expect(cb).to.have.been.called;

        expect(this.metamodel.get('1005-5-a', cb)).to.be.ok; // Test a reg that doesn't exist
        expect(cb).to.have.been.calledWith(false);
    });
});
