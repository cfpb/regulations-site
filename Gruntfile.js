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

    browserify: {
      dev: {
        files: {
          '<%= env.frontEndPath %>/js/built/regulations.js': ['<%= env.frontEndPath %>/js/source/regulations.js']
        },
        options: {
          transform: ['browserify-shim', 'debowerify'],
          browserifyOptions: {
            debug: true
          }
        }
      },
      dist: {
        files: {
          '<%= env.frontEndPath %>/js/built/regulations.js': ['<%= env.frontEndPath %>/js/source/regulations.js']
        },
        options: {
          transform: ['browserify-shim', 'debowerify'],
          browserifyOptions: {
            debug: false
          }
        }
      },
      tests: {
        files: {
          '<%= env.frontEndPath %>/js/unittests/compiled_tests.js': ['<%= env.frontEndPath %>/js/unittests/specs/*.js']
        },
        options: {
          watch: true,
          debug: true
        }
      }
    },

    uglify: {
      dist: {
        files: {
          '<%= env.frontEndPath %>/js/built/regulations.min.js': ['<%= env.frontEndPath %>/js/built/regulations.js']
        }
      }
    },

    mocha: {
      test: {
        src: ['<%= env.frontEndPath %>/js/unittests/runner.html'],
        options: {
          run: true,
        },
      },
    },

    shell: {
      'build-require': {
        command: './require.sh',
      },

      'nose-chrome': {
        command: 'nosetests -s <%= env.testPath %> --tc=webdriver.browser:chrome --tc=testUrl:<%= env.testUrl %>',
        options: {
            stdout: true,
            stderr: true
        }
      },

      'nose-ie10': {
        command: 'nosetests -s <%= env.testPath %> --tc=webdriver.browser:ie10 --tc=testUrl:<%= env.testUrl %>',
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
        files: ['Gruntfile.js', '<%= env.frontEndPath %>/css/less/**/*.less', '<%= env.frontEndPath %>/js/source/**/*.js'],
        tasks: ['less', 'browserify:dev']
      }
    }
  });

  /**
   * The above tasks are loaded here.
   */
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-shell');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-styleguide');
    grunt.loadNpmTasks('grunt-bower-task');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-browserify');
    grunt.loadNpmTasks('grunt-mocha');

    /**
    * Create task aliases by registering new tasks
    */
    grunt.registerTask('nose', ['shell:nose-chrome', 'shell:nose-ie10']);
    grunt.registerTask('test', ['jshint', 'nose', 'browserify:tests', 'mocha']);
    grunt.registerTask('build', ['squish', 'test']);
    grunt.registerTask('squish', ['browserify:dist', 'uglify', 'less']);
};
