var RegsApp = {
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
          if (key === 'label') {
            if (this.inventory.indexOf(jsonObj[key]['text']) === -1) {
              this.inventory.push(jsonObj[key]['text']);
            }
          }

          if (isEnumerableObject(jsonObj[key])) {
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
var isEnumerableObject = function(obj) {
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
