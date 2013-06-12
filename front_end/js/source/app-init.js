define(['jquery', 'underscore', 'backbone', 'content-view', 'regs-data', 'definition-view', 'sub-head-view', 'toc-view', 'regs-dispatch', 'sidebar-view'], function($, _, Backbone, ContentView, RegsData, DefinitionView, SubHeadView, TOCView, Dispatch, SidebarView) {
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
            $('#menu-link').on('click', function() {
                $('#table-of-contents, #reg-content, #menu-link, #content-header').toggleClass('active');
                return false;
            });
        },

        init: function() {
            this.getTree($('#reg-content')); 

            window.subhead = new SubHeadView({el: '#sub-head'});
            window.toc = new TOCView({el: '#menu'});
            window.sidebar = new SidebarView({el: '#sidebar'});
            window.regContent = new ContentView({el: '.main-content'});
            this.bindEvents();
        }
    };
});
