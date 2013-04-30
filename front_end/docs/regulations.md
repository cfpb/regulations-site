# Regulations Client-side App

## Intro
- App inits in static/js/regulations.js
- Data module is static/js/regs-data.js
  - Deps: regs-helpers.js, sample-json.js
- Definitions controller* is static/js/definition-view.js
  - Deps: regs-data.js

## Tech stack
- Backbone, Underscore
- RequireJS with jQuery built in
- Vanilla RequireJS and jQuery 1.9.1 for unit tests (Jasmine and Require w/ jQuery onboard do not get along)
- Grunt
- Jasmine

## Dependencies
- If you're new to Grunt, ask Theresa about it. 
- If you have the Grunt packages installed already, you should just be able to "npm install" at the project root and get all dependencies

## Doing stuff
- To run tests on the command line, "grunt jasmine" at the project root
- To run tests in the browser, use python -m SimpleHTTPServer and then load up 0.0.0.0:8000/tests/browser/_SpecRunner.html

## Current Direction
- Management of DOM manipulation, custom event triggers/handlers and URL routing via Backbone
- Custom data management module to replace Backbone's Model and Collection modules

## Goal
To experiment and test solutions for managing data on the client in a way that:
- is flexible for any type of pairing of content
- minimizes DOM traversal for performance
- minimizes API calls for performance
- can use data stored both in cache and in the DOM to give content different presentation attributes based on user input
- to accept data from the server in either html and json, to be extensible for other input
- to keep the DOM light enough so that the user has a fluid experience

## Notes
- * Controller = Backbone View. I find "View" a misnomer.

## Env - Ubuntu
- $ Fork, checkout
- $ sudo add-apt-repository ppa:chris-lea/node.js
- $ sudo apt-get update
- $ sudo apt-get install nodejs
- $ npm install -g grunt-cli grunt-init
- $ cd to/repo
- $ npm install
- $ grunt jasmine (to test that all is well, specs should run)
- If it cries about PhantomJS when you try to run 'grunt jasmine', do the following
- sudo apt-get install phantomjs

## Env - OSX
- $ Fork, checkout
- $ brew install node
- $ npm install -g grunt-cli grunt-init
- $ cd to/repo
- $ npm install
- $ grunt jasmine (to test that all is well, specs should run)
