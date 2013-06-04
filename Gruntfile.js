module.exports = function(grunt) {

  'use strict';

  grunt.initConfig({

    /**
     * Pull in the package.json file so we can read its metadata.
     */
    pkg: grunt.file.readJSON('package.json'),

    /**
     * Recess: https://github.com/sindresorhus/grunt-recess
     * 
     * Compile, concat and compress LESS files.
     * Make sure to add any other CSS libraries/files you'll be using.
     * We are excluding minified files with the final ! pattern.
     */
    recess: {
      dist: {
        src: ['front_end/css/less/normalize.css', 'front_end/css/less/fonts.css', 'front_end/css/less/main.less', '!front_end/css/*.min.css'],
        dest: 'front_end/css/style.min.css',
        options: {
          compile: true,
          compress: true
        }
      }
    },

    /**
     * Uglify: https://github.com/gruntjs/grunt-contrib-uglify
     * 
     * Minify JS files.
     * Make sure to add any other JS libraries/files you'll be using.
     * We are excluding minified files with the final ! pattern.
     */
    uglify: {
      options: {
        banner: '<%= banner %>'
      },
      dist: {
        src: ['front_end/js/jquery-1.9.1.js', 'front_end/js/<%= pkg.name %>.js', '!front_end/js/*.min.js'],
        dest: 'front_end/js/<%= pkg.name %>.min.js'
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
        sub: true,
        undef: true,
        unused: true,
        boss: true,
        eqnull: true,
        browser: true,
        globals: {
          jQuery: true,
          $: true,
          Backbone: true,
          _: true,
          module: true,
          Highcharts: true
        }
      },
      all: ['front_end/js/<%= pkg.name %>.js']
    },

    /**
     * Jasmine: https://github.com/gruntjs/grunt-contrib-jasmine
     * 
     * Run jasmine specs headlessly through PhantomJS.
     * jQuery and Jasmine jQuery is included for your pleasure: https://github.com/velesin/jasmine-jquery
     */
    jasmine: {
      all: {
        src: 'front_end/js',
        options: {
          template: require('grunt-template-jasmine-requirejs'),
          specs: 'front_end/js/tests/specs/*.js',
          templateOptions: {
            requireConfig: {
              baseUrl: 'front_end/js',
              paths: {
                underscore: './lib/underscore',
                backbone: './lib/backbone',
                jquery: './lib/jquery-1.9.1',
                samplejson: './tests/grunt/js/fixtures/sample-json',
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
        files: ['Gruntfile.js', '<%= recess.dist.src %>', 'front_end/css/*.less','<%= uglify.dist.src %>', '<%= jasmine.options.specs %>'],
        tasks: ['default']
      }
    },

    requirejs: {
        compile: {
            options: {
                baseUrl: 'front_end/js',
                mainConfigFile: 'front_end/js/build.js',
                dir: "front_end/js/built",
                modules: [ {name: "regulations"} ],
                paths: {
                    jquery: './lib/jquery-1.9.1',
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
                        deps: ['jquery'],
                        exports: '_'
                    },
                    backbone: {
                        deps: ['underscore', 'jquery'],
                        exports: 'Backbone'
                    }
                },
            }
        }
    }
  });

  /**
   * The above tasks are loaded here.
   */
    grunt.loadNpmTasks('grunt-recess');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-jasmine');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-notify');
    grunt.loadNpmTasks('grunt-contrib-requirejs');
    /**
    * Create task aliases by registering new tasks
    */
    grunt.registerTask('test', ['jshint', 'jasmine']);

  /**
   * The 'default' task will run whenever `grunt` is run without specifying a task
   */
  grunt.registerTask('default', ['test', 'recess', 'uglify']);
    grunt.registerTask('build', ['test', 'requirejs']);

};
