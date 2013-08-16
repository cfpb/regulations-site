// Module called on app load, once doc.ready
//
// **TODO**: Consolidate/minimize module dependencies
//
// **Usage**: require(['app-init'], function(app) { $(document).ready(function() { app.init(); }) })
define(['jquery', 'underscore', 'backbone', 'content-view', 'regs-data', 'definition-view', 'sub-head-view', 'toc-view', 'regs-dispatch', 'sidebar-view', 'konami', 'header-view', 'analytics-handler'], function($, _, Backbone, ContentView, RegsData, DefinitionView, SubHeadView, TOCView, Dispatch, SidebarView, Konami, HeaderView, AnalyticsHandler) {
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

                RegsData.set({
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

        // as of sprint 6, model form images are giant and block at load
        // incrementally loads in images once rendering is complete
        fetchModelForms: function() {
            var insertImg = function(tag) {
                var $tag = $(tag),
                    url = $tag.data('imgUrl'),
                    alt = $tag.data('imgAlt');

                if (url) {
                    $tag.parent().append('<img class="reg-image" src="' + url + '" alt="' + alt + '" />');
                }
            };

            $('noscript').each(function() {
                var tag = this;
                setTimeout(function() { insertImg(tag); }, 2000, tag);
            });
        },

        init: function() {
            var openSection,
                regVersion,
                regSection = $('.main-content .reg-section');

            // init primary Views that require only a single instance
            window.Regs = {};
            window.Regs.subhead = new SubHeadView();
            window.Regs.toc = new TOCView();
            window.Regs.sidebar = new SidebarView();
            window.Regs.regContent = new ContentView();
            window.Regs.analytics = new AnalyticsHandler();
            window.Regs.mainHeader = new HeaderView();

            openSection = regSection.attr('id');
            Dispatch.set('section', openSection);
            Dispatch.trigger('openSection:set', openSection);

            regVersion = regSection.data('base-version');
            Dispatch.set('version', regVersion);

            this.bindEvents();
            this.fetchModelForms();
        }
    };
});
