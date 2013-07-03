// For Grunt RequireJS Optimizer, front_end/js/source -> front_end/js/built 
({
    paths: {
        jquery: './lib/jquery-1.9.1',
        underscore: './lib/underscore',
        backbone: './lib/backbone',
        'jquery-scrollstop': './lib/jquery.scrollstop',
        'definition-view': './views/definition-view',
        'regs-fixed-el-view': './views/regs-fixed-el-view',
        'sub-head-view': './views/sub-head-view',
        'regs-view': './views/regs-view',
        'toc-view': './views/toc-view',
        'sidebar-view': './views/sidebar-view',
        'sidebar-head-view': './views/sidebar-head-view',
        'content-view': './views/content-view',
        'konami': './lib/konami'
    },
    shim: {
        underscore: {
            deps: ['jquery'],
            exports: '_'
        },
        backbone: {
            deps: ['underscore', 'jquery'],
            exports: 'Backbone'
        },
        konami: {
            exports: 'Konami'
        }
    },
    dir: 'front_end/js/built',
    modules: [ {name: 'regulations'} ]
});
