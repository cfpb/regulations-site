var require = {
    baseUrl: "front_end/js",
    waitSeconds: 200,
    paths: {
      underscore: './lib/underscore',
      backbone: './lib/backbone'
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
