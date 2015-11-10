'use strict';

module.exports = function(grunt) {

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
        dev: {
            options: {
                paths: ['<%= env.frontEndPath %>/css/less'],
                compress: false,
                sourceMap: true,
                sourceMapFilename: '<%= env.frontEndPath %>/css/style.css.map',
                sourceMapBasepath: '<%= env.frontEndPath %>/css/less/',
                sourceMapURL: 'style.css.map'
            },
            files: {
                '<%= env.frontEndPath %>/css/style.css': '<%= env.frontEndPath %>/css/less/main.less'
            }
        }
    },

    /**
     * CSSMin: https://github.com/gruntjs/grunt-contrib-cssmin
     *
     * Minify CSS for production
     */
    cssmin: {
      target: {
        files: {
          '<%= env.frontEndPath %>/css/regulations.min.css': ['<%= env.frontEndPath %>/css/style.css']
        }
      }
    },
    /**
     * ESLint: https://github.com/sindresorhus/grunt-eslint
     *
     * Validate files with ESLint.
     */
    eslint: {
        target: [
          'Gruntfile.js',
          '<%= env.frontEndPath %>/js/source/*.js',
          '<%= env.frontEndPath %>/js/source/events/**/*.js',
          '<%= env.frontEndPath %>/js/source/models/**/*.js',
          '<%= env.frontEndPath %>/js/source/views/**/*.js'
        ]
    },

    /**
    * Browserify:
    *
    * Require('modules') in the browser/bundle up dependencies.
    */
    browserify: {
      dev: {
        files: {
          '<%= env.frontEndPath %>/js/built/regulations.js': ['<%= env.frontEndPath %>/js/source/regulations.js','<%= env.frontEndPath %>/js/source/regulations.js']
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
      }
    },

    uglify: {
      dist: {
        files: {
          '<%= env.frontEndPath %>/js/built/regulations.min.js': ['<%= env.frontEndPath %>/js/built/regulations.js']
        }
      }
    },

    mocha_istanbul: {
      coverage: {
        src: ['<%= env.frontEndPath %>/js/unittests/specs/**/*'],
        options: {
          mask:'**/*-spec.js',
          coverageFolder: '<%= env.frontEndPath %>/js/unittests/coverage',
          excludes: ['<%= env.frontEndPath %>/js/unittests/specs/**/*'],
          coverage: false
        }
      }
     },

    shell: {
      'build-require': {
        command: './require.sh'
      },

      'nose-chrome': {
        command: 'nosetests -s <%= env.testPath %> --tc=webdriver.browser:chrome --tc=testUrl:<%= env.testUrl %>',
        options: {
            stdout: false,
            stderr: true
        }
      },

      'nose-ie10': {
        command: 'nosetests -s <%= env.testPath %> --tc=webdriver.browser:ie10 --tc=testUrl:<%= env.testUrl %>',
        options: {
            stdout: false,
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
      js: {
        files: ['Gruntfile.js', '<%= env.frontEndPath %>/js/source/**/*.js'],
        tasks: ['eslint','browserify:dev']
      },
      css: {
        files: ['<%= env.frontEndPath %>/css/less/**/*.less'],
        tasks: ['less:dev']
      },
      options: {
        livereload: true
      }
    }
  });

  grunt.event.on('coverage', function( lcov, done ) {
    require('coveralls').handleInput( lcov, function( err ) {
      if ( err ) {
        return done( err );
      }
      done();
    });
  });
  /**
   * The above tasks are loaded here.
   */
  require('load-grunt-tasks')(grunt);

    /**
    * Create task aliases by registering new tasks
    * Let's remove `squish` since it's a duplicate task
    */
  grunt.registerTask('nose', ['shell:nose-chrome', 'shell:nose-ie10']);
  grunt.registerTask('test', ['eslint', 'mocha_istanbul', 'nose']);
  grunt.registerTask('test-js', ['eslint', 'mocha_istanbul']);
  grunt.registerTask('build', ['default', 'test-js']);
  grunt.registerTask('squish', ['browserify', 'uglify', 'less', 'cssmin']);
  grunt.registerTask('default', ['browserify', 'uglify', 'less', 'cssmin']);
};
