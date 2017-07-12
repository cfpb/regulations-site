'use strict';
var _ = require( 'underscore' );
var Backbone = require( 'backbone' );
var MetaModel = require( './meta-model' );

Backbone.DiffModel = MetaModel.extend( {} );

var diffModel = new Backbone.DiffModel( {
  supplementalPath: 'diff'
} );

module.exports = diffModel;
