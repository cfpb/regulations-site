define('meta-model', ['underscore', 'backbone', 'dispatch'], function(_, Backbone, Dispatch) {
    'use strict';
    var MetaModel = Backbone.Model.extend({

        constructor: function(properties) {
            var k;

            if (typeof properties !== 'undefined') {
                for (k in properties) {
                    if (properties.hasOwnProperty(k)) {
                        this[k] = properties[k];
                    }
                }
            }

            // in the case of reg-model
            // an index of all of the entities in the reg, whether or not they've been loaded
            this.content = this.content || {};

            // in the case of reg-model
            // content = markup to string representations of each reg paragraph/entity
            // loaded into the browser (rendered or not)
            this.structure = this.structure || [];

            Backbone.Model.apply(this, arguments);
        },

        set: function(sectionId, sectionValue) {
            var cached = this.has(sectionId),
                section;

            if (typeof sectionId !== 'undefined' && !(_.isEmpty(sectionId))) {
                if (!(cached)) {
                    this.content[sectionId] = sectionValue;
                    section = sectionValue;

                    if (_.indexOf(this.structure, sectionId) === -1) {
                        this.structure.push(sectionId);
                    }
                }
                else {
                    section = cached;
                }
            }

            return section; 
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
        fetch: function(id) {
            return this.get(id);
        },

        request: function(id) {
            var url = this.getAJAXUrl(id),
                $promise;

            $promise = $.ajax({
                url: url,
                success: function(data) { this.set(id, data); }.bind(this)
            });

            return $promise;
        },

        getAJAXUrl: function(id) {
            var url,
                urlPrefix = Dispatch.getURLPrefix();

            if (urlPrefix) {
                url = '/' + urlPrefix + '/partial/';
            }
            else {
                url = '/partial/';
            }

            if (typeof this.supplementalPath !== 'undefined') {
                url += this.supplementalPath + '/';
            }

            url += id;

            if (id.indexOf('/') === -1) {
                url += '/' + Dispatch.getVersion(); 
            }

            return url;
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

    return MetaModel;
});
