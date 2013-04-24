define("regs-data", ['./regs-helpers'], function(RegsHelpers) {
  return {
    regStructure: [],
    content: {},

    parse: function(jsonObj) {
      var workingObj;
      if (typeof jsonObj === 'object') {
        for (var key in jsonObj) {
          if (key === 'label') {
            workingObj = jsonObj[key];
            workingObj['content'] = jsonObj['text'];
            this.store(workingObj);
          }

          if (RegsHelpers.isIterable(jsonObj[key])) {
            this.parse(jsonObj[key]);
          }
        } 
      }

      return this;
    },

    store: function(obj) {
      var label = obj['text'],
          record,
          cached = this.isLoaded(label);

      if (!(cached)) {
        this.content[label] = obj['content'];
        record = obj['content'];

        if (this.regStructure.indexOf(label) === -1) {
          this.regStructure.push(label);
        }
      }
      else {
        record = cached;
      }

      return record; 
    },

    isLoaded: function(id) {
      if (this.content[id]) {
        return this.content[id];
      }
      return false;    
    },

    retrieve: function(id, format, withChildren) {
      var format = format || 'json',
          withChildren = withChildren || false,
          obj = this.isLoaded(id) || this.request(id, format);

      if (!obj) {
        throw new Error("Can't retrive this definition");
      }

      return obj;
    },

    // stub for talking to api
    request: function(id, format) {
      var content = {
        "2345-9-a-2": "klsdiuenjwkd",
        "2345-9-b-1": "sdflkjsdfkjsdklfj",
        "2345-9-b-2": "weoiruwoieruwioeur",
        "2345-9-c": "xmncbvnmxbcvmnxb" 
      };
      return content[id];
    },

    getChildren: function(id) {
      var kids = [],
          regStructureLen = this.regStructure.length,
          regex = new RegExp(id + "[\-,a-z,0-9]");

      while (regStructureLen--) {
        if (regex.test(this.regStructure[regStructureLen])) {
          kids.push(this.regStructure[regStructureLen]);
        } 
      }

      return kids;
    },

    getParent: function(id) {
      var parent, z;
      z  = id.split('-');
      z.pop();
      parent = z.join('-');

      if (this.regStructure.indexOf(parent) !== -1) {
        return this.content[parent];
      }

      return false;
    }
  }
});
