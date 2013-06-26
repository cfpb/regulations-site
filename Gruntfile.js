module.exports = function(grunt) {

  'use strict';

  grunt.initConfig({

    /**
     * Pull in the package.json file so we can read its metadata.
     */
    pkg: grunt.file.readJSON('package.json'),

    /**
     *
     *  Pull in environment-specific vars
     *
     */
    env: grunt.file.readJSON('config.json'),

    /**
     * https://github.com/gruntjs/grunt-contrib-less
     */
    less: {
        development: {
            options: {
                paths: ['front_end/css/less', 'front_end/css/less/module'],
                yuicompress: true
            },
            files: {
                "front_end/css/style.min.css": "front_end/css/less/main.less"
            }
        }
    },

    /**
     * JSHint: https://github.com/gruntjs/grunt-contrib-jshint
     * 
     * Validate files with JSHint.
     * Below are options that conform to idiomatic.js standards.
     * Feel free to add/remove your favorites: http://www.jshint.com/docs/#options
     */
    jshint: {
      options: {
        camelcase: true,
        curly: true,
        eqeqeq: true,
        forin: true,
        immed: true,
        latedef: true,
        newcap: true,
        noarg: true,
        quotmark: true,
        undef: true,
        strict: true,
        unused: true,
        boss: true,
        browser: true,
        globalstrict: true,
        sub: true,
        globals: {
          jQuery: true,
          $: true,
          Backbone: true,
          _: true,
          require: true,
          define: true,
          subhead: true,
          toc: true,
          sidebar: true,
          regContent: true
        }
      },
      all: ['front_end/js/source/*.js', 'front_end/js/source/views/*.js', '!front_end/js/source/build.js', '!front_end/js/source/require.config.js']
    },

    /**
     * Jasmine: https://github.com/gruntjs/grunt-contrib-jasmine
     * 
     * Run jasmine specs headlessly through PhantomJS.
     * jQuery and Jasmine jQuery is included for your pleasure: https://github.com/velesin/jasmine-jquery
     */
    jasmine: {
      all: {
        src: 'front_end/js/source',
        options: {
          template: require('grunt-template-jasmine-requirejs'),
          specs: 'front_end/js/tests/specs/*.js',
          templateOptions: {
            requireConfig: {
              baseUrl: 'front_end/js/source',
              paths: {
                underscore: './lib/underscore',
                backbone: './lib/backbone',
                jquery: './lib/jquery-1.9.1',
                samplejson: '../tests/grunt/js/fixtures/sample-json',
                'jquery-scrollstop': './lib/jquery.scrollstop',
                'jquery-hoverIntent': './lib/jquery.hoverIntent',
                'definition-view': './views/definition-view',
                'interpretation-view': './views/interpretation-view',
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
                  exports: '_'
                },
                backbone: {
                  deps: ['underscore'],
                  exports: 'Backbone'
                },
                konami: {
                    exports: 'Konami'
                }
              }
            }
          }
        }
      }
    },

    /**
     * Watch: https://github.com/gruntjs/grunt-contrib-watch
     * 
     * Run predefined tasks whenever watched file patterns are added, changed or deleted.
     * Add files to monitor below.
     */
    watch: {
      gruntfile: {
        files: ['Gruntfile.js', '<%= recess.dist.src %>', 'front_end/css/*.less', '<%= jasmine.options.specs %>'],
        tasks: ['build']
      }
    },

    /**
     *
     * https://npmjs.org/package/grunt-ghost
     *
     * Functional testing w/ Phantom, Casper
     *
     */
    ghost: {
        dist: {
            filesSrc: ['front_end/js/tests/functional/*.js'],
            options: {
                args: {
                    testUrl: '<%= env.testUrl %>'
                },
                direct: true,
                verbose: true,
                logLevel: 'debug'
            }
        }
    },

    requirejs: {
        compile: {
            options: {
                baseUrl: 'front_end/js/source',
                mainConfigFile: 'front_end/js/source/build.js',
                dir: "front_end/js/built",
                modules: [ {name: "regulations"} ],
                paths: {
                    jquery: './lib/jquery-1.9.1',
                    underscore: './lib/underscore',
                    backbone: './lib/backbone',
                    'jquery-scrollstop': './lib/jquery.scrollstop',
                    'definition-view': './views/definition-view',
                    'interpretation-view': './views/interpretation-view',
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
                }
            }
        }
    }
  });

  /**
   * The above tasks are loaded here.
   */
    grunt.loadNpmTasks('grunt-contrib-jasmine');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-notify');
    grunt.loadNpmTasks('grunt-contrib-requirejs');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-ghost');

    /**
    * Create task aliases by registering new tasks
    */
    grunt.registerTask('test', ['jshint', 'jasmine']);
    grunt.registerTask('build', ['test', 'ghost', 'requirejs', 'less']);
    grunt.registerTask('squish', ['requirejs', 'less']);
};
