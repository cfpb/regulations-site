// **Extends** SidebarModuleView
//
// **TODO** Determine how much sense that still makes ^^
//
// **Usage** ```require(['definition-view'], function(DefinitionView) {})```
//
// A single inline interpretation, child of the sidebar
// As of sprint 6, the only View that is instantiated more than once
define('definition-view', ['jquery', 'underscore', 'backbone', 'sidebar-module-view', 'reg-model', 'dispatch', 'regs-helpers', './regs-router'], function($, _, Backbone, SidebarModuleView, RegModel, Dispatch, RegsHelpers, Router) {
    'use strict';

    // **Constructor**
    // this.options:
    // 
    // * **id** string, dash-delimited id of definition paragraph
    // * **$anchor** jQobj, the reg-view link that opened the def
    //
    // this.options turns into this.model
    var DefinitionView = SidebarModuleView.extend({
        className: 'open-definition',
        events: {
            'click .close-button.tab-activated': 'close',
            'click .close-button': 'headerButtonClose',
            'click .definition': 'sendDefinitionLinkEvent',
            'click .continue-link': 'sendContinueLinkEvent'
        },

        formatInterpretations: function() {
            var interpretation = this.$el.find('.inline-interpretation'),
                interpretationId;

            if (typeof interpretation[0] !== 'undefined') {
                interpretationId = $(interpretation[0]).data('interp-id');
                interpretation.remove();

                this.$el.children('.definition-text').append(
                    RegsHelpers.fastLink(
                        '#' + interpretationId, 
                        'Official Interpretation',
                        'continue-link internal interp'
                    )
                );
            }
        },

        removeHeadings: function() {
            var keyTerm = this.$el.find('dfn.key-term'),
                keyTerms;

            if (typeof keyTerm[0] !== 'undefined') {
                keyTerms = keyTerm.length;

                for (var i = 0; i < keyTerms; i++) {
                    $(keyTerm[i]).remove(); 
                }
            }
        },

        definitionRouter: function(paragraph, actionText) {
            var targetSection;
            if (paragraph.indexOf('Interp') === -1) {
                targetSection = paragraph.split('-').slice(0,2).join('-');
            } else {
                // Interpretations all live in the same place
                targetSection = paragraph.split('-')[0] + '-Interp';
            }
            if (targetSection === Dispatch.getOpenSection()) {
                // Definition is on this page
                Dispatch.trigger('ga-event:definition', {
                    action: actionText,
                    context: '#' + paragraph
                });
            } else {
                // Definition is on a different page
                Router.navigate(targetSection + '/' + Dispatch.getVersion() + '#' + paragraph, {'trigger': true});
            }
        },

        sendContinueLinkEvent: function(e) {
            e.preventDefault();
            this.definitionRouter($(e.target).attr('href').substr(1), 'clicked continue link');
        },

        sendDefinitionLinkEvent: function(e) {
            e.preventDefault();
            this.definitionRouter($(e.target).data('definition'), 'clicked term inside definition');
        },

        render: function() {
            var defHTML = RegModel.get(this.model.id);

            if (typeof defHTML.done !== 'undefined') {
                defHTML.done(function(res) {
                    this.template(res);
                }.bind(this));
            }
            else {
                this.template(defHTML);
            }

            return this;
        },

        template: function(res) {
            var $defText;
            this.$el.html('<div class="definition-text">' + res + '</div>');

            $defText = this.$el.find('.definition-text');

            this.$el.prepend('<div class="sidebar-header group"><h4>Defined Term<a class="right close-button" href="#">Close definition</a></h4></div>');

            // link to definition in content body
            $defText.append(
                RegsHelpers.fastLink(
                    '#' + this.model.id, 
                    RegsHelpers.idToRef(this.model.id),
                    'continue-link internal'
                )
            );

            // remove inline interpretation, add interpretation link
            this.formatInterpretations();
            this.removeHeadings();

            // make definition tabbable
            this.$el.attr('tabindex', '0');
                // make tab-activeated close button at bottom of definition content
            $defText.append('<a class="close-button tab-activated" href="#">Close definition</a>');

            // **Event trigger** triggers definition open event
            Dispatch.trigger('definition:render', this.$el);

            // set focus to the open definition
            this.$el.focus();

            return this;
        },

        close: function(e) {
            e.preventDefault();
            Dispatch.remove('definition');
            Dispatch.trigger('ga-event:definition', {
                action: 'closed definition by tab-revealed link',
                context: this.model.id
            });
            Dispatch.trigger('definition:remove', this.model.id);
        },

        headerButtonClose: function(e) {
            e.preventDefault();
            Dispatch.remove('definition');
            Dispatch.trigger('ga-event:definition', 'close by header button');
            Dispatch.trigger('definition:remove', this.model.id);
        },

        remove: function() {
            this.stopListening();
            this.$el.remove();
            // **Event trigger** notifies app that definition is removed
            Dispatch.trigger('sidebarModule:remove', this.model.id);

            return this;
        }
    });

    return DefinitionView;
});
