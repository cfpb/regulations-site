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

            this.model.set(Dispatch.getOpenSection(), analyses.innerHTML);

            Dispatch.on('regSection:open:after', this.getAnalyses, this);

            this.modifyListDisplay();
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

            this.modifyListDisplay();
        },

        modifyListDisplay: function() {
            var $folderContent = this.$el.find('.expand-drawer');
            if ($folderContent.children().length > 0) {
                this.highlightHeader();
            }
            else {
                $folderContent.text('No analysis available for ' + Dispatch.getOpenSection());
            }
        },

        highlightHeader: function() {
            this.$el.find('h4').addClass('has-content');
        }
    });

    return SxSListView;
});
