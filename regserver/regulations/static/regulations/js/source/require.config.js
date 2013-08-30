var require = {
    paths: {
        jquery: './lib/jquery-1.9.1',
        underscore: './lib/underscore',
        backbone: './lib/backbone',
        'jquery-scrollstop': './lib/jquery.scrollstop',
        'jquery-cookie': './lib/jquery.cookie',
        'definition-view': './views/definition-view',
        'regs-fixed-el-view': './views/regs-fixed-el-view',
        'sub-head-view': './views/sub-head-view',
        'sidebar-module-view': './views/sidebar-module-view',
        'toc-view': './views/toc-view',
        'sidebar-view': './views/sidebar-view',
        'sidebar-head-view': './views/sidebar-head-view',
        'content-view': './views/content-view',
        'konami': './lib/konami',
        'analytics-handler': './views/analytics-handler-view',
        'header-view': './views/header-view',
        'section-footer-view': './views/section-footer-view',
        'drawer-view': './views/drawer-view',
        'history-view': './views/history-view',
        'search-view': './views/search-view',
        'sxs-list-view': './views/sxs-list-view',
        'sidebar-list-view': './views/sidebar-list-view',
        'sxs-view': './views/sxs-view'
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
    }
};
