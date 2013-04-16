var RegsApp = {
  state: {
    // open defintions 
    // location: definition
    definitions: {
      '1005-3': '1005-2-a-1'
    }
  },
  layout: {},

  model: {
    inventory: [],

    loadFromDOM: function($el) {
      // traverse dom starting at $el
      // create a tree from all IDed els?
    },

    set: function(jsonObj) {
      // designate a json object as the model
      if (typeof jsonObj === 'object') {
        for (var key in jsonObj) {
          this.inventory.push(key);
          if (typeof jsonObj[key] === 'object') {
            this.set(jsonObj[key]);
          }
        } 
      }            
    },

    isLoaded: function(id) {
      // return boolean 
      // is piece of content loaded in app?
    },

    retrieve: function(id, format) {
      // determine if content is loaded locally
      // if not, request from server
      // format = json or html
    }
  } 
};


// var Regs = RegsApp.model.loadFromDOM('#reg-container');

var JSONObj = JSON.stringify({
  '1005': {
    '1005.1': {
      'a': 'baslfkjas;dlkfjals;kdfj',
      'b': {
        'i': 'sdfslkdjfsalkdf',
        'ii': 'sdkflsjdfkls'
      },
      'c': 'sdfsdfsdf'
    },

    '1005.3': {
      'a': 'sdfklsjdflksdf',
      'b': 'asdlfkjsdfk'
    }
  }
});

$(document).ready(function() {
  var regE = RegsApp.model.set(JSON.parse(JSONObj)); 
});
