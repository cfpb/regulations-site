define("regs-data", ["underscore", "backbone", './regs-helpers'], function(_, Backbone, RegsHelpers) {
    "use strict";

    // represents a whole regulation
    Backbone.RegModel = Backbone.Model.extend({
        regStructure: [],
        content: {},

        parse: function(jsonObj) {
            var workingObj;
            if (typeof jsonObj === 'object') {
                for (var key in jsonObj) {
                    if (key === 'label') {
                        workingObj = jsonObj[key];
                        workingObj['content'] = jsonObj['text'];
                        this.set(workingObj);
                    }

                    if (RegsHelpers.isIterable(jsonObj[key])) {
                        this.parse(jsonObj[key]);
                    }
                } 
            }

            return this;
        },

        set: function(obj) {
            var label = obj['text'],
                record,
                cached = this.has(label);

            if (!(cached)) {
                this.content[label] = obj['content'];
                record = obj['content'];

                if (_.indexOf(this.regStructure, label) === -1) {
                    this.regStructure.push(label);
                }
            }
            else {
                record = cached;
            }

            return record; 
        },

        has: function(id) {
            if (this.content[id]) {
                return this.content[id];
            }
            return false;    
        },

        get: function(id, format, withChildren) {
            var format = format || 'json',
                withChildren = withChildren || false,
                obj = this.has(id) || this.request(id, format);
            return obj;
        },

        fetch: function(id, format, withChildren) {
            return this.get(id, format, withChildren);
        },

        // stub for talking to api
        request: function(id, format) {
            return "this is where we'd load the api response for " + id + " in " + format + " format.";
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
        },

        // we don't have need for:
        sync: function() {
            return;
        },

        save: function() {
            return;
        },

        destroy: function() {
            return;
        }
    });

    var reg = new Backbone.RegModel();

    return reg;
});
