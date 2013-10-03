// **Extends** Backbone.Events
//
// **Usage** require(['dispatch'], function(Dispatch) {}))
//
// **Dispatch:**
// Verb: 
// * 1. Send off to a destination or for a purpose.
// * 2. Deal with a task quickly and efficiently
//
// Noun: The sending of someone or something to a destination or for a purpose.
//
// Dispatch is responsible, via Backbone.Events, for, appropriately, dispatching event triggers and notifying bindings
// There are entities that, at first glance, would seem to have a straightforward parent/child relationship with another module
// However, there are significant interactions that occur across two or more modules. Instead of having a complicated 
// multi-event scheme or introducing a lot of coupling between modules, Dispatch can house and serve information about these entities.
//
// Example: inline definitions. They are triggered by a link in reg-view, can be closed by reg-view, sidebar-head-view or sidebar-view.
// Closing a definition without introducing multiple events or causing cyclical dependencies can be tricky. If the definition View instance belongs
// to any of these modules, another module will need to as the parent module directly for information about the View instance. Instead, all
// modules can remove the open definition by calling `Dispatch.remove('definition');`
define('dispatch', ['jquery', 'underscore', 'backbone'], function($, _, Backbone) {
    'use strict';
    var Dispatch = _.extend({
        // storage for entities
        // **Usage** Dispatch.open.definition
        // idea is that each entity will be stored according to its type so that any module can refer to it without knowing what
        // instance it holds. 
        // This scheme currently limits it to one value associated with each type, in theory.
        open: {},

        state: {},

        // store a new entity in Dispatch.open
        // **Params**
        //
        // * **key**, string, entity type, ex. 'definition'
        // * **val**, object, new Backbone View
        set: function(key, val) {
            this.open[key] = val;
        },

        trigger: function(name) {
            // var events: {
            //     'content:loading': {
            //          'args': { 
            //              'id': 'unique id ex. 123-4',
            //              'type': 'type of content ex "regSection" or "sxs",
            //          },
            //          'usage': 'to do prep work or start transitional states before content loads'

            //      },
            //      'content:loaded': {
            //          'usage': 'to render loaded content or settle state after content is rendered'
            //      },
            //      'mode:change': {
            //          'args': {
            //              'id': 'open content in new mode',
            //              'type': 'new mode changed to. should correspond with this.state["mode"]',
            //              'usage': 'to prompt views to make alterations based on the new state
            //          }
            //      },
            //      'ga-event:?': {
            //          '?': 'event to be sent to Google Analytics'
            //      }
            //
            // };

            var listenTo = {
                'content:loaded': this.setActivityStatus,
                'content:loading:regSection': this.setActivityStatus,
                'content:loading:sxs': this.setActivityStatus,
                'content:loading:sidebar': this.setActivityStatus,
                'mode:change': this.setUIMode
            };

            if (listenTo.hasOwnProperty[name]) {
                listenTo[name](arguments);
            }

            Dispatch.__super__.trigger.apply(this, name); 
        },

        removeContentView: function() {
            if (typeof this.open['contentView'] !== 'undefined') {
                this.open['contentView'].remove();
                delete(this.open['contentView']);
            }
        },

        setContentView: function(view) {
            this.set('contentView', view);
        },

        // remove a value from Dispatch.open and call its `remove()` method
        // **Param** string, entity type, ex. 'definition'
        remove: function(key) {
            if (this.open[key]) {
                this.open[key].remove();
                delete(this.open[key]);
            }
        },

        hasPushState: function() {
            return(this.state['pushState']);
        },

        setState: function(state) {
            this.state['pushState'] = state;
        },

        getUIMode: function() {
            // var options = ['regSection', 'breakaway', 'search', 'diff', 'history'];
            return(this.state['mode']);
        },

        setUIMode: function(context) {
            this.state['mode'] = context.type;
        },

        getActivityStatus: function() {
            // var options = ['standby', 'init', 'loading'];
            return(this.state['activity'] || 'standby');   
        },

        setActivityStatus: function(context) {
            this.state['activity'] = context.type;
        },

        // retrieve the id of the stored object
        // **Param** string, entity type, ex. 'definition'
        getViewId: function(type) {
            if (typeof this.open[type] === 'object') {
                return this.open[type].model.id;
            }
            return false;
        },

        getDrawerState: function() {
            if (typeof this.open['drawerState'] !== 'undefined') {
                return this.open['drawerState'];
            }
            else {
                return false;
            }
        },

        get: function(item) {
            return this.open[item];
        },

        // return open section ex. 1005-3
        getOpenSection: function() {
            return this.open['section']; 
        },

        getVersion: function() {
            return this.open['version'];
        },

        getURLPrefix: function() {
            if (this.open['urlprefix']) {
                return this.open['urlprefix'];
            }
            else {
                return false;
            }
        },

        getRegId: function() {
            return this.open['reg'];
        },

        getContentView: function() {
            return this.open['contentView'];
        }

    }, Backbone.Events);   

    return Dispatch;
});
