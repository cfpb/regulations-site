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

        nonNumericId: function(p0, p1) {
            if (isNaN(parseInt(p0, 10))) {
                return 'Supplement ' + p0 + ' to Part ' + p1;
            }
            else if (isNaN(parseInt(p1, 10))) {
                return 'Appendix ' + p1 + ' to Part ' + p0;
            }
        },

        idToRef: function(id) {
            var ref = '', 
                parts, i, len, dividers, item;
            parts = id.split('-');
            len = parts.length - 1;
            dividers = ['§ .', '', '( )', '( )', '( )', '( )'];

            if (isNaN(parseInt(parts[0], 10)) || 
                isNaN(parseInt(parts[1], 10))) {
                return this.nonNumericId(parts[0], parts[1]);
            }

            for (i = 0; i <= len; i++) {
                if (i === 1) {
                    ref += parts[i];
                }
                else {
                    item = dividers[i].split(' '); 
                    ref += item[0] + parts[i] + item[1];
                }
            }

            return ref;
        },

        findBaseSection: function(id) {
            var parts = id.split('-');

            return parts[0] + '-' + parts[1];
        }
    };
});
