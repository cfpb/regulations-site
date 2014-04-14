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
                paths: ['<%= env.frontEndPath %>/css/less'],
                yuicompress: true
            },
            files: {
                "<%= env.frontEndPath %>/css/style.min.css": "<%= env.frontEndPath %>/css/less/main.less"
            }
        }
    },

    styleguide: {
            dist: {
                options: {
                    name: 'eRegs Styleguide'
                },
                files: {
                    '<%= env.frontEndPath %>/docs/styleguide': '<%= env.frontEndPath %>/css/'
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
      all: ['<%= env.frontEndPath %>/js/source/*.js', '<%= env.frontEndPath %>/js/source/views/*.js', '<%= env.frontEndPath %>/js/source/views/*/*.js', '!<%= env.frontEndPath %>/js/source/require.config.js']
    },

    requirejs: {
        compile: {
            options: {
                baseUrl: '<%= env.frontEndPath %>/js/source',
                dir: "<%= env.frontEndPath %>/js/built",
                modules: [ {name: "regulations"} ],
                paths: grunt.file.readJSON('require.paths.json'),
                shim: grunt.file.readJSON('require.shim.json'),
                skipDirOptimize: true,
                optimizeCss: 'none',
                removeCombined: 'true'
            }
        }
    },

    shell: {
      'build-require': {
        command: './require.sh',
      },

      'nose-chrome': {
        command: 'nosetests -s <%= env.testPath %> --tc=webdriver.browser:chrome',
        options: {
            stdout: true,
            stderr: true
        }
      },

      'nose-ie10': {
        command: 'nosetests -s <%= env.testPath %> --tc=webdriver.browser:ie10',
        options: {
            stdout: true,
            stderr: true
        }
      },

      'run-mocha-tests': {
        command: '<%= env.frontEndPath %>/js/unittests/sauce_unit_tests.sh',
        options: {
            stdout: true,
            stderr: true
        }
      }
    },

    // https://github.com/yatskevich/grunt-bower-task
    bower: {
        install: {
            options: {
                targetDir: '<%= env.frontEndPath %>/js/source/lib'
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
        files: ['Gruntfile.js', '<%= env.frontEndPath %>/css/less/*.less', '<%= env.frontEndPath %>/css/less/module/*.less', '<%= env.frontEndPath %>/css/less/media-queries/breakpoints/*.less','<%= env.frontEndPath %>/js/tests/specs/*.js', '<%= env.frontEndPath %>/js/source/*.js', '<%= env.frontEndPath %>/js/source/views/*.js', '<%= env.frontEndPath %>/js/source/views/*/*.js', '<%= env.frontEndPath %>/js/tests/functional/*.js'],
        tasks: ['less']
      }
    }
  });

  /**
   * The above tasks are loaded here.
   */
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-shell');
    grunt.loadNpmTasks('grunt-contrib-requirejs');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-styleguide');
    grunt.loadNpmTasks('grunt-bower-task');

    /**
    * Create task aliases by registering new tasks
    */
    grunt.registerTask('nose', ['shell:nose-chrome', 'shell:nose-ie10']);
    grunt.registerTask('test', ['jshint', 'nose', 'shell:run-mocha-tests']);
    grunt.registerTask('build', ['squish', 'test']);
    grunt.registerTask('squish', ['requirejs', 'less']);
};
