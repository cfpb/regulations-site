define(["jquery", "underscore", "backbone", "regs-state", "regs-data", "definition-view", "sub-head-view", "toc-view", "regs-dispatch", "sidebar-view"], function($, _, Backbone, RegsState, RegsData, DefinitionView, SubHeadView, TOCView, Dispatch, SidebarView) {
    "use strict";
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
            // fake template
            var template = function(b, p) {
                $('#' + p).append(b);
            };

            /* 
            * EVENT BINDINGS 
            */

            // interpretations accordion
            $('.expand-button').on('click', function(e) {
                var button = $(this);
                button.toggleClass('open').next('.hidden').slideToggle();
                button.html(button.hasClass('open') ? 'Hide' : 'Show');
            });

            // click term link, open definition
            $('.definition').on('click', function(e) {
                e.preventDefault();
                if ($(this).data('active')) {
                    RegsState.openDef.view.remove();
                    delete(RegsState.openDef.id);
                    $(this).removeClass('active').removeData('active');
                    return;
                }

                var defId = $(this).attr('data-definition'),
                    $link = $(e.target);
                $link.addClass('active').data('active', 1);

                if (!_.isEmpty(RegsState.openDef.link)) {
                    RegsState.openDef.link.removeClass('active').removeData('active');
                }

                RegsState.openDef.link = $link;
                if (defId === RegsState.openDef.id) {
                    return;
                }

                if (!_.isEmpty(RegsState.openDef.view)) {
                    RegsState.openDef.view.remove();
                }
                RegsState.openDef.id = defId;
                RegsState.openDef.view = new DefinitionView({
                    id: defId,
                    $anchor: $link
                });
            });

            // mimics 'read more' accordion type thing
            $('.expand').on('click', function(e) {
                e.preventDefault();
                var pid = $(this).parent().attr('id'),
                    body = RegsData.retrieve(pid); 
                template(body, pid);

                $(this).remove();
            });

            // toc class toggle
            $('#menu-link').on('click', function(e) {
                $('#table-of-contents, #reg-content, #menu-link, #content-header').toggleClass('active');
                return false;
            });

            // persistent reg header on scroll
            $(window).on('scroll', function(e) {
                var docScroll = $(this).scrollTop();
                if (docScroll >= subhead.menuOffset) {
                    Dispatch.trigger('header:expand');
                } else {
                    Dispatch.trigger('header:contract');
                }
            });
        },

        init: function() {
            this.getTree($('#reg-content')); 

            window.subhead = new SubHeadView({el: '#sub-head'});
            window.toc = new TOCView({el: '#menu'});
            window.sidebar = new SidebarView({el: '#sidebar'});
            this.bindEvents();
        }
    }
});
