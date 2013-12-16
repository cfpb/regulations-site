define('search-results-view', ['jquery', 'underscore', 'backbone', './search-model', './regs-router', 'header-controller', 'main-controller', 'drawer-controller', 'child-view'], function($, _, Backbone, SearchModel, Router, HeaderEvents, MainEvents, DrawerEvents, ChildView) {
    'use strict';

    var SearchResultsView = ChildView.extend({
        el: '#content-wrapper.search-results',

        events: {
            'click .search-nav a': 'paginate',
            'click h3 .internal': 'openResult'
        },

        initialize: function() {
            this.query = this.options.query;
            this.version = this.options.version;
            this.page = parseInt(this.options.page, 10) || 0;
            this.title = 'Search of ' + this.options.regPart + ' for ' + this.query + ' | eRegulations';

            // if the browser doesn't support pushState, don't 
            // trigger click events for links
            if (Router.hasPushState === false) {
                this.events = {};
            }

            DrawerEvents.trigger('pane:change', 'search');

            // if the site was loaded on the search results page
            if (typeof this.options.rendered === 'undefined') {
                this.options.id = this._assembleSearchURL(this.options);
                ChildView.prototype.initialize.apply(this, arguments);
            }
        },

        _assembleSearchURL: function(options) {
            var url = options.regPart;
            url += '?q=' + options.query;
            url += '&version=' + options.version;

            if (typeof options.page !== 'undefined') {
                url += '&page=' + options.page;
            }

            return url;
        },

        render: function(html, options) {

            var $results = this.$el.find('#result-count');

            // if the results were ajaxed in, update header
            if ($results.text().length > 0) {
                HeaderEvents.trigger('search-results:open', $results.text());
                $results.remove();
            }

            if (Router.hasPushState) {
                if (typeof this.options.id !== 'undefined') {
                    Router.navigate('search/' + this.options.id);
                }
            }
        },

        paginate: function(e) {
            e.preventDefault();

            var page = $(e.target).hasClass('previous') ? this.page - 1 : this.page + 1,
                config = {
                    query: this.query,
                    version: this.version,
                    page: page
                };

            MainEvents.trigger('search-results:open', config);
        },

        openResult: function(e) {
            e.preventDefault();
            var $resultLink = $(e.target),
                config = {};

            config.version = $resultLink.data('linked-version');
            config.scrollToId = $resultLink.data('linked-subsection');
            MainEvents.trigger('section:open', $resultLink.data('linked-section'), config, 'reg-section');
        },

        remove: function() {
            this.$el.remove();
            this.stopListening();
            return this;
        }
    });

    return SearchResultsView;

});
