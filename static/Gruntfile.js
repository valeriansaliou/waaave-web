/*
 * Waaave
 * Static build tasks (uses GruntJS)
 *
 * Copyright 2013, Waaave
 * Author: Valerian Saliou <valerian@valeriansaliou.name>
 */


var _ = require('underscore');


module.exports = function(grunt) {

  // Known targets
  var GRUNT_TARGETS = ['development', 'testing', 'production'];


  // Configuration vars
  var CONF_COMPASS_OPTIONS = {
    development: {
      options: {
        config: 'config.rb',
        environment: 'development'
      }
    },

    production: {
      options: {
        config: 'config.rb',
        environment: 'production'
      }
    },
  };

  var CONF_COPY_FILES = {
    images: { expand: true, cwd: 'src/', src: ['**/images/**'], dest: 'build/' },
    fonts: { expand: true, cwd: 'src/', src: ['**/fonts/**'], dest: 'build/' },
    flashes: { expand: true, cwd: 'src/', src: ['**/flashes/**'], dest: 'build/' }
  };

  var CONF_COFFEE_FILES = {
    expand: true,
    cwd: 'src/',
    src: ['**/*.coffee'],
    dest: 'tmp/',
    ext: '.js'
  };

  var CONF_INCLUDES_FILES = {
    cwd: 'src/',
    src: ['**/*.js', '!**/_*.js'],
    dest: 'tmp/',
  };

  var CONF_CONCAT_FILES = [
    {
      expand: true,
      cwd: 'tmp/',
      src: ['**/*.js'],
      dest: 'build/',
      ext: '.js'
    },
  ];

  var CONF_UGLIFY_FILES = CONF_CONCAT_FILES;

  var CONF_IMAGEMIN_FILES = [
    {
      expand: true,
      cwd: 'build/',
      src: ['**/*.{png,jpg,jpeg}'],
      dest: 'build/'
    }
  ];


  // Project configuration
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),


    // Task: Watch
    watch: {
      options: {
        interval: 500
      },

      stylesheets: {
        files: ['src/**/stylesheets/**'],
        tasks: ['compass:development']
      },

      javascripts: {
        files: 'src/**/javascripts/**',
        tasks: ['includes', 'coffee', 'concat:development', 'clean:build']
      },

      images: {
        files: 'src/**/images/**',
        tasks: ['copy:images']
      },

      fonts: {
        files: 'src/**/fonts/**',
        tasks: ['copy:fonts']
      }
    },


    // Task: Clean
    clean: {
      reset: ['tmp/', 'build/*', '.sass-cache/'],
      build: ['tmp/'],
      lint: ['tmp/', '.sass-cache/']
    },


    // Task: CSSLint
    csslint: {
      all: {
        options: {
          /*
           * CSS Lint Options
           * Reference: https://github.com/gruntjs/grunt-contrib-csslint/blob/master/README.md#options
           */

          'important': false,
          'duplicate-background-images': false,
          'duplicate-properties': false,
          'star-property-hack': false,
          'adjoining-classes': false,
          'box-model': false,
          'qualified-headings': false,
          'unique-headings': false,
          'floats': false,
          'font-sizes': false,
          'gradients': false,
        },

        src: ['build/controllers/**/*.css', 'build/assets/**/*.css']
      }
    },


    // Task: Compass
    compass: {
      development: CONF_COMPASS_OPTIONS.development,
      testing: CONF_COMPASS_OPTIONS.development,
      production: CONF_COMPASS_OPTIONS.production
    },


    // Task: CoffeeScript
    coffee: {
      files: CONF_COFFEE_FILES
    },


    // Task: Copy
    copy: {
      flashes: { files: [CONF_COPY_FILES.flashes] },
      fonts: { files: [CONF_COPY_FILES.fonts] },
      images: { files: [CONF_COPY_FILES.images] }
    },


    // Task: Includes
    includes: {
      options: {
        includeRegexp: /\/\*\s*@include\s+['"]?([^'"]+)['"]?\s*\*\//,
        duplicates: false,
        filenamePrefix: '_',
        filenameSuffix: '.js'
      },

      files: CONF_INCLUDES_FILES
    },


    // Task: Concat
    concat: {
      options: {
        banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n\n'
      },

      development: { files: CONF_CONCAT_FILES },
      testing: { files: CONF_CONCAT_FILES }
    },


    // Task: Uglify
    uglify: {
      options: {
        report: 'min',
        banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n\n'
      },

      javascripts: {
        files: CONF_UGLIFY_FILES
      }
    },


    // Task: Imagemin
    imagemin: {
      production: {
        options: {
          optimizationLevel: 4
        },

        files: CONF_IMAGEMIN_FILES
      }
    }
  });


  // Load plugins
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-contrib-compass');
  grunt.loadNpmTasks('grunt-contrib-coffee');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-imagemin');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-csslint');
  grunt.loadNpmTasks('grunt-includes');


  // Map tasks
  var GRUNT_TASKS_BUILD = {
    development: [['includes',0], ['coffee',0], ['concat',1], ['compass',1], ['copy',0]],
    testing: [['includes',0], ['coffee',0], ['concat',1], ['compass',1], ['copy',0]],
    production: [['includes',0], ['coffee',0], ['uglify',0], ['compass',1], ['copy',0], ['imagemin',1]]
  };

  var GRUNT_TASKS_LINT = {
    css: [['csslint',0]]
  };


  // Register tasks
  grunt.registerTask('default', function() {
    return grunt.warn('Usage:' + '\n\n' + 'build - grunt build:target' + '\n' + 'clean - grunt clean:reset' + '\n\n');
  });

  grunt.registerTask('build', function(t) {
    if(!t) {
      return grunt.warn('Build target must be specified, like build:production.');
    } else if(GRUNT_TARGETS.indexOf(t) === -1) {
      return grunt.warn('Invalid build target name. Must be either: ' + GRUNT_TARGETS.join(', ') + '\n');
    }

    for(var i in GRUNT_TASKS_BUILD[t]) {
      grunt.task.run(GRUNT_TASKS_BUILD[t][i][0] + (GRUNT_TASKS_BUILD[t][i][1] ? (':' + t) : ''));
    }

    grunt.task.run('clean:build');
  });

  grunt.registerTask('lint', function(t) {
    grunt.task.run('clean:lint');

    var lint_t_all = [];

    if(!t) {
      for(t in GRUNT_TASKS_LINT) {
        lint_t_all.push(t);
      }
    } else if(typeof GRUNT_TASKS_LINT[t] != 'object') {
      return grunt.warn('Invalid lint target name.\n');
    } else {
      lint_t_all.push(t);
    }

    for(var c in lint_t_all) {
      t = lint_t_all[c];

      for(var i in GRUNT_TASKS_LINT[t]) {
        grunt.task.run(GRUNT_TASKS_LINT[t][i][0] + (GRUNT_TASKS_LINT[t][i][1] ? (':' + t) : ''));
      }
    }
  });

  grunt.registerTask('dev', function() {
    grunt.task.run('build:development');
  });

  grunt.registerTask('rebuild', function() {
    grunt.task.run('clean:reset');
    grunt.task.run('dev');
  });

};
