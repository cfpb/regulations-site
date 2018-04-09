'use strict';
var $ = require( 'jquery' );
var _ = require( 'underscore' );
var Backbone = require( 'backbone' );
Backbone.$ = $;

var AlertView = Backbone.View.extend( {
  el: '#update-alert'
} );

module.exports = AlertView;
