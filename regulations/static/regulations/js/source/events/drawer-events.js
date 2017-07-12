'use strict';
var $ = require( 'jquery' );
var _ = require( 'underscore' );
var Backbone = require( 'backbone' );
Backbone.$ = $;

var DrawerEvents = _.clone( Backbone.Events );
module.exports = DrawerEvents;
