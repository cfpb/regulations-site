// Module called on app load, once doc.ready
//
// **TODO**: Consolidate/minimize module dependencies
//
// **Usage**: require(['app-init'], function(app) { $(document).ready(function() { app.init(); }) })
define(['jquery', 'underscore', 'backbone', 'main-view', 'reg-model', 'definition-view', 'sub-head-view', 'drawer-view', 'dispatch', 'sidebar-view', 'konami', 'header-view', 'analytics-handler', 'regs-helpers', './regs-router', './reg-view', 'search-results-view'], function($, _, Backbone, MainView, RegModel, DefinitionView, SubHeadView, DrawerView, Dispatch, SidebarView, Konami, HeaderView, AnalyticsHandler, RegsHelpers, Router, RegView, SearchResultsView) {
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

            /*
            * landing page expandable until we discuss the langing page view 
            * TODO: unify all expandables
            */
            $('.disclaimer-header').on('click', function(e){
                e.preventDefault();
                
                var header = $(e.currentTarget),
                section = header.parent(),
                button = header.find('.expand-button'),
                buttonText = header.find('.expand-text');

                section.toggleClass('open');
                header.next('.hidden').slideToggle();
                button.toggleClass('open');
                buttonText.html(section.hasClass('open') ? 'Hide' : 'Show');
            });

            /* ssshhhhh */
            new Konami(function() {
                /* http://thenounproject.com/noun/hamburger/#icon-No17373 */
                /* http://thenounproject.com/noun/carrot/#icon-No7790 */
                document.getElementById('menu-link').className += ' hamburgerify';
                $('.inline-interpretation .expand-button').addClass('carrotify');
                $('#about-tool').html('Made with <span style="color: red"><3</span> by:');
                $('#about-reg').html('Find our brilliant attorneys at:');
            });
        },

        init: function() {
            var openSection,
                urlPrefix,
                regId = $('#menu').data('reg-id'),
                regSection = $('section[data-base-version]'),
                regVersion = regSection.data('base-version');

            Dispatch.set('reg', regId);

            if (window.location.pathname.indexOf('search') > 0) {
                var urlobj = RegsHelpers.parseURL(window.location.href),
                    params = urlobj.params;

                Dispatch.setContentView(
                    new SearchResultsView({
                        query: params.q,
                        version: params.version
                    })
                );
            }
            else if (typeof regSection !== 'undefined') {
                openSection = regSection.attr('id');
                Dispatch.set('section', openSection);

                // cache open section content
                RegModel.set(openSection, regSection.html());

                Dispatch.setContentView(new RegView({id: openSection}));
            }


            if (typeof regVersion !== 'undefined') {
                Dispatch.set('version', regVersion);
            }

            // cache URL prefix
            urlPrefix = RegsHelpers.findURLPrefix();
            if (urlPrefix) {
                Dispatch.set('urlprefix', urlPrefix);
            }

            // init primary Views that require only a single instance
            window.Regs = {};
            window.Regs.subhead = new SubHeadView();
            window.Regs.drawer = new DrawerView();
            window.Regs.sidebar = new SidebarView();
            window.Regs.mainView = new MainView();
            window.Regs.analytics = new AnalyticsHandler();
            window.Regs.mainHeader = new HeaderView();

            Router.start();

            this.bindEvents();
        }
    };
});
