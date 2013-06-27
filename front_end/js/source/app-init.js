define(['jquery', 'underscore', 'backbone', 'content-view', 'regs-data', 'definition-view', 'sub-head-view', 'toc-view', 'regs-dispatch', 'sidebar-view', 'konami'], function($, _, Backbone, ContentView, RegsData, DefinitionView, SubHeadView, TOCView, Dispatch, SidebarView, Konami) {
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
                setTimeout(function() { insertImg(tag); }, 1000, tag);
            });
        },

        init: function() {
            this.getTree($('#reg-content')); 

            window.subhead = new SubHeadView({el: '#content-subhead'});
            window.toc = new TOCView({el: '#menu'});
            window.sidebar = new SidebarView({el: '#sidebar'});
            window.regContent = new ContentView({el: '.main-content'});
            this.bindEvents();
            this.fetchModelForms();
        }
    };
});
