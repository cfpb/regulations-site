define('drawer-view', ['jquery', 'underscore', 'backbone', 'regs-dispatch', 'toc-view'], function($, _, Backbone, Dispatch, TOCView) {
    'use strict';

    var DrawerView = Backbone.View.extend({
        el: '#menu',

        initialize: function() {
            Dispatch.on('drawer:stateChange', this.changeContents, this);

            this.$label = $('.toc-type');
            this.$children = $('.toc-container');
            this.childViews = {
                '#table-of-contents': {
                    'selector': $('#table-of-contents'),
                    'title':('Table of contents for')
                },
                '#history': {
                    'selector': $('#history'),
                    'title':('Switch between versions of')
                },
                '#search': {
                    'selector': $('#search'),
                    'title':('Search')
                }
            };

            this.childViews['#table-of-contents'].view = new TOCView({el: '#toc'}); 

        },

        changeContents: function(activeId) {
            this.$children.addClass('hidden');
            this.childViews[activeId]['selector'].removeClass('hidden');

            this.$label.html(this.childViews[activeId]['title']);
            Dispatch.set('drawerState', activeId);

            
        }

    });

    return DrawerView;
});
