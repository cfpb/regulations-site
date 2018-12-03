# :warning: THIS REPO IS DEPRECATED (12/3/2018) :warning:
Please migrate to using [cfgov-refresh](https://github.com/cfpb/cfgov-refresh).

regulations-site
================

[![Build Status](https://travis-ci.org/cfpb/regulations-site.png?branch=master)](https://travis-ci.org/cfpb/regulations-site)

An interface for viewing regulations data. This project combines all of the
data from a parsed regulation and generates navigable, accessible HTML,
complete with associated information.

This repository is part of a larger project. To read about it, please see
[http://cfpb.github.io/eregulations/](http://cfpb.github.io/eRegulations/).

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
Django templates.

## Quick start

If you're familiar with Python and Node environments, after cloning this repo:

```bash
$ mkvirtualenv regsite
$ workon regsite
$ pip install -r requirements.txt
$ ./frontendbuild.sh
$ python manage.py runserver
```

### Python

Requirements are retrieved and/or build automatically via pip (see below).

* lxml - Used to convert strings into XML for processing
* requests - Client library for reading data from an API

If running tests:

* mock - makes constructing mock objects/functions easy
* django-nose - provides nosetest as a test runner
* nose-exclude - allows certain directories to be excluded from nose
* nose-testconfig - pass configuration data to tests; used to configure
  selenium tests
* coverage - provides test-coverage metrics

## Setup & Running

This project uses `requirements*.txt` files for defining dependencies, so you
can get up and running with `pip`:

```bash
$ pip install -r requirements.txt       # modules required for execution
$ pip install -r requirements_test.txt  # modules required for running tests
$ pip install -r requirements_dev.txt   # helpful modules for developers
```

With that, you can start the development server:
```bash
$ python manage.py runserver
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

The application's UI itself uses a number of dependencies that you can see in package.json. To start, we are going to be concerned with the foundations of the environment:

## Front end environment setup

### Node/npm

The front-end development environment relies on on Node (version 4+) and npm for package management. To install Node, we recommend [nvm](https://github.com/creationix/nvm):

```sh
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.30.2/install.sh | bash # install nvm and run it's setup scripts
nvm install 4 # install node 4
nvm alias default 4 # set node 4 as the default
```

Alternately you can install Node by:

- Install a binary or installer from http://nodejs.org/download/
- If you're on OS X, you can use [Homebrew](http://brew.sh/)

#### Global npm packages
You will need to install the Grunt command line interface using npm.

```sh
cd regulations-site
npm install -g grunt-cli
```

#### Installing dependencies
The rest of the dependencies you will need are managed by npm. Do:

```sh
npm install
```

#### Configuration JSON

In the root of the repository, copy ```example-config.json``` to ```config.json``` and edit as necessary. Grunt depends on these settings to carry out tasks.
- ```testURL``` is the environment that you would like tests to run on.
- ```frontEndPath``` is the path to the root of your codebase where the ```css/``` and ```js/``` directories are.
- ```testPath``` is the path to the functional test specs.

## Running the application

Once all of the Python and front end dependencies have been met, compile the CSS and JavaScript and start the server:

```sh
$ grunt
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

## Additional front end information

### Running Grunt tasks
There are a number of tasks configured in [Gruntfile.js](https://github.com/cfpb/regulations-site/blob/master/Gruntfile.js). On the last lines, you will find tasks that group subtasks into common goals. Running ```grunt build``` will run unit, functional and lint tests, and compress static assets. Its recommended that you run this task before deploying changes.

### Unit and Functional Tests
The Grunt build will run a suite of Selenium tests written in Python and a small suite of [Mocha.js](http://mochajs.org/) unit tests. All tests run in [Sauce Labs](https://saucelabs.com). These tests run as part of the ```grunt build``` tasks. To use these, a little extra environment setup is required.

#### Sauce Labs Configuration
After you create a [Sauce Labs](https://saucelabs.com) account:
- In your bash config (probably ```~/.bash_profile```), define two variables: ```$SAUCE_USERNAME``` and ```$SAUCE_ACCESS_KEY``` which house your username and access key from Sauce Labs.
- If you want to test a local or otherwise not publically available environment, download and run [Sauce Connect](https://saucelabs.com/docs/connect). If you do need Sauce Connect, you will need to start it before running tests/Grunt builds.
- Be sure that the Django server is running in the environment you want to test.

##### For functional tests
- They also require having the environment serving data from ```dummy_api/```. To start the dummy API, from the root of your repo, run ```./dummy_api/start.sh 0.0.0.0:8282```.
- The tests run using [nose](http://nose.readthedocs.org/en/latest/). If you wish to run the tests outside of the Grunt environment, you may by running ```nosetests regulations/uitests/*.py``` from the root of the repo.

##### For unit tests
- Unit tests do not require running the dummy API.
- To run the unit tests along with the functional tests: ```grunt test``` from the root of the repo.
- To run unit tests individually: ```grunt mocha_istanbul``` from the root of the repo.

### Font files

The CSS styles for this project refer to some font files which cannot be distributed publicly (see definitions in `regulations/static/regulations/css/less/fonts.less`). These fonts need to live under a `fonts` subdirectory of wherever static assets are served from, e.g. `/static/fonts`. There are fallback fonts defined which will be used if the desired fonts are not available.

If you want to install self-hosted fonts locally for use in development, you can place the font files in repo subdirectory `static.in/cfgov-fonts/fonts/` and restart the local web server. If you are a CFPB employee, you can perform this step with:

```
cd static.in/ && git clone https://[GHE]/CFGOV/cfgov-fonts/
```
where `[GHE]` is our GitHub Enterprise URL.

See the [cfgov-refresh Webfonts documentation](https://cfpb.github.io/cfgov-refresh/installation/#webfonts) for a similar setup.

## Configuration

### Update notices

Define an `EREGS_REGULATION_UPDATES` Django setting in order to temporarily place a notice on the landing page of regulations that are in the process of being updated. For example, to turn on this notice for regulations for part 1003 and part 1005, define:

```py
# in your Django settings file
EREGS_REGULATION_UPDATES = ['1003', '1005']
```

Content for this notice can be found in `regulations/templates/regulations/generic_landing.html`.
