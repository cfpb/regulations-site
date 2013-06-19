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

        idToRef: function(id) {
            var ref, parts;

            parts = id.split('-');
            ref = parts[0];
            parts.shift();
            ref += "." + parts[0];

            return ref;
        }
    };
});
