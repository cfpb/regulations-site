// **Usage**
// require(['regs-helpers'], function(RegsHelpers) {});
//
// Defines some globally useful helper functions
define('regs-helpers', function() {
    'use strict';
    return {
        isIterable: function(obj) {
            if (typeof obj === 'array' || typeof obj === 'object') {
                return true;
            }
            return false;
        },

        // **Params**
        // ```href```: String, url
        // ```text```: String, link text 
        // ```classStr```: String, optional, class name
        //
        // **Returns**
        // jQobj: new link
        //
        // verbose, but much faster than the concise jquery alternatives
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

        // **Params**
        // ```interpParts```: Array of Strings or Numbers, entity that is 
        // interpreted
        //
        // **Returns** human-readable representation of the reg section
        interpId: function(interpParts) {
            if (interpParts.length === 1) {
                return 'Supplement I to Part ' + interpParts[0];
            } else if (isNaN(interpParts[1])) {
                return 'Supplement I to Appendix ' + interpParts[1];
            } else {
                return 'Supplement I to §' + interpParts[0] + '.' + interpParts[1];
            }
        },

        // **Params**
        // ```p0```: String or Number, section ID
        // ```p1```: String or Number, reg ID
        //
        // **Returns** human-readable representation of the reg section
        appendixId: function(part, letter) {
            return 'Appendix ' + letter  + ' to Part ' + part;
        },

        // **Param** dash-delimited string representation of reg entity ID
        //
        // **Returns** Reg entity marker formatted for human readability
        idToRef: function(id) {
            var ref = '', 
                parts, i, len, dividers, item, interpIndex;
            parts = id.split('-');
            len = parts.length - 1;
            dividers = ['§ .', '', '( )', '( )', '( )', '( )'];

            /* if we've got only the reg part number */
            if (len === 0) {
                ref = parts[0];
                return ref;
            }

            /* if we have a supplement */
            interpIndex = $.inArray('Interp', parts);
            if (interpIndex >= 0) {
                return this.interpId(parts.slice(0, interpIndex));
            }
            /* if we have an appendix */
            if (isNaN(parseInt(parts[1], 10))) {
                return this.appendixId(parts[0], parts[1]);
            }

            /* we have a paragraph */
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

        // Finds parent-most reg paragraph
        //
        // **TODO** RegsData.getParent is the same?
        findBaseSection: function(id) {
            if (id.indexOf('-') !== -1) {
                var parts = id.split('-');

                return parts[0] + '-' + parts[1];
            }
            else {
                return id;
            }
        },

        findURLPrefix: function() {
            var i, pathLen, sitePath,
                url = [];

            sitePath = document.location.pathname.split('/');
            pathLen = sitePath.length;

            for (i=0; i<=pathLen; i++) {
                if (sitePath[i] === 'regulation') {
                    break;
                }
                else if (sitePath[i] !== '') {
                    url.push(sitePath[i]);
                }
            }

            if (url.length === 0) {
                return false;
            }
            else {
                return url = _.compact(url).join('/');
            }
        }
    };
});
