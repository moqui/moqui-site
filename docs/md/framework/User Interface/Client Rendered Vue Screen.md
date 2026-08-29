# Client Rendered Vue Screen

Moqui has three web wrappers under the webroot screen. They share the same application screen tree (mounted on `apps.xml`); the wrapper only changes how screens are rendered in the browser.

- **/qapps** (default) — Quasar + Vue SPA. Screen content is loaded using the **qvt**, **qjs**, and **qvue** render modes.
- **/vapps** — Vue + Bootstrap SPA. Screen content is loaded using the **vuet**, **js**, and **vue** render modes.
- **/apps** — server-rendered HTML (no Vue router).

The `qapps.xml` and `vapps.xml` screens are SPA shells: they require a login, include Vue and the root instance, and set `allow-extra-path="true"` so the rest of the URL is handled in the browser. Both shells set `confBasePath` to `/apps` (the actual screen tree) and `confLinkBasePath` to `/qapps` or `/vapps` (what you see in the address bar).

Most XML Screens in these SPAs are a **hybrid**: the server renders XML widgets to a Vue template (`qvt` or `vuet`) and the client mounts that template. Screens can also be **100% client rendered** with a Vue component (`.js` / `.qjs` file, or an embedded `.vue` / `.qvue` SFC) and an optional separate template (`.vuet` / `.qvt` file).

The root Vue instance maps render-mode names to URL extensions so the same screen definition can serve both SPAs:

```
# WebrootVue.qvt.js (/qapps)
moqui.urlExtensions = { js:'qjs', vue:'qvue', vuet:'qvt' }

# WebrootVue.js (/vapps)
moqui.urlExtensions = { js:'js', vue:'vue', vuet:'vuet' }
```

`loadComponent` in those files uses `urlExtensions` plus the screen's `render-modes` attribute to pick `.qvue` / `.vue`, `.qjs` / `.js`, or `.qvt` / `.vuet`.

The example component ships both styles. Use those screens as illustrations rather than a widget cookbook.

[TOC levels=2-3]

## Vue + Bootstrap (`vuet` / `/vapps`)

In the **vuet** render mode (under **/vapps**) XML Screens normally use a hybrid of client and server rendering. Screens can also be built that are 100% client rendered with a Vue JS component (**.js** file) and an embedded or separate Vue template (**.vuet** file).

Here is an example screen definition:

[DynamicExampleItems.xml](https://github.com/moqui/example/blob/master/screen/ExampleApp/Example/DynamicExampleItems.xml)

The most important differences from a normal XML Screen are:

* use the screen **render-modes="js,vuet"** attribute so the WebrootVue router and screen loader know this screen supports the js and vuet render modes; for a Vue component with an embedded template instead of a separate file this would be just "js" instead of "js,vuet"
* if the .js and .vuet text is static content on the server, i.e. not an FTL or other template, tell the WebrootVue screen loader that it can be cached using the **server-static="js,vuet"** attribute

Under the **screen.widgets** element there is a single **render-mode** element with a **text** element for **type="js"** and another for **type="vuet"** since this has a separate Vue template file. Here are direct links to the .js and .vuet files:

[ExampleItems.js](https://github.com/moqui/example/blob/master/screen/ExampleApp/Example/DynamicExampleItems/ExampleItems.js)
[ExampleItems.vuet](https://github.com/moqui/example/blob/master/screen/ExampleApp/Example/DynamicExampleItems/ExampleItems.vuet)

This is a very simple example with an add form and a list of items. The add form demonstrates Vue component data binding and a method to handle the form submit in the browser. The list of items demonstrates iterating over a list that is loaded from the server with a jQuery.ajax() call.

With this approach the screen runs in the context of the WebrootVue root component, which handles routing and various other things. As with standard Vue JS that can be referenced in other components using **this.$root**, which is how the .js script in this example gets the **exampleId** parameter from the **currentParameters** object in the WebrootVue component. That `this.$root.currentParameters` pattern is still used in the Quasar root instance as well.

Vue components used in Moqui vuet templates can also be used, such as the **drop-down** component used in this example (which supports data binding with the **v-model** attribute).

Visit this screen at `http://localhost:8080/vapps/example/Example/DynamicExampleItems`. Because it declares only `js,vuet` (not `qjs`/`qvt`), it is the Bootstrap SPA example, not the default Quasar UI.

## Quasar (`qvt` / `/qapps`)

**/qapps** is the default UI. XML Screens that do not declare a limited `render-modes` list are rendered through the **qvt** macros (`DefaultScreenMacros.qvt.ftl`) inside the Quasar shell — still a hybrid of server-rendered widgets and client Vue.

For a 100% client-rendered screen under Quasar, the example component has a counterpart:

[DynamicExampleItemsVue.xml](https://github.com/moqui/example/blob/master/screen/ExampleApp/Example/DynamicExampleItemsVue.xml)

That screen uses **render-modes="vue,qvue"** and **server-static="vue,qvue"**. Under `/qapps`, `urlExtensions.vue` is `qvue`, so `loadComponent` requests the screen with a `.qvue` extension and parses it with `http-vue-loader`. Under `/vapps` the same screen is requested as `.vue`.

The Vue SFC is inline in a `render-mode` **text** element with **type="vue,qvue"** (template plus `module.exports` script). It is the same add-form / item-list illustration as the vuet example: `v-model` binding, a client `addItem()` method, and a `mounted` hook that reads **this.$root.currentParameters.exampleId** and loads rows with `$.ajax()` from a transition on the sibling `DynamicExampleItems` screen (URL under `/apps/...`, matching `confBasePath`).

Visit it at `http://localhost:8080/qapps/example/Example/DynamicExampleItemsVue`.

The example is deliberately small. It is not a Quasar component cookbook; for XML Form widgets under `/qapps` use the qvt screen macros rather than hand-written Quasar markup unless you need a custom client screen like this one.
