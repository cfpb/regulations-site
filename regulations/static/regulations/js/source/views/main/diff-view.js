define('diff-view', ['jquery', 'underscore', 'backbone', 'main-controller', './regs-router', 'drawer-controller', 'child-view', 'header-controller', './regs-helpers'], function($, _, Backbone, MainEvents, Router, DrawerEvents, ChildView, HeaderEvents, Helpers) {
    'use strict';
    var DiffView = ChildView.extend({
        initialize: function() {
            this.id = this.options.id;
            this.baseVersion = this.options.baseVersion;
            this.newerVersion = this.options.newerVersion;

            // the model builds url off of id (?)
            this.options.id = this._assembleDiffURL(this.options);
            this.url = 'diff/' + this.options.id;
            ChildView.prototype.initialize.apply(this, arguments);

            if (typeof this.options.rendered !== 'undefined') {
                // site loaded on a diff page
                DrawerEvents.trigger('pane:change', 'timeline');
            }
        },

        // "12 CFR Comparison of §1005.1 | eRegulations"
        _assembleTitle: function() {
            var titleParts, newTitle;
            titleParts = _.compact(document.title.split(" "));
            newTitle = [titleParts[0], titleParts[1], Helpers.idToRef(this.id), '|', 'eRegulations'];
            return newTitle.join(' ');
        },

        // ex: diff/1005-1/2011-12121/2012-11111/?from_version=2012-11111
        _assembleDiffURL: function(options) {
            var url = options.id + '/' + options.baseVersion;
            url += '/' + options.newerVersion;
            url += '?from_version=' + options.newerVersion;

            return url;
        }

    });

    return DiffView;
});
