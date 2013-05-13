# Regulations Client-side App

## Intro
- App inits in js/regulations.js
- Data module is js/regs-data.js
- Inline element parent controller* is js/regs-view.js
- Inline definitions controller* is js/definition-view.js
- Inline interpretations controller* is js/interpretation-view.js
- Global helpers in js/regs-helpers.js

## Tech stack
- Backbone, Underscore
- RequireJS with jQuery built in
- Vanilla RequireJS and jQuery 1.9.1 for unit tests (Jasmine and Require w/ jQuery onboard do not get along)
- Grunt
    - NPM dependency management
    - Jasmine tests
    - Recess and Uglify for minification and stuff
- Less CSS

## Doing stuff
- To run tests on the command line, "grunt jasmine" at the project root
- To run tests in the browser, use python -m SimpleHTTPServer and then load up 0.0.0.0:8000/front_end/js/tests/browser/_SpecRunner.html

## Current Direction
- Management of DOM manipulation, custom event triggers/handlers and URL routing via Backbone
- Custom data management module to replace Backbone's Model and Collection modules

## Goal
To manage data on the client in a way that:
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

## Overview of RegsData (5/13/13)
RegsData keeps two objects that it uses to determine what the deal is with fetching content. *RegsData.content* is an object whose contents are key = section or paragraph ID, value = contents of the corresponding section, including children. Hierarchy is not represented in RegsData.content, meaning that RegsData['2345-10'] and RegsData['2345-10-a-i'] are both valid.

It keeps an array in *RegsData.regStructure* that houses all of the sections and paragraphs that exist in the regulation that is in scope. For example, if we have section #2345 in the DOM, RegsData.regStructure will represent the full navigation. However, not all of the items might have their content loaded into the app. RegsData.content might have a value for '2345-1', which is also in RegsData.regStructure, but not for '2345-9'.

*RegsData.parse* recurses through a JSON object to turn the generated tree into individual sections and paragraphs that the app can reference. Its currently pretty tightly coupled with the structure of the parsed tree.

*RegsData.store* creates a new key: value pair in RegsData.regStructure if necessary and returns the record.

*RegsData.isLoaded* returns the requested content if it exists in RegsData.content. We should think carefully if we find ourselves calling isLoaded() outside of RegsData.

*RegsData.retrieve* is probably going to be the most common way to interact with the module. It determines whether the requested content is loaded via .isLoaded() and requests from the server if it doesn't. It will request JSON by default, but 'markup' will also be a valid option. 

*RegsData.request* predictably will ask the server for content.

*RegsData.getChildren and RegsData.getParent* determines and returns the appropriate content based on the ID passed in. To avoid the complexity of preserving the full tree on the front end, we rely on formatting to determine family objects only when necessary.
