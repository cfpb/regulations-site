define('sub-head-view', ['jquery', 'underscore', 'backbone', 'regs-helpers', 'header-events'], function($, _, Backbone, RegsHelpers, HeaderEvents) {
    'use strict';
    var SubHeadView = Backbone.View.extend({
        el: '#content-header',

        initialize: function() {
            this.externalEvents = HeaderEvents;

            this.externalEvents.on('section:open', this.changeTitle, this);
            this.externalEvents.on('search-results:open', this.displayCount, this);
            this.externalEvents.on('search-results:open',this.changeDate, this);
            this.externalEvents.on('clear', this.reset, this);
            this.externalEvents.on('subpart:present', this.renderSubpart,this);
            this.externalEvents.on('subpart:absent', this.removeSubpart, this);

            // cache inner title DOM node for frequent reference
            this.$activeTitle = this.$el.find('.header-label');

            // same for subpart label
            this.$subpartLabel = this.$el.find('.subpart');
        },

        // populates subhead with new title
        changeTitle: function(id) {
            this.$activeTitle.html(RegsHelpers.idToRef(id));
        },

        displayCount: function(resultCount) {
            this.$activeTitle.html('<span class="subpart">Search results</span> ' + resultCount);
        },
        
        changeDate: function() {
            this.version = $('section[data-base-version]').data('base-version');
            this.displayDate = $('select[name=version] option[value='+this.version+']').text();
            $('.effective-date').html('<strong>Effective date:</strong> ' + this.displayDate);
        },

        renderSubpart: function(label) {
            this.$subpartLabel.text(label).show();
            this.$activeTitle.addClass('with-subpart');
        },

        removeSubpart: function() {
            this.$subpartLabel.text('').hide();
            this.$activeTitle.removeClass('with-subpart');
        },

        reset: function() {
            this.$activeTitle.html('');
        }
    });

    return SubHeadView;
});
