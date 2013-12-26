define('sidebar-model', ['underscore', 'backbone', 'meta-model'], function(_, Backbone, MetaModel) {
    'use strict';

    var SidebarModel = MetaModel.extend({
        supplementalPath: 'sidebar'
    });

    return SidebarModel;
});
