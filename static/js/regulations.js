var Regs = {
  data: {
    inventory: [],
    content: {},

    loadFromDOM: function($el) {
      // traverse dom starting at $el
      // create a tree from all IDed els?
    },

    set: function(jsonObj) {
      // add object as reg entity
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
      if (this.inventory.indexOf(id) !== -1) {
        return this.content[id];
      }
      return false;    
    },

    retrieve: function(id, format) {
      var format = format || 'json',
          obj = this.isLoaded(id) || this.request(id, format);
      if (format === 'json') return obj;
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

// var Regs = Regs.data.loadFromDOM('#reg-container');

$(document).ready(function() {
  if (typeof JSONObj !== 'undefined') {
    var regE = Regs.data.set(JSONObj); 
  }
});
