define('drawer-view', ['jquery', 'underscore', 'backbone', 'jquery-cookie', 'regs-dispatch', 'toc-view', 'history-view', 'search-view'], function($, _, Backbone, jQCookie, Dispatch, TOCView, HistoryView, SearchView) {
    'use strict';

    var DrawerView = Backbone.View.extend({
        el: '#menu',

        initialize: function() {
            Dispatch.on('drawer:stateChange', this.changeContents, this);

            this.$label = $('.toc-type');
            this.$children = $('.toc-container');
            this.childViews = {
                'table-of-contents': {
                    'selector': $('#table-of-contents'),
                    'title':('Table of contents for'),
                    'constuctor': TOCView
                },
                'history': {
                    'selector': $('#history'),
                    'title':('Switch between versions of'),
                    'constuctor': HistoryView
                },
                'search': {
                    'selector': $('#search'),
                    'title':('Search'),
                    'constuctor': SearchView
                }
            };

            if ($.cookie('Drawer_State') === undefined) {
                this.childViews['table-of-contents'].view = new TOCView({el: '#toc'});
                this.changeContents('table-of-contents');
            } else {
                this.childViews[$.cookie('Drawer_State')].view = new this.childViews[$.cookie('Drawer_State')].constructor();
                this.changeContents($.cookie('Drawer_State')); 
            }
        },

        changeContents: function(activeId) {
            this.$children.addClass('hidden');
            this.childViews[activeId]['selector'].removeClass('hidden');

            this.$label.html(this.childViews[activeId]['title']);
            Dispatch.set('drawerState', activeId);

            $.cookie('Drawer_State', activeId);

        }

    });

    return DrawerView;
});
