# Regs Data

## Intro
- App inits in static/js/regulations.js
- Data module is static/js/regs-data.js
  - Deps: regs-helpers.js, sample-json.js

## Tech stack
- RequireJS with jQuery built in
- Grunt
- Jasmine
  - When you run specs, for now you'll see an error like "Illegal path or script error: ['jquery']". I think this has to do with us using the RequireJS with jQuery built in. All specs should run fine, though.

## Dependencies
- If you have the Grunt packages installed already, you should just be able to "npm install" at the project root and get all dependencies

## Doing stuff
- To run tests, "grunt jasmine" at the project root

## Goal
To experiment and test solutions for managing data on the client in a way that:
- is flexible for any type of pairing of content
- minimizes DOM traversal for performance
- minimizes API calls for performance
- can use data stored both in cache and in the DOM to give content different presentation attributes based on user input
