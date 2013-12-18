define('child-view', ['jquery', 'underscore', 'backbone', 'jquery-scrollstop', './regs-router', 'header-controller', 'drawer-controller', './regs-helpers', 'main-controller', 'ga-events'], function($, _, Backbone, jQScroll, Router, HeaderEvents, DrawerEvents, Helpers, MainEvents, GAEvents) {
    'use strict';
    var ChildView = Backbone.View.extend({
        initialize: function() {
            var returned, render;

            this.model = this.options.model;
            this.controller = MainEvents;
            this.controller.on('section:rendered', this.setElement, this);
            // callback to be sent to model's get method
            // called after ajax resolves sucessfully
            render = function(returned) {
                if (typeof this.options.cb !== 'undefined') {
                    this.options.cb(returned, this.options);
                }

                this.render();
            }.bind(this);

            // if the site wasn't loaded on this content
            if (typeof this.options.rendered === 'undefined') {
                // simplifies to
                // this.model.get()
                returned = this.model.get(this.options.id, render);

                if (typeof this.title === 'undefined') {
                    this.title = this._assembleTitle();
                }

                this.route(this.options);

                GAEvents.trigger('section:open', this.options);
            }

            this.$sections = {};
            this.activeSection = this.id;
            this.$activeSection = '';

            HeaderEvents.trigger('clear');

            if (this.id) {
                this.attachWayfinding();

                DrawerEvents.trigger('section:open', this.id);
            }

            return this;
        },

        setElement: function() {
            if (this.id) {
                Backbone.View.prototype.setElement.call(this, '#' + this.id);
            }
        },

        attachWayfinding: function() {
            this.updateWayfinding();
            // * when a scroll event completes, check what the active secion is
            // we can't scope the scroll to this.$el because there's no localized
            // way to grab the scroll event, even with overflow:scroll
            $(window).on('scrollstop', (_.bind(this.checkActiveSection, this)));

        },

        render: function() {
            this.updateWayfinding();
            HeaderEvents.trigger('section:open', this.id);
            DrawerEvents.trigger('section:open', this.id);
        },

        changeFocus: function(id) {
            $(id).focus();
        },

        _assembleTitle: function() {
            var titleParts, newTitle;
            titleParts = _.compact(document.title.split(" "));
            newTitle = [titleParts[0], titleParts[1], Helpers.idToRef(this.id), '|', 'eRegulations'];
            return newTitle.join(' ');
        },


        // naive way to update the active table of contents link and wayfinding header
        // once a scroll event ends, we loop through each content section DOM node
        // the first one whose offset is greater than the window scroll position, accounting
        // for the fixed position header, is deemed the active section
        checkActiveSection: function() {
            var len = this.$contentContainer.length - 1;

            for (var i = 0; i <= len; i++) {
                if (this.$sections[i].offset().top + this.$contentHeader.height() >= $(window).scrollTop()) {
                    if (_.isEmpty(this.activeSection) || (this.activeSection !== this.$sections[i].id)) {
                        this.activeSection = this.$sections[i][0].id;
                        this.$activeSection = this.$sections[i][0];
                        // **Event** trigger active section change
                        HeaderEvents.trigger('section:open', this.activeSection);

                        if (typeof window.history !== 'undefined' && typeof window.history.replaceState !== 'undefined') {
                            // update hash in url
                            window.history.replaceState(
                                null,
                                null,
                                window.location.origin + window.location.pathname + window.location.search + '#' + this.activeSection
                            );
                        }

                        return;
                    }
                }
            }
            
                 
            return this;
        },

        updateWayfinding: function() {
            var i, len;

            // cache all sections in the DOM eligible to be the active section
            // also cache some jQobjs that we will refer to frequently
            this.$contentHeader = this.$contentHeader || $('header.reg-header');

            // sections that are eligible for being the active section
            this.$contentContainer = $('#' + this.id).find('.level-1 li[id], .reg-section, .appendix-section, .supplement-section');

            // cache jQobjs of each reg section
            len = this.$contentContainer.length;

            // short term solution: sometimes, back buttoning on diffs, this.$sections undefined. why?
            this.$sections = this.$sections || {};

            for (i = 0; i < len; i++) {
                this.$sections[i] = $(this.$contentContainer[i]);
            }
        },

        route: function(options) {
            if (Router.hasPushState && typeof options.noRoute === 'undefined') {
                var url = this.url,
                    hashPosition, titleParts, newTitle;

                // if a hash has been passed in
                if (options && typeof options.scrollToId !== 'undefined') {
                    url += '#' + options.scrollToId;
                }
                else {
                    hashPosition = (typeof Backbone.history.fragment === 'undefined') ? -1 : Backbone.history.fragment.indexOf('#');
                    //  Be sure not to lose any hash info
                    if (hashPosition !== -1) {
                        url += Backbone.history.fragment.substr(hashPosition);
                    }
                }
                Router.navigate(url);
                document.title = this.title;
            }
        },

        remove: function() {
            $(window).off('scrollstop');
            this.stopListening();
            return this;
        }
    });

    return ChildView;
});
