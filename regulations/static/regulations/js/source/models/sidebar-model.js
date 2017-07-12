'use strict';
var _ = require( 'underscore' );
var Backbone = require( 'backbone' );
var MetaModel = require( './meta-model' );

Backbone.SidebarModel = MetaModel.extend( {} );

var sidebarModel = new Backbone.SidebarModel( {
  supplementalPath: 'sidebar'
} );

module.exports = sidebarModel;
