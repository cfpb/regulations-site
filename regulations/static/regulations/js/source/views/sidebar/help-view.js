'use strict';
var $ = require( 'jquery' );
var _ = require( 'underscore' );
var Backbone = require( 'backbone' );
Backbone.$ = $;

var HelpView = Backbone.View.extend( {
  el: '#help'
} );

module.exports = HelpView;
