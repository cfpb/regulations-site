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
        fastLink: function(href, text, classStr, dataConfig) {
            var link = document.createElement('a'),
                $link;

            $link = $(link);
            link.href = href;
            link.innerHTML = text;
            link.className = classStr || '';

            // takes an array to add a data attr
            if (typeof dataConfig !== 'undefined') {
                link[dataConfig[0]] = dataConfig[1];
            }

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
        // **TODO** RegModel.getParent is the same?
        findBaseSection: function(id) {
            var parts, base;

            if (id.indexOf('-') !== -1) {
                parts = id.split('-');
                base = parts[0];

                if (id.indexOf('Interp') !== -1) {
                    base += '-Interp';
                }
                else {
                    base += '-' + parts[1];
                }

                return base;
            }
            else {
                return id;
            }
        },

        isSupplement: function(id) {
            var parts;

            if (typeof id !== 'undefined') {
                parts = _.compact(id.split('-'));
                if (parts.length < 2) {
                    return false;
                }

                if (parts[1].toLowerCase() === 'interp') {
                    return true;
                }
            }

            return false;
        },

        isAppendix: function(id) {
            var parts;

            if (typeof id !== 'undefined') {
                parts = _.compact(id.split('-'));
                if (parts.length < 2) {
                    return false;
                }

                if (isNaN(parts[1]) && parts[1].toLowerCase() !== 'interp') {
                    return true;
                }
            }

            return false;
        },

        // thanks, James Padolsey http://james.padolsey.com/javascript/parsing-urls-with-the-dom/
        parseURL: function(url) {
            var a =  document.createElement('a');
            a.href = url;
            return {
                source: url,
                protocol: a.protocol.replace(':',''),
                host: a.hostname,
                port: a.port,
                query: a.search,
                params: (function(){
                    var ret = {},
                        seg = a.search.replace(/^\?/,'').split('&'),
                        len = seg.length, i = 0, s;
                    for (;i<len;i++) {
                        if (!seg[i]) { continue; }
                        s = seg[i].split('=');
                        ret[s[0]] = s[1];
                    }
                    return ret;
                })(),
                hash: a.hash.replace('#',''),
                path: a.pathname.replace(/^([^\/])/,'/$1'),
                segments: a.pathname.replace(/^\//,'').split('/')
            };
        }
    };
});
