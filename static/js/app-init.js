// TODO: function -> module
define(["jquery", "underscore", "backbone", "regs-data", "definition-view"], function($, _, Backbone, RegsData,  DefinitionView) {
    return function() {
        var getTree = function($obj) {
            $obj.children().each(function() {
                var $child = $(this),
                    cid = $child.attr('id');

                RegsData.store({
                    'text': cid,
                    'content': $child.html()
                }); 

                if (typeof cid !== 'undefined') {
                    getTree($child);
                }
            });
        };

        getTree($('#reg-content')); 

        // fake template
        var template = function(b, p) {
            $('#' + p).append(b);
        };

        /* 
        * EVENT BINDINGS 
        */
        // click term link, open definition
        $('.definitionBREAK').on('click', function(e) {
            e.preventDefault();
            var defId = $(this).attr('data-definition');

            // briefly considered giving the term link its own view
            // decided that it was unecessary for now. if this event
            // binding section gets out of hand, we should reconsider [ts]

            // TODO: supports only one open definition
            if (!RegsViews.openDefinitions[defId]) {
                RegsViews.openDefinitions[defId] = new DefinitionView({
                    termId: defId,
                    termLink: e.target
                });
            }
            else {
                RegsViews.openDefinitions[defId].remove();
                delete(RegsViews.openDefinitions[defId]);
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
    }
});
