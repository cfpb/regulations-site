define(["jquery", "underscore", "backbone", "regs-state", "regs-data", "definition-view", "sub-head-view", "toc-view"], function($, _, Backbone, RegsState, RegsData, DefinitionView, SubHeadView, TOCView) {
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
                var defId = $(this).attr('data-definition');

                // briefly considered giving the term link its own view
                // decided that it was unecessary for now. if this event
                // binding section gets out of hand, we should reconsider [ts]

                // TODO: supports only one open definition
                if (!RegsState.openDefs[defId]) {
                    RegsState.openDefs[defId] = new DefinitionView({
                        id: defId,
                        $anchor: $(e.target)
                    });
                }
                else {
                    RegsState.openDefs[defId].remove();
                    delete(RegsState.openDefs[defId]);
                }
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
                    Events.trigger('expand');
                } else {
                    Events.trigger('contract');
                }
            });
        },

        init: function() {
            this.getTree($('#reg-content')); 
            window.Events = _.extend({}, Backbone.Events);
            window.subhead = new SubHeadView({el: '#sub-head'});
            window.toc = new TOCView({el: '#menu'});
            this.bindEvents();
        }
    }
});
