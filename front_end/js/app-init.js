define(["jquery", "underscore", "backbone", "regs-state", "regs-data", "definition-view", "interpretation-view"], function($, _, Backbone, RegsState, RegsData, DefinitionView, InterpretationView) {
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

            $('.interpretation-ref').on('click', function(e) {
                e.preventDefault();
                var $this = $(this),
                    parent = $this.closest('li').attr('id'),
                    interpretationId = "I-" + parent;

                if ($this.data("state") === 'open') {
                    RegsState.openInterps[interpretationId].remove();
                    $this.removeData("state");
                }
                else {
                    RegsState.openInterps[interpretationId] = new InterpretationView({
                        id: interpretationId,
                        $anchor: $this
                    });

                    $this.data("state", "open");
                }
            });

            // toc class toggle

            $('#menu-link').click(function(){
                $('#table-of-contents').toggleClass('active');
                // prevent default link behavior
                return false;
            });
        },

        init: function() {
            this.getTree($('#reg-content')); 
            this.bindEvents();
            console.log(RegsData);
        }
    }
});
