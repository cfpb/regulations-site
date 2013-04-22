require(["jquery", "underscore", "backbone", "regs-data", "sample-json", "definition-view"], function($, _, Backbone, RegsData, JSONObj, DefinitionView) {
  $(document).ready(function() {
    // template stub
    var template = function(b, p) {
      $('#' + p).append(b);
    };

    if (typeof JSONObj !== 'undefined') {
      RegsData.parse(JSONObj); 

      $('.definition').on('click', function(e) {
        e.preventDefault();
        var defId = $(this).attr('data-definition'),
            def = new DefinitionView({
              model: defId
            });
      });
        
      // event bindings
      $('.expand').on('click', function(e) {
        e.preventDefault();
        var pid = $(this).parent().attr('id'),
            body = RegsData.retrieve(pid); 
        template(body, pid);

        $(this).remove();
      });
    }
  });
});
