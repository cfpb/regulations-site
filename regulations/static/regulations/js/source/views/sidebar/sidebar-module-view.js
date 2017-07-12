'use strict';
var $ = require( 'jquery' );
var _ = require( 'underscore' );
var Backbone = require( 'backbone' );
var RegModel = require( '../../models/reg-model' );
Backbone.$ = $;

var SidebarModuleView = Backbone.View.extend( {
  initialize: function() {
    var field;
    this.model = {};

    for ( field in this.options ) {
      if ( this.options.hasOwnProperty( field ) ) {
        this.model[field] = this.options[field];
      }
    }

    this.model.content = RegModel.get( this.model.id, this.render );

    return this;
  },

  render: function() {
    this.$el.html( this.model.content );
  }
} );

module.exports = SidebarModuleView;
