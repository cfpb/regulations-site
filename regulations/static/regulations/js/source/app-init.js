// Module called on app load, once doc.ready
//
// **TODO**: Consolidate/minimize module dependencies
define(['jquery', 'underscore', 'backbone', 'main-view', 'reg-model', 'definition-view', 'sub-head-view', 'drawer-view', 'sidebar-view', 'konami', 'header-view', 'analytics-handler', 'regs-helpers', './regs-router', './reg-view', 'search-results-view'], function($, _, Backbone, Main, RegModel, DefinitionView, SubHeadView, DrawerView, SidebarView, Konami, HeaderView, AnalyticsHandler, Helpers, Router, RegView, SearchResultsView) {
    'use strict';
    return {
        // Temporary method. Recurses DOM and builds front end representation of content.
        // API should make this obsolete.
        getTree: function($obj) {
            var parent = this;
            $obj.children().each(function() {
                var $child = $(this),
                    cid = $child.attr('id'),
                    clist = $child.find('ol'),
                    $nextChild;

                RegModel.set({
                    'text': cid,
                    'content': $child.html()
                }); 

                if (typeof (cid, clist) !== 'undefined') {
                    $nextChild = clist ? $(clist) : $child;
                    parent.getTree($nextChild);
                }
            });
        },

        // Purgatory for DOM event bindings that should happen in a View
        bindEvents: function() {

            // disable/hide an alert
            $('.disable-link').on( 'click', function(e) {
                e.preventDefault();
                $(this).closest('.displayed').addClass('disabled');
            });

            /* ssshhhhh */
            new Konami(function() {
                /* http://thenounproject.com/noun/hamburger/#icon-No17373 */
                /* http://thenounproject.com/noun/carrot/#icon-No7790 */
                document.getElementById('menu-link').className += ' hamburgerify';
                $('.inline-interpretation .expand-button').addClass('carrotify');
            });
        },

        init: function() {
            Router.start();
            this.bindEvents();
        }
    };
});
