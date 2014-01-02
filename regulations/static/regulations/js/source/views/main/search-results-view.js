define('search-results-view', ['jquery', 'underscore', 'backbone', './search-model', './regs-router', 'header-events', 'main-events', 'drawer-events', 'child-view'], function($, _, Backbone, SearchModel, Router, HeaderEvents, MainEvents, DrawerEvents, ChildView) {
    'use strict';

    var SearchResultsView = ChildView.extend({
        events: {
            'click .search-nav a': 'paginate',
            'click h3 .internal': 'openResult'
        },

        initialize: function() {
            this.query = this.options.query;
            this.regVersion = this.options.regVersion;
            this.page = parseInt(this.options.page, 10) || 0;
            this.title = 'Search of ' + this.options.regPart + ' for ' + this.query + ' | eRegulations';

            // if the browser doesn't support pushState, don't 
            // trigger click events for links
            if (Router.hasPushState === false) {
                this.events = {};
            }

            DrawerEvents.trigger('pane:change', 'search');

            // if the site wasn't loaded on the search results page
            if (this.options.render) {
                this.options.id = this.assembleSearchURL(this.options);
                this.url = 'search/' + this.options.id;

                ChildView.prototype.initialize.apply(this, arguments);
            }

        },

        setElement: function() {
            Backbone.View.prototype.setElement.call(this, '#content-wrapper.search-results');            
        },

        assembleSearchURL: function(options) {
            var url = options.regPart;
            url += '?q=' + options.query;
            url += '&version=' + options.regVersion;

            if (typeof options.page !== 'undefined') {
                url += '&page=' + options.page;
            }

            return url;
        },

        render: function() {
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
                    regVersion: this.regVersion,
                    page: page
                };

            MainEvents.trigger('search-results:open', null, config, 'search-results');
        },

        openResult: function(e) {
            e.preventDefault();
            var $resultLink = $(e.target),
                config = {};

            config.regVersion = $resultLink.data('linked-version');
            config.scrollToId = $resultLink.data('linked-subsection');
            MainEvents.trigger('section:open', $resultLink.data('linked-section'), config, 'reg-section');
        }
    });

    return SearchResultsView;

});
