'use strict';
var $ = require('jquery');
var _ = require('underscore');
var Backbone = require('backbone');
Backbone.$ = $;
var GAEvents = _.clone(Backbone.Events);
module.exports = GAEvents;
