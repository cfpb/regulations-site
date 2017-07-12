'use strict';
var $ = require( 'jquery' );
var _ = require( 'underscore' );
var Backbone = require( 'backbone' );
Backbone.$ = $;

var HeaderEvents = _.clone( Backbone.Events );
module.exports = HeaderEvents;
