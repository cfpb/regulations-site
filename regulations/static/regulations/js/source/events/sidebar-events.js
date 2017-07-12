'use strict';
var $ = require( 'jquery' );
var _ = require( 'underscore' );
var Backbone = require( 'backbone' );
Backbone.$ = $;

var SidebarEvents = _.clone( Backbone.Events );
module.exports = SidebarEvents;
