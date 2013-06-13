define('toc-view', ['jquery', 'underscore', 'backbone', 'regs-fixed-el-view', 'regs-dispatch'], function($, _, Backbone, RegsFixedElView, Dispatch) {
    'use strict';
    var TOCView = RegsFixedElView.extend({
        initialize: function() {
            Dispatch.on('activeSection:change', this.setActive, this);
        },

        setActive: function(id) {
            this.$el.find('.current').removeClass('current');
            this.$el.find('a[href=#' + id + ']').addClass('current');

            return this;
        }
    });

    return TOCView;
});
