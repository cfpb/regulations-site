// **Extends** Backbone.Model
//
// **Usage** ```require(['regs-data'], function(RegModel) {})```
//
// Currently represents the whole of a regulation.
// Not really in use until there's an API.
//
// The idea here is that Backbone Models are created with a certain type of content in mind.
// Content that:
//
// * there are many instances of with the same general properties (hence Collections)
// * that will be updated both on the server and client, frequently
//
// This is not the case with our content and so this module is intended as a replacement of 
// Backbone's Model scheme
// The Backbone Model API should be kept as much as makes sense. Existing entities should
// be reused to aim for the effect of a native Backbone experience, but shouldn't try so hard
// as to be confusing. Ex. the return value of Model.fetch should be the same as in core Backbone,
// even if the internals are different
define('regs-data', ['underscore', 'backbone', './regs-helpers', './regs-dispatch'], function(_, Backbone, RegsHelpers, Dispatch) {
    'use strict';

    // represents a whole regulation
    Backbone.RegModel = Backbone.Model.extend({
        // an index of all of the entities in the reg, whether or not they've been loaded
        regStructure: [],

        // content = markup to string representations of each reg paragraph/entity
        // loaded into the browser (rendered or not)
        content: {},

        // recurses over the parsed reg tree and creates an in-browser representation
        // of a reg. may or may not be functional based on current tree.
        // **TODO** was only useful for development. refactor into something useful or kill 
        parse: function(jsonObj) {
            var workingObj;
            if (typeof jsonObj === 'object') {
                for (var key in jsonObj) {
                    if (jsonObj.hasOwnProperty(key)) {
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
            }

            return this;
        },

        // store a new reg entity
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

        // **Param**
        // id, string, dash-delimited reg entity id
        //
        // **Returns** the markup string to render an entity or
        // false if the entity hasn't been loaded
        has: function(id) {
            if (this.content[id]) {
                return this.content[id];
            }
            return false;    
        },

        // **Params**
        // 
        // * ```id```: string, dash-delimited reg entity id
        //
        // **Returns** representation of the reg entity requested in the format requested,
        get: function(id) {
            var obj = this.has(id) || this.request(id);
            return obj;
        },

        // Basically an alias for ```this.get```, included for API continuity
        fetch: function(id, format, withChildren) {
            return this.get(id, format, withChildren);
        },

        request: function(id) {
            var url = '/partial/' + id + '/' + Dispatch.getVersion(),
                promise;

            promise = $.ajax({
                url: url,
                success: function(data) { this.set(data); }.bind(this)
            });

            return promise;
        },

        // **Param**
        // ```id```: string, dash-delimited reg entity id
        //
        // **Returns** an array of strings, dash-delimited reg entity ids of children
        //
        // The magic of the flexibility of the app is that we can pass around these 
        // dash-delimited ids and get the job done pretty seamlessly w/o worrying about
        // what exactly we're dealing with. We just rely on a set of rules.
        getChildren: function(id) {
            var kids = [],
                regStructureLen = this.regStructure.length,
                regex = new RegExp(id + '[-,a-z,0-9]');

            while (regStructureLen--) {
                if (regex.test(this.regStructure[regStructureLen])) {
                    kids.push(this.regStructure[regStructureLen]);
                } 
            }

            return kids;
        },

        // **Param**
        // ```id```: string, dash-delimited reg entity id
        // 
        // **Returns** string, dash-delimited reg entity id of parent to
        // the id passed in or boolean false if the requested id has no parent
        //
        // The converse of ```this.getChildren```
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

        // We don't have need for the following methods.
        // This is my half-baked way of overriding them so that they
        // can be legally called as Backbone runs its course, but have
        // no effect.
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
