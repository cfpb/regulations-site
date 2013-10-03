define('sxs-list-view', ['jquery', 'underscore', 'backbone', 'dispatch', 'sidebar-list-view', './folder-model', 'sxs-view'], function($, _, Backbone, Dispatch, SidebarListView, FolderModel, SxSView) {
    'use strict';
    var SxSListView = SidebarListView.extend({
        el: '#sxs-list',

        events: {
            'click .sxs-link': 'openSxS'
        },

        initialize: function() {
            this.model = new FolderModel({supplementalPath: 'sidebar'});
            this.render = _.bind(this.render, this);

            Dispatch.on('regSection:open:after', this.getSidebar, this);

            this.modifyListDisplay();
        },

        openSxS: function(e) {
            if (window.history && window.history.pushState) {
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
            }
        },

        getSidebar: function(sectionId) {
            var partial = this.model.get(sectionId, this.render);
        },

        render: function(html) {
            var $html = $(html),
                list = $html.find('#sxs-list').html();
            this.$el.html(list);

            this.modifyListDisplay();

            // @TODO: move permalink updating to somewhere sane
            Dispatch.trigger('sidebar:update', $html.find('#permalinks'));
        },

        modifyListDisplay: function() {
            var $folderContent = this.$el.find('.expand-drawer');
            if ($folderContent.children().length > 0) {
                this.highlightHeader();
            }
        },

        highlightHeader: function() {
            this.$el.find('header').addClass('has-content');
        }

    });

    return SxSListView;
});
