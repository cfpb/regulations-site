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
- Vanilla RequireJS and jQuery 1.9.1 for unit tests
- Grunt
- Jasmine

## Dependencies
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
