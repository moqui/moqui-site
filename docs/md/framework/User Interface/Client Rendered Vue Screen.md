# Client Rendered Vue Screen

In the **vuet** render mode (under **/vapps** in the OOTB applications) XML Screens normally use a hybrid of client and server rendering. Screens can also be build that are 100% client rendered with a Vue JS component (**.js** file) and an embedded or separate Vue template (**.vuet** file).

Here is an example screen definition:

[DynamicExampleItems.xml](https://github.com/moqui/example/blob/master/screen/ExampleApp/Example/DynamicExampleItems.xml)

The most important differences from a normal XML Screen are:

* use the screen **render-modes="js,vuet"** attribute to tell the WebrootVue router and screen loader that this screen support the js and vuet render modes; for a Vue component with an embedded template instead of in a separate file this would be just "js" instead of "js,vuet"
* if the .js and .vuet text is static content on the server, ie not an FTL or other templtes, tell the WebrootVue screen loader that it can be cached using the **server-static="js,vuet"** attribute

Under the **screen.widgets** element there is a single **render-mode** element with a **text** element for **type="js"** and another for **type="vuet"** since this has a separate Vue template file. Here are direct links to the .js and .vuet files:

[ExampleItems.js](https://github.com/moqui/example/blob/master/screen/ExampleApp/Example/DynamicExampleItems/ExampleItems.js)
[ExampleItems.vuet](https://github.com/moqui/example/blob/master/screen/ExampleApp/Example/DynamicExampleItems/ExampleItems.vuet)

This is a very simple example with an add form and a list of items. The add form demonstrate Vue component data binding and a method to handle the form submit in the browser. The list of items demonstrates iterating over a list that is loaded from the server with an jQuery.ajax() call. 

With this approach the screen runs in the context of the WebrootVue root component which handle routing and various other things. As with standard Vue JS that can be referenced in other components using **this.$root** which is how the .js script in this example gets the **exampleId** parameter from the **currentParameters** object in the WebrootVue component.

Vue components used in Moqui vuet templates can also be used, such as the **drop-down** component used in this example (which supports data binding with the **v-model** attribute).
