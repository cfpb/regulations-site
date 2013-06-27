define(['jquery', 'underscore', 'backbone', 'content-view', 'regs-data', 'definition-view', 'sub-head-view', 'toc-view', 'regs-dispatch', 'sidebar-view', 'konami', 'analytics-handler'], function($, _, Backbone, ContentView, RegsData, DefinitionView, SubHeadView, TOCView, Dispatch, SidebarView, Konami, AnalyticsHandler) {
    'use strict';
    return {
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

        bindEvents: function() {
            // toc class toggle
            $('#menu-link, #toc-close').on('click', function() {
                $('#menu, #reg-content, #menu-link, #content-header').toggleClass('active');
                return false;
            });

            new Konami(function() {
                // http://thenounproject.com/noun/hamburger/#icon-No17373
                // http://thenounproject.com/noun/carrot/#icon-No7790
                document.getElementById('menu-link').className += ' hamburgerify';
                $('.inline-interpretation .expand-button').addClass('carrotify');
                $('#about-tool').html('Made with <span style="color: red"><3</span> by:');
                $('#about-reg').html('Find our brilliant attorneys at:');
            });
        },

        init: function() {
            this.getTree($('#reg-content')); 

            window.Regs = {};
            window.Regs.subhead = new SubHeadView({el: '#content-subhead'});
            window.Regs.toc = new TOCView({el: '#menu'});
            window.Regs.sidebar = new SidebarView({el: '#sidebar'});
            window.Regs.regContent = new ContentView({el: '.main-content'});
            window.Regs.analytics = new AnalyticsHandler();
            this.bindEvents();
        }
    };
});
