var require = {
    baseUrl: "front_end/js",
    waitSeconds: 200,
    paths: {
        underscore: './lib/underscore',
        backbone: './lib/backbone',
        'definition-view': './views/definition-view',
        'interpretation-view': './views/interpretation-view',
        'regs-fixed-el-view': './views/regs-fixed-el-view',
        'sub-head-view': './views/sub-head-view',
        'regs-view': './views/regs-view',
        'toc-view': './views/toc-view'
    },
    shim: {
        underscore: {
        exports: '_'
    },
    backbone: {
        deps: ['underscore'],
        exports: 'Backbone'
    }
    }
};
