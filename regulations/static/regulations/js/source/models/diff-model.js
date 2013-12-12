define('diff-model', ['underscore', 'backbone', 'meta-model'], function(_, Backbone, MetaModel) {
    'use strict';
    Backbone.DiffModel = MetaModel.extend({});

    var diffModel = new Backbone.DiffModel({
        supplementalPath: 'diff'
    });

    return diffModel;
});
