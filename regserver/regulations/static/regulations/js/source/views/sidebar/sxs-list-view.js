define('sxs-list-view', ['jquery', 'underscore', 'backbone', 'dispatch', 'sidebar-list-view', './folder-model', 'sxs-view', './regs-router'], function($, _, Backbone, Dispatch, SidebarListView, FolderModel, SxSView, Router) {
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
            Dispatch.on('sxs:route', this.createSxSView, this);

            this.modifyListDisplay();

            // if the browser doesn't support pushState, don't 
            // trigger click events for links
            if (Dispatch.hasPushState() === false) {
                this.events = {};
            }
        },

        openSxS: function(e) {
            e.preventDefault();

            var $sxsLink = $(e.target);

            this.createSxSView({
                    'regParagraph': $sxsLink.data('sxs-paragraph-id'),
                    'docNumber': $sxsLink.data('doc-number'),
                    'fromVersion': Dispatch.getVersion()
                },
                function(sxsURL) {
                    if (Dispatch.hasPushState()) {
                        Router.navigate('sxs/' + sxsURL);
                    }
                }
            );
        },

        createSxSView: function(options, callback) {
            var sxsURL = options.regParagraph + '/' + options.docNumber + '?from_version=' + options.fromVersion;

            Dispatch.set('sxs-analysis', new SxSView({
                    'regParagraph': options.paragraphId,
                    'docNumber': options.docNumber,
                    'fromVersion': options.version,
                    'url': sxsURL
                })
            );

            if (typeof callback !== 'undefined') {
                callback(sxsURL);
            }
        },

        getSidebar: function(sectionId) {
            this.model.get(sectionId, this.render);
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
