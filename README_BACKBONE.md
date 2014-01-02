# Understanding and using the eRegulations Backbone Application

- [How is content identified?](#how-is-content-identified)
- [How does eRegulations' Backbone layer receive data?](#how-does-eregulations-backbone-layer-receive-data)
- [How is Backbone used?](#how-is-backbone-used)
- [How should I add a new feature?](#how-should-i-add-a-new-feature)

## How is content identified?
Regulations are very large and structured documents. The application loads regulations section by section. Sections and paragraphs can also have different applications outside of the flow of reg text. For example, a paragraph will define a term, and so we sometimes display this data outside of the content area (in the sidebar) in its other context - as a definition.

**The id of a piece of content is a dash-delimited string containing the section, part and paragraphs that identify the content in the regulation.** To learn about this structure, see pages 5 and 6 of [this PDF](http://www.archives.gov/federal-register/tutorial/tutorial_060.pdf).

For example, section 1005.2(a)(3)(iii) would have the id 1005-2-a-3-iii.

## How does eRegulations’ Backbone layer receive data?
The Backbone application does not consume an API. Everything that makes eRegulations unique relies on layers of transformations to the plain regulation text. These transformations happen server side. The application pulls in rendered partial templates from Django. The application is agnostic about the content itself but relies on ids and certain data attributes in the markup for context.

## How is Backbone used?
eRegulations uses Backbone in a non-standard fashion. It uses the following Backbone components:
- [Models](http://backbonejs.org/#Model)
- [Views](http://backbonejs.org/#View)
- [Router](http://backbonejs.org/#Router)
- [Events](http://backbonejs.org/#Events)

### Models
eRegulations’ Backbone Models do not sync data in a standard Backbone way. Because data only needs to travel one direction, from the server to the client, we do not use built-in events to trigger standard data sync processes. 

**The model caches data in a key-value pair**. The key is the id of the section and the value is a string of HTML containing the content. Example:

```{
    ‘1005-2-a’: ‘<li id=”1005-2-a”>Paragraph content</li>’
}```

All models inherit from [meta-model](regulations/static/regulations/js/source/models/meta-model.js). The cycle of a model is as follows:
- A view is created for a piece of content. The view calls [get()](regulations/static/regulations/js/source/models/meta-model.js#L60) on its model.
- The model checks to see if it has the content cached in memory.

If not:
- The model constructs a URL to request data from the server and makes the AJAX request and creates a Promise object
- When the Promise resolves:
 - A callback passed from the view is called
 - The newly-fetched data is cached

If it is:
- The model retrieves the relevant value from its key-value store by the id passed in and returns the value

### Views
There are two levels of views: content area views and content views. 

#### Content area views
There is one of these for each area of the UI:
- [Header](regulations/static/regulations/js/source/views/header/header-view.js)
- [Drawer (left side expanding navigation)](regulations/static/regulations/js/source/views/drawer/drawer-view.js)
- [Main](regulations/static/regulations/js/source/views/main/main-view.js)
- [Sidebar](regulations/static/regulations/js/source/views/sidebar/sidebar-view.js)
- [Breakaway (used when opening a Section by Section Analysis)](regulations/static/regulations/js/source/views/breakaway/breakaway-view.js)

**These views are responsible for creating and removing subchildren that hold content.** It also handles loading states as applicable (ex: translucent overlays over loading content). 

It builds the configuration object that is passed into the child view’s constructor. In Backbone, this is ```this.options``` in the child view’s constructor. This object is used for many things, including context to events that occur during the creation of a new child view.

**Content area views are, by convention, singletons.** They are initialized when they are first loaded as dependencies by [Require.js](http://requirejs.org/).

#### Content views (child views)
All main content area child views inherit from [ChildView](regulations/static/regulations/js/source/views/main/child-view.js). **Content views are responsible for reacting to user input on the data.** A content view is created to display a particular piece of content and is removed once a user navigates away from that content.

### Events
None of the events built into Backbone are used. As the flow of the eRegulations application is different from a vanilla Backbone application, we use custom events.

Each content area view has an associated events router. By convention, each view - both content area and child views - know its associated event router as ```this.externalEvents```. It is intended that all communication cross-content area happen through these event routers.

**To understand the cycle of any view, look at the methods bound to events in the view’s constructor.** Event handlers are bound with [Backbone’s on()](http://backbonejs.org/#Events-on). Events are triggered using [Backbone’s trigger()](http://backbonejs.org/#Events-trigger). Event names follow the [Backbone convention.](http://backbonejs.org/#Events-on)

There are five distinct modules, one for each content area, but this is just for ease when including them as dependencies with [Require.js](http://requirejs.org/). They are all clones of [Backbone.Events](http://backbonejs.org/#Events) with no modifications.

## How should I add a new feature?
The intention for this JS application is that, as new ways to parse, glean context and display the data become possible, it can easily flex to meet these needs.

To develop along the grain, so to speak, you should consider the following:

- Can I employ the existing pattern of content area and content views to my new feature?
- Can I develop the new feature without adding an explicit state to the application? Can my new feature simply respond to events w/o other modules knowing about it?
- Can the way this feature is developed neatly fit into the existing event stream?
- Can I create this without making any transformations to content client side?
