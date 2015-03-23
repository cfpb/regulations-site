'use strict';
var _ = require('underscore');
var Backbone = require('backbone');
var MetaModel = require('./meta-model');

var SidebarModel = MetaModel.extend({
    supplementalPath: 'sidebar'
});

module.exports = SidebarModel;
