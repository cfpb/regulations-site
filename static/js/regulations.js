var Regs = {
  data: {
    inventory: [],
    content: {},

    loadFromDOM: function($el) {
    },

    parse: function(jsonObj) {
      var workingObj;
      if (typeof jsonObj === 'object') {
        for (var key in jsonObj) {
          if (key === 'label') {
            workingObj = jsonObj[key];
            workingObj['content'] = jsonObj['text'];
            this.store(workingObj);
          }

          if (isIterable(jsonObj[key])) {
            this.parse(jsonObj[key]);
          }
        } 
      }
    },

    store: function(obj) {
      var label = obj['text'],
          record,
          cached = this.isLoaded(label);

      if (!(cached)) {
        this.inventory.push(label);
        this.content[label] = obj['content'];
        record = obj['content'];
      }
      else {
        record = cached;
      }

      return record; 
    },

    isLoaded: function(id) {
      if (this.inventory.indexOf(id) !== -1) {
        return this.content[id];
      }
      return false;    
    },

    retrieve: function(id, format, withChildren) {
      var format = format || 'json',
          withChildren = withChildren || false,
          obj = this.isLoaded(id) || this.request(id, format);
      if (format === 'json') return obj || false;
    },

    getChildren: function(id) {
      var kids = [],
          inventoryLen = this.inventory.length,
          regex = new RegExp(id + "[\-,a-z,0-9]");

      while (inventoryLen--) {
        if (regex.test(this.inventory[inventoryLen])) {
          kids.push(this.inventory[inventoryLen]);
        } 
      }

      return kids;
    },

    getParent: function(id) {
      var parent, z;
      z  = id.split('-');
      z.pop();
      parent = z.join('-');

      if (this.inventory.indexOf(parent) !== -1) {
        return this.content[parent];
      }

      return false;
    }
  } 
};

var isIterable = function(obj) {
  if (typeof obj === 'array' || typeof obj === 'object') {
    return true;
  }
  return false;
};

// var Regs = Regs.data.loadFromDOM('#reg-container');

$(document).ready(function() {
  if (typeof JSONObj !== 'undefined') {
    var regE = Regs.data.parse(JSONObj); 
  }
});
