'use strict';
var _ = require( 'underscore' );
var Backbone = require( 'backbone' );
var MetaModel = require( './meta-model' );

Backbone.SxSModel = MetaModel.extend( {} );

var sxsModel = new Backbone.SxSModel( {
  supplementalPath: 'sxs'
} );

module.exports = sxsModel;
