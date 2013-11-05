This repository is part of a larger project. To read about it, please see http://eregs.github.io/eregulations/.

## JavaScript Application Environment
The front end of the site uses a number of JavaScript libraries and frameworks to create the unique experience of navigating and reading a regulation, as you can see at http://consumerfinance.gov/eregulations. If you'd like to modify the JavaScript layer, you should set up the build and testing environment.

If you run the application with ```env = "built"``` in your ```local_settings.py``` and would like to use the UI as it ships with this project, you can skip this.

The application's UI itself uses a number of dependencies that you can see in package.json and bower.json. To start, we are going to be concerned with the foundations of the environment:

- npm, a package manager to install dependencies in the development environment: https://npmjs.org/
- Grunt, a task runner that modules to build and run tests depend on: http://gruntjs.com/
- Bower, a utility to fetch dependencies for the: UI http://bower.io/
- Phantom, a headless browser to run unit and functional tests in: http://phantomjs.org/
- Casper, a utility to execute functional tests: http://casperjs.org/

### Environment setup
#### Node/npm
First we will need npm. npm ships with Node.js. If you don't already have it installed, please grab and install a binary from http://nodejs.org/download/.

#### Global npm packages
You will need to install the Grunt command line interface and Bower globally using npm. 
If you already have a different version of phantomjs installed, its probably ok. The version specified is known to work with this codebase, though.
```
npm install -g grunt-cli bower phantomjs@1.9.2-2
```

#### Casper installation

