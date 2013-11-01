define('sxs-model', ['underscore', 'backbone', './meta-model'], function(_, Backbone, MetaModel) {
    'use strict';

    Backbone.SxSModel = MetaModel.extend({});

    var sxsModel = new Backbone.SxSModel({
        supplementalPath: 'sxs'
    });

    return sxsModel;
});
