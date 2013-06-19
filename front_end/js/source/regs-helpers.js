define('regs-helpers', function() {
    'use strict';
    return {
        isIterable: function(obj) {
            if (typeof obj === 'array' || typeof obj === 'object') {
                return true;
            }
            return false;
        },

        // verbose, but much faster than the concise
        // jquery alternatives
        // http://jsperf.com/create-dom-element/8
        fastLink: function(href, text, classStr) {
            var link = document.createElement('a'),
                $link;

            $link = $(link);
            link.href = href;
            link.innerHTML = text;
            link.className = classStr || '';

            return $link;
        },

        // super dumb impementation. TODO
        // recursive strategy when full spectrum is implemented
        idToRef: function(id) {
            var ref, parts;
            parts = id.split('-');

            if (!isNaN(parseInt(parts[0], 10))) {
                // only handles two at the moment. to be made smarter.

                if (parts[1]) {
                    if (isNaN(parseInt(parts[1], 10))) {
                        ref = 'Appendix ';
                        ref += parts[1];
                        ref += ' to Part ';
                        ref += parts[0];
                    }
                    else {
                        ref = '§ ';
                        ref += parts[0];
                        parts.shift();
                        ref += '.' + parts[0];

                    }
                }
            }
            else {
                ref = 'Supplement ';
                ref += parts[0];
                if (parts[1]) {
                    ref += ' to Part ';
                    ref += parts[1]; 
                }
            }
            
            return ref;
        }
    };
});
