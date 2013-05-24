# Regulations Client-side App

## Intro
- App inits in js/regulations.js
- Data module is Backbone.RegModel in js/regs-data.js
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
- Extends Backbone.Model to Backbone.RegModel for custom data handling with a Backbonesque API

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

## Diff between Backbone.Model and Backbone.RegModel
Backbone.RegModel extends Backbone.Model, but implements its own logic and alters the API slightly in areas.

Backbone.RegModel effectively removes Backbone.Model.sync

Backbone.RegModel.set will only take an object and does not accept options as a second optional parameter

Since Backbone.RegModel.get has similar logic to Backbone.Model.fetch, Backbone.RegModel.fetch is simply another way to call Backbone.RegModel.get.

Backbone.RegModel adds:

Backbone.RegModel.request is the interface through which the app asks the server for content.

Backbone.RegModel.getChildren and Backbone.RegModel.getParent determine and return the appropriate content based on the ID passed in. To avoid the complexity of preserving the full tree on the front end, we rely on formatting to determine family objects only when necessary.

## Backbone.View and You
RegsView extends Backbone.View. Currently, DefinitionView and InterpretationView extend RegsView. RegsView sets up init and render methods that align with the inline display of these content types. It will expand to include content that is surfaced in a similar manner.

### What should/shouldn't be in Backbone Views
The only DOM-related JS that does not live within Backbone constructs are the jQuery event listeners and handlers in app-init.js. They are separate because the event handlers create Backbone Views.

When possible, we should create Backbone Views to handle DOM manipulation. If cases arise where a simple event handler is not the solution and a View doesn't make sense, we should introduce another structure. 

All JS files should be Require modules. All distinct pieces of functionality should be their own module. 

## Require Modules
Each new JS file should be a Require module. Typically, you'll want to wrap the contents of your module in a call to `define()`. Anatomy of a `define` call:
```javascript
define("module-name", ["jquery", "underscore", "backbone", "modules/helpful-module"], function($, _, Backbone, helpfulModule) {
    var stuff = function() {
        // do things.
        // this could also have been an object literal
    }

    // return value is the module source
    return stuff;
});
```
or, if you prefer:
```javascript
define(module name, array of dependencies, anon function that receives dependencies as params)
```

jQuery, Underscore and Backbone's paths are defined globally. For other modules, you will want to specify the path to the module relative to front_end/js without appending the ".js" to the end of the filename. Example: "modules/helpful-module" would point to "front_end/js/modules/helpful-module.js".

## Questions Theresa has asked herself
Q: Why don't we create new model instances for each paragraph? Why don't we initialize Backbone Views for each of those paragraphs on load?
A: I haven't found a way to test this, but it seems a safe assessment that its non-trivial and unecessary overhead to create, manage and destroy instances which may or may not ever be interacted with by the user.

Q: Should we load all of the content into the app on load?
A: No. The vast majority of users will only need to access a fraction of the content available in a reg. Moreover, even on shorter regs, like Reg E, before the page is cached in the browser, even scrolling can be very janky. 

Q: Would we benefit from AMD modules?
A: Yes. As more features are added to the app, chances are that any single user won't leverage all of them. Loading them only as necessary respects the user's time and resources. Additionally, it enforces decoupled and testable code.

Q: Should we just use Backbone.Model as is?
A: No. Backbone models are predicated on there being many instances in a collection, and serve to keep those instances in sync on the server. Part of the nice thing about Backbone is that it responds to certain common events and attempts this synchronization process without any intervention. The down side is that, if you have a one-way pipeline of data like we do, there are at best wasted cycles, at worst erroring code. Furthermore, given the size of the content trees we have and the likelihood that a user will touch enough pieces to warrant it, it doesn't make sense to build a nested model structure that represents the content tree as it exists. It would, afaik at this point, make content management needlessly complex.
