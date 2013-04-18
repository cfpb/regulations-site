require(function() {
  return {
    isIterable: function(obj) {
      if (typeof obj === 'array' || typeof obj === 'object') {
        return true;
      }
      return false;
    }
  }
});
