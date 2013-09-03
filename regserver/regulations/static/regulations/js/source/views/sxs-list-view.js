define('sxs-list-view', ['jquery', 'underscore', 'backbone', 'dispatch', 'sidebar-list-view', './folder-model', 'sxs-view'], function($, _, Backbone, Dispatch, SidebarListView, FolderModel, SxSView) {
    'use strict';
    var SxSListView = SidebarListView.extend({
        el: '#sxs-list',

        events: {
            'click a': 'openSxS'
        },

        initialize: function() {
            var analyses = this.$el.find('.chunk');
            this.model = new FolderModel({supplementalPath: 'sidebar'});

            this.model.set(Dispatch.getOpenSection(), analyses);

            Dispatch.on('section:open', this.getAnalyses, this);

            this.truncateLinks();
            this.highlightHeader(this.$el);
        },

        openSxS: function(e) {
            e.preventDefault();

            var $sxsLink = $(e.target),
                paragraphId = $sxsLink.data('sxs-paragraph-id'),
                docNumber = $sxsLink.data('doc-number');

            Dispatch.set('sxs-analysis', new SxSView({
                    regParagraph: paragraphId,
                    docNumber: docNumber,
                    fromVersion: Dispatch.getVersion()
                })
            );
        },

        getAnalyses: function(sectionId) {
            var partial = this.model.get(sectionId);

            if (typeof partial.done !== 'undefined') {
                partial.done(function(sxs) {
                    this.render(sxs);
                }.bind(this));
            }
            else {
                this.render(partial);
            }
        },

        render: function(html) {
            var $html = $(html),
                list = $html.find('#sxs-list').html();
            this.$el.html(list);

            this.truncateLinks();
            this.highlightHeader($html);
        },

        highlightHeader: function($html) {
            if ($html.find('.expand-drawer').children().length > 0) {
                this.$el.find('h4').addClass('has-content');
            }
        },

        truncateLinks: function() {
            this.$el.find('li').each(function(i, li) {
                var $link = $(li).find('a'),
                    pid = $link.text();
                $link.text(pid.split('.')[1]);
            });
        }
    });

    return SxSListView;
});
