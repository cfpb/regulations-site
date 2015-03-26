regulations-site
================

[![Build Status](https://travis-ci.org/cfpb/regulations-site.png?branch=master)](https://travis-ci.org/cfpb/regulations-site)

An interface for viewing regulations data. This project combines all of the
data from a parsed regulation and generates navigable, accessible HTML,
complete with associated information.

This repository is part of a larger project. To read about it, please see 
[http://cfpb.github.io/eregulations/](http://cfpb.github.io/eregulations/).

## Features

* Navigability: Instead of the monolithic text usually used to represent
  regulations, proper indentation, spacing, etc., this presents the text in a
  clean, readable form.
* Inline Interpretations: Associated interpretations are displayed right
  along side the paragraph/section/appendix they are interpreting.
* Definitions: Defined terms are highlighted in the regulation text;
  clicking them opens the term's definition in the sidebar.
* Internal Citations: Citations to other parts of the same regulation are
  clickable links, allowing easy navigation within a regulation
* Alternate Versions of the Regulation: Quick access to versions of the
  regulation by browsing effective dates, or typing in an arbitrary date is
  provided.
* Comparing Versions: A "Diff-view" is provided to highlight additions and
  deletions between versions of the regulation.
* Section-by-Section Analysis: Analysis for regulation
  paragraphs/sections/appendices are provided in the sidebar. This analysis
  comes from Federal Register notice preambles.
* Additional Formatting Concerns: Tables, subscripts, notes, and even source
  code found within a regulation are rendered as appropriate markup.
* Responsive Design: The application design is responsive, adjusting to the
  device and screen size of the user.

## Screenshot

![eRegs](/regulations/static/regulations/img/easy-01.png)

## Requirements

This application lives in two worlds, roughly translating to a Python,
Django app, and a Backbone, Javascript app, which communicate through the
Django templates. To get started quickly, we provide a default, pre-compiled
version of the Javascript assets.

### Python

Requirements are retrieved and/or build automatically via buildout (see
below).

* zc-buildout - Tool used for building the application and handling
  dependencies
* lxml - Used to convert strings into XML for processing
* requests - Client library for reading data from an API

If running tests:

* mock - makes constructing mock objects/functions easy
* django-nose - provides nosetest as a test runner
* nose-exclude - allows certain directories to be excluded from nose
* nose-testconfig - pass configuration data to tests; used to configure
  selenium tests
* coverage - provides test-coverage metrics
* selenium - functional testing via a headless web browser

## Buildout

Buildout is a simple tool for building and distributing python applications
quickly. We use it to get a version of the API up and running without
needing all of the fuss usually associated with setting up Django. Just run

```bash
$ pip install zc.buildout
$ buildout
```

After downloading the internet, you'll notice that some helpful scripts are
located in ```bin```, including ```bin/django``` and ```bin/test```. The
latter will run our test suite while the former is equivalent to running
manage.py in a traditional Django environment.

Before starting the development server, you also need to specify the ```STATICFILES_DIRS```
and  ```STATIC_ROOT``` variables in your ```local_settings.py``` file.
Then run ```bin/django collectstatic``` to move all static resources into
your ```STATIC_ROOT``` directory.

With that, you can start the development server:
```bash
$ ./bin/django runserver
```

## Building the documentation

For most tweaks, you will simply need to run the Sphinx documentation
builder again.

```
$ ./bin/sphinx-build -b dirhtml -d docs/_build/doctrees/ docs/ docs/_build/dirhtml/
```

The output will be in ```docs/_build/dirhtml```.

If you are adding new modules, you may need to re-run the skeleton build
script first:

```
$ rm docs/regulations*.rst
$ ./bin/sphinx-apidoc -F -o docs regulations
```

## JavaScript Application 
### Code
The application code in JavaScript uses [Backbone.js](http://backbonejs.org/) as a foundation, though in some non-standard ways. If you plan to do work on this layer, it is recommended that you acquaint yourself with this [starter documentation](README_BACKBONE.md).

### Environment
The front end of the site uses a number of JavaScript libraries and frameworks to create the unique experience of navigating and reading a regulation, as you can see at http://consumerfinance.gov/eregulations. If you'd like to modify the JavaScript layer, you should set up the build and testing environment.

If you run the application with ```env = "built"``` in your ```local_settings.py``` and would like to use the UI as it ships with this project, you can skip this.

The application's UI itself uses a number of dependencies that you can see in package.json and bower.json. To start, we are going to be concerned with the foundations of the environment:

- npm, a package manager to install dependencies in the development environment: https://npmjs.org/
- Grunt, a task runner that modules to build and run tests depend on: http://gruntjs.com/
- Bower, a utility to fetch dependencies for the: UI http://bower.io/

### Environment setup
#### Node/npm
First we will need npm. npm ships with Node.js. If you don't already have it installed, there are a few ways to get it.
- You can grab and install a binary or installer from http://nodejs.org/download/
- If you're on OS X, you can use [Homebrew](http://brew.sh/) if that's your thing
- If you are using Ubuntu, the default apt-get package is out of date. Do:

```
sudo add-apt-repository ppa:chris-lea/node.js
sudo apt-get update
sudo apt-get install nodejs
```

If you receive an error about ```add-apt-repository``` not being found, do:

```
sudo apt-get install python-software-properties
```

#### Global npm packages
You will need to install the Grunt command line interface and Bower globally using npm. 
```
cd regulations-site
npm install -g grunt-cli bower
```

#### Installing dependencies
The rest of the dependencies you will need are managed by Bower and npm. Do:
```
npm install
bower install
```

#### Configuration JSON
In the root of the repository, copy ```example-config.json``` to ```config.json``` and edit as necessary. Grunt depends on these settings to carry out tasks.
- ```testURL``` is the environment that you would like tests to run on.
- ```frontEndPath``` is the path to the root of your codebase where the ```css/``` and ```js/``` directories are.
- ```testPath``` is the path to the functional test specs.

#### Running Grunt tasks
There are a number of tasks configured in [Gruntfile.js](https://github.com/cfpb/regulations-site/blob/master/Gruntfile.js). On the last lines, you will find tasks that group subtasks into common goals. Running ```grunt build``` will run unit, functional and lint tests, and compress static assets. Its recommended that you run this task before deploying changes. 

#### Unit and Functional Tests
The Grunt build will run a suite of Selenium tests written in Python and a small suite of [Mocha.js](http://visionmedia.github.io/mocha/) unit tests. All tests run in [Sauce Labs](https://saucelabs.com). These tests run as part of the ```grunt build``` tasks. To use these, a little extra environment setup is required.

##### Sauce Labs Configuration
After you create a [Sauce Labs](https://saucelabs.com) account:
- In your bash config (probably ```~/.bash_profile```), define two variables: ```$SAUCE_USERNAME``` and ```$SAUCE_ACCESS_KEY``` which house your username and access key from Sauce Labs.
- If you want to test a local or otherwise not publically available environment, download and run [Sauce Connect](https://saucelabs.com/docs/connect). If you do need Sauce Connect, you will need to start it before running tests/Grunt builds.
- Be sure that the Django server is running in the environment you want to test. 

###### For functional tests
- They also require having the environment serving data from ```dummy_api/```. To start the dummy API, from the root of your repo, run ```./dummy_api/start.sh 0.0.0.0:8282```.
- The tests run using [nose](http://nose.readthedocs.org/en/latest/). If you wish to run the tests outside of the Grunt environment, you may by running ```nosetests regulations/uitests/*.py``` from the root of the repo.

###### For unit tests
- To run unit tests individually: ```regulations/static/regulations/js/unittests/sauce_unit_tests.sh http://url.of/test/site``` from the root of the repo.
- Unit tests do not require running the dummy API.
- You may also run the unit tests locally with no additional configuration by loading the following URL in a web browser: ```http://your.site/static/regulations/js/unittests/runner.html```.
