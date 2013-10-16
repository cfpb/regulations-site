  require.config({
    "baseUrl": "/static/regulations/js/source",
      "paths": {
        jquery: './lib/jquery-1.9.1',
        underscore: './lib/underscore',
        backbone: './lib/backbone',
        samplejson: '../tests/grunt/js/fixtures/sample-json',
        'queryparams': './lib/backbone.queryparams',
        'jquery-scrollstop': './lib/jquery.scrollstop',
        'definition-view': './views/definition-view',
        'interpretation-view': './views/interpretation-view',
        'regs-fixed-el-view': './views/regs-fixed-el-view',
        'sub-head-view': './views/sub-head-view',
        'sidebar-module-view': './views/sidebar-module-view',
        'toc-view': './views/toc-view',
        'sidebar-view': './views/sidebar-view',
        'sidebar-head-view': './views/sidebar-head-view',
        'reg-view': './views/reg-view',
        'konami': './lib/konami',
        'analytics-handler': './views/analytics-handler-view',
        'header-view': './views/header-view',
        'section-footer-view': './views/section-footer-view',
        'drawer-view': './views/drawer-view',
        'history-view': './views/history-view',
        'search-view': './views/search-view',
        'sxs-list-view': './views/sxs-list-view',
        'sidebar-list-view': './views/sidebar-list-view',
        'sxs-view': './views/sxs-view',
        'search-results-view': './views/search-results-view',
        'main-view': './views/main-view',
        'permalink-view': './views/permalink-view'
      },
      "shim": {
        "underscore": {
          "exports": "_"
        },
        "backbone": {
          "deps": [
            "underscore"
          ],
          "exports": "Backbone"
        },
        'jquery-scrollstop': {
            deps: ['jquery']
        }
      }
  });

require(['../specs/regs-helpers-spec.js', '../specs/dispatch-spec.js', '../specs/reg-model-spec.js'], function() {
    if (window.mochaPhantomJS) { mochaPhantomJS.run(); }
    else { mocha.run(); }
});
