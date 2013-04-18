require(["jquery", "regs-data", "sample-json"], function($, RegsData, JSONObj) {
  $(document).ready(function() {
    if (typeof JSONObj !== 'undefined') {
      RegsData.parse(JSONObj); 
    }
  });
});
