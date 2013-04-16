/**
  add ability to load json fixtures into jasmine
**/

var readJsonFixtures = function() {
  return jasmine.getJsonFixtures().proxyCallTo_('read', arguments);
};

var preloadJsonFixtures = function() {
  jasmine.getJsonFixtures().proxyCallTo_('preload', arguments);
};

var loadJsonFixtures = function() {
  return jasmine.getJsonFixtures().proxyCallTo_('load', arguments);
};

var setJsonFixtures = function(data) {
  return jasmine.getJsonFixtures().set(data);
};

var getJsonFixture = function(url) {
  return jasmine.getJsonFixtures().proxyCallTo_('read', arguments)[url];
};

jasmine.getJsonFixtures = function() {
  return jasmine.currentJsonFixtures_ = jasmine.currentJsonFixtures_ || new jasmine.JSONFixtures();
};

jasmine.JSONFixtures = function() {
  this.fixturesCache_ = {};
  this.fixturesPath = 'spec/javascripts/fixtures/json';
};

jasmine.JSONFixtures.prototype.set = function(data) {
  this.clearCache();
  this.fixturesCache_ = data
};

jasmine.JSONFixtures.prototype.preload = function() {
  this.read.apply(this, arguments);
};

jasmine.JSONFixtures.prototype.load = function() {
  this.read.apply(this, arguments);
  return this.fixturesCache_
};

jasmine.JSONFixtures.prototype.read = function() {
  var fixtureUrls = arguments;
  for(var urlCount = fixtureUrls.length, urlIndex = 0; urlIndex < urlCount; urlIndex++) {
    this.getFixtureData_(fixtureUrls[urlIndex]);
  }
  return this.fixturesCache_
};

jasmine.JSONFixtures.prototype.clearCache = function() {
  this.fixturesCache_ = {};
};

jasmine.JSONFixtures.prototype.getFixtureData_ = function(url) {  
  if (typeof this.fixturesCache_[url] == 'undefined') {
    this.loadFixtureIntoCache_(url);
  }
  return this.fixturesCache_[url];
};

jasmine.JSONFixtures.prototype.loadFixtureIntoCache_ = function(relativeUrl) {
  var self = this;
  var url = this.fixturesPath.match('/$') ? this.fixturesPath + relativeUrl : this.fixturesPath + '/' + relativeUrl;
  jQuery.ajax({
    async: false, // must be synchronous to guarantee that no tests are run before fixture is loaded
    cache: false,
    dataType: 'json',
    url: url,
    success: function(data) {
      self.fixturesCache_[relativeUrl] = data;
    },
    error: function(jqXHR, status, errorThrown) {
        throw Error('JSONFixture could not be loaded: ' + url + ' (status: ' + status + ', message: ' + errorThrown.message + ')');
    }
  });
};

jasmine.JSONFixtures.prototype.proxyCallTo_ = function(methodName, passedArguments) {
  return this[methodName].apply(this, passedArguments);
};