var RegsApp = {
  model: {
    inventory: [],
    content: {},

    loadFromDOM: function($el) {
      // traverse dom starting at $el
      // create a tree from all IDed els?
    },

    set: function(jsonObj) {
      // add json objects as model instances
      var workingObj;

      if (typeof jsonObj === 'object') {
        for (var key in jsonObj) {
          if (key === 'label') {
            workingObj = jsonObj[key];
            if (this.inventory.indexOf(workingObj['text']) === -1) {
              this.inventory.push(workingObj['text']);
              this.content[workingObj['text']] = jsonObj['text'];
            }
          }

          if (isIterable(jsonObj[key])) {
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

// very naive helper function
var isIterable = function(obj) {
  if (typeof obj === 'array' || typeof obj === 'object') {
    return true;
  }
  return false;
};

// var Regs = RegsApp.model.loadFromDOM('#reg-container');

$(document).ready(function() {
  if (typeof JSONObj !== 'undefined') {
    var regE = RegsApp.model.set(JSONObj); 
  }
});
