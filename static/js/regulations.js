var Regs = {
  data: {
    inventory: [],
    content: {},

    loadFromDOM: function($el) {
      // traverse dom starting at $el
      // create a tree from all IDed els?
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
      if (format === 'json') return obj;
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
