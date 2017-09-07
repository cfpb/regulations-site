'use strict';
var _ = require( 'underscore' );
var Backbone = require( 'backbone' );
var MetaModel = require( './meta-model' );

Backbone.DefinitionModel = MetaModel.extend( {} );

var definitionModel = new Backbone.DefinitionModel( {
  supplementalPath: 'definition'
} );

module.exports = definitionModel;
