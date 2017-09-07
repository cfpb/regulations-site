// **Extends** MetaModel
//
// **Usage** ```require(['reg-model'], function(RegModel) {})```
//
// Currently represents the whole of a regulation.
// Not really in use until there's an API.
//
// The idea here is that Backbone Models are created with a certain type of content in mind.
// Content that:
//
// * there are many instances of with the same general properties (hence Collections)
// * that will be updated both on the server and client, frequently
//
// This is not the case with our content and so this module is intended as a replacement of
// Backbone's Model scheme
// The Backbone Model API should be kept as much as makes sense. Existing entities should
// be reused to aim for the effect of a native Backbone experience, but shouldn't try so hard
// as to be confusing. Ex. the return value of Model.fetch should be the same as in core Backbone,
// even if the internals are different

'use strict';
var $ = require( 'jquery' );
var _ = require( 'underscore' );
var Backbone = require( 'backbone' );
var RegsHelpers = require( '../helpers' );
var MetaModel = require( './meta-model' );
Backbone.$ = $;

// represents a whole regulation
Backbone.RegModel = MetaModel.extend( {
  // **Param**
  // ```id```: string, dash-delimited reg entity id
  //
  // **Returns** an array of strings, dash-delimited reg entity ids of children
  //
  // The magic of the flexibility of the app is that we can pass around these
  // dash-delimited ids and get the job done pretty seamlessly w/o worrying about
  // what exactly we're dealing with. We just rely on a set of rules.
  getChildren: function( id ) {
    var kids = [],
        structureLen = this.structure.length,
        regex = new RegExp( id + '[-,a-z,0-9]' );

    while ( structureLen-- ) {
      if ( regex.test( this.structure[structureLen] ) ) {
        kids.push( this.structure[structureLen] );
      }
    }

    return kids;
  },

  // **Param**
  // ```id```: string, dash-delimited reg entity id
  //
  // **Returns** string, dash-delimited reg entity id of parent to
  // the id passed in or boolean false if the requested id has no parent
  //
  // The converse of ```this.getChildren```
  getParent: function( id ) {
    var parent, z;
    z = id.split( '-' );
    z.pop();
    parent = z.join( '-' );

    if ( this.structure.indexOf( parent ) !== -1 ) {
      return this.content[parent];
    }

    return false;
  }
} );

var reg = new Backbone.RegModel();

module.exports = reg;
