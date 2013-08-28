// **Extends** MetaModel
//
// **Usage** ```require(['reg-model'], function(RegModel) {})```
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
define('reg-model', ['jquery', 'underscore', 'backbone', './regs-helpers', './dispatch', './meta-model'], function($, _, Backbone, RegsHelpers, Dispatch, MetaModel) {
    'use strict';

    // represents a whole regulation
    Backbone.RegModel = MetaModel.extend({
        // an index of all of the entities in the reg, whether or not they've been loaded
        regStructure: [],

        // content = markup to string representations of each reg paragraph/entity
        // loaded into the browser (rendered or not)
        content: {},

        // recurses over the parsed reg tree and creates an in-browser representation
        // of a reg. may or may not be functional based on current tree.
        // only in use for tests right now...
        // refactor to parse just out of the DOM
        parse: function(jsonObj) {
            if (typeof jsonObj === 'object') {
                for (var key in jsonObj) {
                    if (jsonObj.hasOwnProperty(key)) {
                        if (key === 'label') {
                            this.set(jsonObj[key]['text'], jsonObj['text']);
                        }

                        if (RegsHelpers.isIterable(jsonObj[key])) {
                            this.parse(jsonObj[key]);
                        }
                    }
                } 
            }

            return this;
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
        }
    });

    var reg = new Backbone.RegModel();

    return reg;
});
