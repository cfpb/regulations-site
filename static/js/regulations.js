require(["jquery", "regs-data", "sample-json"], function($, RegsData, JSONObj) {
  $(document).ready(function() {
    // template stub
    var template = function(b, p) {
      $('#' + p).append(b);
    };

    if (typeof JSONObj !== 'undefined') {
      RegsData.parse(JSONObj); 
        
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
