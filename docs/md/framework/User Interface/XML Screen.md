# XML Screen

Screens in Moqui are organized in two ways:

-   each screen exists in a hierarchy of subscreens
-   a screen may be a node in a graph tied to other nodes by transitions

The hierarchy model is used to reference the screen, and in a URL specify which screen to render by its path in the hierarchy. Screens also contain links to other screens (literally a hyperlink or a form submission) that are more like the structure of going from one node to another in a graph through a transition.
 
[TOC levels=2-3]
 
## Subscreens

The subscreen hierarchy is primarily used to dynamically include another screen, a subscreen or child screen. The subscreens of a screen can also be used to populate a menu.

When a screen is rendered it is done with a root screen and a list of screen names.

The root screen is configured per webapp in the Moqui Conf XML file with the *moqui-conf.webapp-list.webapp.root-screen* element. Multiple root screens can be configured per webapp based on a hostname pattern, providing a convenient means of virtual hosting within a single webapp.

You should have at least one catchall root-screen element meaning that the **host** is set to the regular expression ".\*". The `MoquiDefaultConf.xml` file uses the default **webroot** component and its root screen which you can override in a runtime or component Moqui Conf XML file.

If the list of subscreen names does not reach a leaf screen (with no subscreens) then the default subscreen, specified with the *screen.subscreens*.**default-item** attribute will be used. Because of this any screen that has subscreens should have a default subscreen.

There are **four** ways to add subscreens to a screen:

1.  **Directory Structure**: for screens within a single application, by directory structure: create a directory in the directory where the parent screen is named the same as the parent screen's filename and put XML Screen files in that directory (**name**=filename up to .xml, **title**=*screen*.**default-menu-title**, **location**=parent screen minus filename plus directory and filename for subscreen)
2.  **Screen XML File**: to include screens that are part of another application, or shared and not in any application, use the *subscreens-item* element under the *screen.subscreens* element
3.  **Database Record**: to add and remove subscreens anywhere in the screen tree or change order and title of subscreens, use records in the *moqui.screen.SubscreensItem* entity
4.  **Moqui Conf XML File**: a configuration-file based alternative to the Database Record approach, most useful for adding subscreens without modifying the screen to mount under; this is usually done in a `MoquiConf.xml` in a component directory where you can put any Moqui Conf XML settings including the *screen.subscreens-item* element under the *screen-facade* element

For #1 (**Directory Structure**) a directory structure would look something like this (from the Example application):

-   ExampleApp.xml
-   ExampleApp
    -   Feature.xml
    -   Feature
        -   FindExampleFeature.xml
        -   EditExampleFeature.xml
    -   Example.xml
    -   Example
        -   FindExample.xml
        -   EditExample.xml

The pattern to notice is that if there are subscreens there should be a directory with the same name as the XML Screen file, just without the .xml extension. The `Feature.xml` file is an example of a screen with subscreens, whereas the `FindExampleFeature.xml` has no subscreens (it is a leaf in the hierarchy of screens).

For approach #2 (**Screen XML File**) the *subscreens-item* element would look something like this element from the `apps.xml` file used to mount the Example app’s root screen:

```
<subscreens-item name="example" menu-title="Example" menu-index="8"  
    location="component://example/screen/ExampleApp.xml"/>
```

For #3 (**Database Record**) the record in the database in the SubscreensItem entity would look something like this (an adaptation of the XML element above):

```
<moqui.screen.SubscreensItem subscreenName="example" userGroupId="ALL_USERS"
     menuTitle="Example" menuIndex="8" menuInclude="Y"
     screenLocation="component://webroot/screen/webroot/apps.xml"
     subscreenLocation="component://example/screen/ExampleApp.xml"/>
```

For #4 (**Moqui Conf XML File**) you can put these elements in any of the Moqui Conf XML files that get merged into that runtime configuration. The main way to do this is in a `MoquiConf.xml` file in your component directory so the configuration is in the same component as the screens and you don't have to modify and maintain files elsewhere. See more details about the Moqui Conf XML options in the [Run and Deploy](/docs/framework/Run+and+Deploy) instructions. Here is an example from the `MoquiConf.xml` file in the moqui/example component:

```
<screen-facade>
    <screen location="component://webroot/screen/webroot/apps.xml">
        <subscreens-item name="example" menu-title="Example" menu-index="97" 
            location="component://example/screen/ExampleApp.xml"/>
    </screen>
</screen-facade>
```

Within the widgets (visual elements) part of your screen you specify where to render the active subscreen using the *subscreens-active* element. You can also specify where the menu for all subscreens should be rendered using the *subscreens-menu* element. For a single element to do both with a default layout use the *subscreens-panel* element.

Applications are mounted on `component://webroot/screen/webroot/apps.xml` (as in the example `MoquiConf.xml` above). The webroot screen then chooses which wrapper sits above that tree. In `webroot.xml` the default subscreen is **qapps**:

```
<subscreens default-item="qapps">
    <subscreens-item name="toolstatic" location="component://tools/screen/toolstatic.xml" menu-include="false"/>
</subscreens>
```

`qapps.xml` and `vapps.xml` are SPA shells (`allow-extra-path="true"`). They render a Vue root page and load screen content from the `/apps` tree. `apps.xml` is the server-rendered HTML wrapper. So the same Example app is:

- `http://localhost:8080/qapps/example/...` — default Quasar UI
- `http://localhost:8080/vapps/example/...` — Vue + Bootstrap SPA
- `http://localhost:8080/apps/example/...` — server-rendered HTML

The *subscreens.conditional-default* element is still available if you need a condition-based default item (it is just no longer used in `webroot.xml`).

Once a screen such as FindExample is rendered through one of these wrappers, its links retain that base screen path in URLs generated from relative screen paths so the user stays in the path the original default pointed to.

## Screen Extend

To change a screen you do not own, put a `screen-extend` XML file in your component under `screen-extend/` with a path and filename that matches the original screen (the path under that component's `screen/` directory, or the full location after `://`). The extend file can add parameters, transitions, and subscreens, insert or replace actions (`actions-extend` with `when` = before, after, or replace), and insert widgets (`widgets-extend` matching a `name` or `id`, `where` = before or after). Forms and sections in the extend file merge with or override the originals by name. This is how add-on components such as `moqui-sso` attach to the Login screen without forking it.

## Standalone Screen

Normally screens will be rendered following the render path, starting with the root screen. Each screen along the way may add to the output. A screen further down the path that is rendered without any previous screens in the path adding to the output is a "standalone" screen.

This is useful when you want a screen to control all of its output and not use headers, menus, footers, etc from the screen it is under in the subscreens hierarchy.

There are two ways to make a screen standalone:

-   set the *screen*.**standalone** attribute to true to make the screen always standalone
-   to render any screen standalone pass in the **lastStandalone**=true parameter, or set it in a screen pre-action (action under the *screen.pre-actions* element)

The first option is most useful for screens that are the root of an application separate from the rest and that need different decoration and such. The second option is most useful for screens that are sometimes used in the context of an application, and other times used to produce undecorated output like a CSV file or for loading dynamically in a dialog window or screen section.

## Screen Transition

A transition is defined as a part of a screen and is how you get from one screen to another, processing input if applicable along the way. A transition can of course come right back to the same screen and when processing input often does.

The logic in transitions (transition actions) should be used only for processing input, and not for preparing data for display. That is the job of screen actions which, conversely, should not be used to process input (more on that below).

When an XML Screen is running in a web application the transition comes after the screen in the URL. In any context the transition is the last entry in the list of subscreen path elements. For example the first path goes to the EditExample screen, and the second to the **updateExample** transition within that screen (under `/apps`; in the default UI use `/qapps/example/...`):

/apps/example/Example/EditExample

/apps/example/Example/EditExample/updateExample

When a transition is the target of an HTTP request any actions associated with the transition will be run, and then a redirect will be sent to ask the HTTP client (usually a web browser) to go to the URL of the screen the transition points to. If the transition has no logic and points right to another screen or external URL when a link is generated to that transition it will automatically go to that other screen or external URL and skip calling the transition altogether. Note that these points only apply to an XML Screen running in a web-based application.

A simple transition that goes from one screen to another, in this case from FindExample to EditExample, looks like this:

```
<transition name="editExample">
    <default-response url="../EditExample"/>
</transition>
```

The path in the **url** attribute is based on the location of the two screens as siblings under the same parent screen. In this attribute a simple dot (".") refers to the current screen and two dots ("..") refer to the parent screen, following the same pattern as Unix file paths.

For screens that have input processing the best pattern to use is to have the transition call a single service. With this approach the service is defined to agree with the form that is submitted to the corresponding transition. This makes the designs of both more clear and offers other benefits such as some of the validations on the service definition being used to generate matching client-side validations. When a *service-call* element is directly under a *transition* element it is treated a bit differently than if it were in an actions block and it automatically gets in-parameters from the context (equivalent to **in-map**="context") and puts out-parameters in the context (equivalent to **out-map**="context").

This sort of transition would look like this (the **updateExample** transition on the `EditExample` screen):

```
<transition name="updateExample">
    <service-call name="org.moqui.example.ExampleServices.update#Example"/>
    <default-response url="."/>
</transition>
```

In this case the *default-response*.**url** attribute is simply a dot which refers to the current screen and means that after this transition is processed it will go to the current screen.

A screen transition can also have actions instead of a single service call by using the *actions* element. If a transition has both service-call and actions elements the *service-call* will be run first and then the *actions* will be run. Just as with all *actions* elements in all XML files in Moqui, the subelements are standard Moqui XML Actions that are transformed into a Groovy script. This is what a screen transition with actions might look like (simplified example, also from the `FindExample` screen):

```
<transition name="getExampleTypeEnumList">
    <actions>
        <entity-find entity-name="..." list="...">
          <econdition field-name="..." from="..."/>
          <order-by field-name="..."/>
        </entity-find>
        <script>ec.web.sendJsonResponse([exampleTypeEnumList:exampleTypeEnumList])</script>
    </actions>
    <default-response type="none"/>
</transition>
```

This example also shows how you would do a simple entity find operation and return the results to the HTTP client as a JSON response. Note the call to the *ec.web*.**sendJsonResponse**() method and the none value for the *default-response*.**type** attribute telling it to not process any additional response.

As implied by the element *default-response* you can also conditionally choose a response using the *conditional-response* element. This element is optional and you can specify any number of them, though you should always have at least one *default-response* element to be used when none of the conditions are met. There is also an optional *error-response* which you may use to specify the response in the case of an error in the transition actions.

A transition with a *conditional-response* would look something like this simplified example from the `DataExport` screen:

```
<transition name="EntityExport.xml">
  <actions>
    <script><![CDATA\[if (...) noResponse = true]]></script>
  </actions>
  <conditional-response type="none">
    <condition>
      <expression>noResponse</expression>
    </condition>
  </conditional-response>
  <default-response url="."/>
</transition>
```

This is allowing the script to specify that no response should be sent (when it sends back the data export), otherwise it transitions back to the current screen. Note that the text under the condition.expression element is simply a Groovy expression that will be evaluated as a boolean.

All \*-response elements can have parameter subelements that will be used when redirecting to the url or other activating of the target screen. Each screen has a list of expected parameters so this is only necessary when you need to override where the parameter value comes from (default defined in the parameter tag under the screen) or to pass additional parameters.

Here are the shared attributes of the *default-response*, *conditional-response*, and *error-response* elements:

|                         |                                                                                                                                                                                                                                                                                           |
|---------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **type**                    | Defaults to url, can be :<br> **none** : No response, do nothing aside from the transition actions. <br> **screen-last** : Go to the screen from the last request unless there is a saved one from some previous request (using the save-current-screen attribute, done automatically for login). If no last screen is found the value in the url will be used, and if nothing there will go to the default screen (just to root with whatever defaults are setup for each subscreen). <br>  **screen-last-noparam** : Like screen-last but don’t pass through any parameters. <br>  **url** : Redirect to the URL specified in the url attribute, of url-type |
| **url**                      | The URL to follow in response, based on **url-type**. The default **url-type** is screen-path which means the value here is a path from the current screen to the desired screen, transition, or sub-screen content.     <br><br> Use "." to represent the current screen, and ".." to represent the parent screen on the runtime screen path. The ".." can be used multiple times, such as "../.." to get to the parent screen of the parent screen (the grand-parent screen). If the screen-path type url starts with a "/" it will be relative to the root screen instead of relative to the current screen.<br><br>If **url-type** is plain then this can be any valid URL (relative on current domain or absolute). |
| **url-type**            | Can be either screen-path (default) or plain. Normally responses will go to another screen, hence the default, but if you want to go to a relative or absolute URL use the plain type. |
| **parameter-map**       | Just like the parameter subelement can be used to specify parameters to pass with the redirect. |
| **save-current-screen** | Save the current screen's path and parameters for future use, generally with the screen-last **type** of response. |
| **save-parameters**     | Save the current parameters (and request attributes) before doing a redirect so that the screen rendered after the redirect renders in a context similar to the original request to the transition. |

## Parameters and Web Settings

One of the first things in a screen definition is the parameters that are passed to the screen. This is used when building a URL to link to the screen or preparing a context for the screen rendering. You do this using the *parameter* element, which generally looks something like this:

```
<parameter name="exampleId"/>
```

The **name** attribute is the only required one, and there are others if you want a default static value (with the **value** attribute) or to get the value by default from a field in the context other than one matching the parameter name (with the **from** attribute).

While parameters apply to all render modes there are certain settings that apply only when the screen is rendered in a web-based application. These options are on the *screen.web-settings* element, including:

-   **allow-web-request**: Defaults to true. Set to false to not allow access to an HTTP client.
-   **require-encryption**: Defaults to true. Set to false for screens that are less secure and don’t require encryption (i.e. HTTPS).
-   **mime-type**: Defaults to text/html. This can vary based on how the screen is rendered (the render mode) but when always producing a certain type of output set the corresponding mime type here.
-   **character-encoding**: Defaults to UTF-8 for text output. If you are rendering text with a different encoding, set it here.

## Screen Actions, Pre-Actions, and Always Actions

Before rendering the visual elements (widgets) of a screen data preparation is done using XML Actions under the *screen.actions* element. These are the same XML Actions used for services and other tools and are described in [Logic and Services](/docs/framework/Logic+and+Services). There are elements for running services and scripts (inline Groovy or any type of script supported through the Resource Facade), doing basic entity and data moving operations, and so on.

Screen actions should be used only for preparing data for output. Use transition actions to process input.

When screens are rendered it is done in the order they are found in the screen path and the actions for each screen are run as each screen in the list is rendered. To run actions before the first screen in the path is rendered use the *pre-actions* element. This is used mainly for preparing data needed by screens that will include the current screen (i.e., before the current screen in the screen path). When using this keep in mind that a screen can be included by different screens in different circumstances.

If you want actions to run before the screen renders and before any transition is run, then use the *always-actions* element. The main difference between *always-actions* and *pre-actions* is that the *pre-actions* only run before a screen or subscreen is rendered, while *always-actions* will run before any transition in the current screen and any transition in any subscreen. The *always-actions* also run whether the screen will be rendered, while the *pre-actions* only run if the screen will be rendered (i.e., is below a standalone screen in the path).

## XML Screen Widgets

The elements under the *screen.widgets* element are the visual elements that are rendered, or when producing text that actually produce the output text. The most common widgets are XML Forms (using the *form-single* and *form-list* elements) and included templates. See [XML Form](/docs/framework/User+Interface/XML+Form) for details about XML Forms.

While XML Forms are not specific to any render mode, templates by their nature are particular to a specific render mode. This means that to support multiple types of output you’ll need multiple templates. The `webroot.xml` screen (the default root screen) has an example of including multiple templates for different render modes:

```
<render-mode>
 <text type="html" no-boundary-comment="true"
 location="component://webroot/screen/includes/Header.html.ftl"/>
 <text type="xsl-fo" no-boundary-comment="true"
 location="component://webroot/screen/includes/Header.xsl-fo.ftl"/>
</render-mode>
```

The same screen also has an example of supporting multiple render modes with inline text:

```
<render-mode>
 <text type="html"><![CDATA[</body></html>]]></text>
 <text type="xsl-fo">
 <![CDATA[</fo:flow></fo:page-sequence></fo:root>]]></text>
</render-mode>
```

These are the widget elements for displaying basic things:

-   **link**: a hyperlink to a transition, another screen, or any URL
-   **image**: display an image
-   **label**: display some text

To structure screens use these widget elements:

-   *section*: a named part of a screen with condition, actions, widgets, and fail-widgets (run when the condition evaluates to false)
-   *section-iterate*: like section but is run for each entry in a collection
-   *container*: an area of a screen
-   *container-panel*: an area of a screen structured into a header, footer and left, center and right panels in between
-   *container-dialog*: a screen area that is initially hidden and that pops up when a button is pressed
-   *dynamic-dialog*: a button and placeholder for a popup that loads its content from the server through a transition of the current screen
-   *include-screen*: literally include another screen

## Section, Condition and Fail-Widgets

A section is a special widget that contains other widgets. It can be used anywhere other screen widget elements are used. A section has *widgets*, *condition*, and *fail-widgets* subelements. The screen element also supports these subelements, making it a sort of top-level section of a screen.

The *condition* element is used to specify a condition. If it evaluates to true the widgets under the *widgets* element will be rendered, and if false the widgets under the *fail-widgets* element will be.

## Macro Templates and Custom Elements

Moqui XML Screen and XML Form files are transformed to the desired output using a set of macros in a FreeMarker (FTL) template file. There is one macro for each XML element to produce its output when the screen is rendered.

There are two ways to specify the macro template used to render a screen:

-   for all screens: *moqui-conf.screen-facade.screen-text-output*.**macro-template-location** attribute in the Moqui Conf XML file; there is one screen-text-output element for each render mode (i.e. html, xml, csv, xsl-fo, etc) identified by the *screen-text-output*.**type** attribute
-   for a single screen: *screen.macro-template*.**location** attribute; you can also specify a macro-template element for each render-mode, identified by the *macro-template*.**type** attribute

The location of the macro template can be any location supported by the Resource Facade. The most common types of locations you’ll use for this include component, content, and runtime directory locations.

The default macro templates included with Moqui are specified in the `MoquiDefaultConf.xml` file along with all other default settings. You can override them with your own in the Moqui Conf XML file specified at runtime.

When you use a custom macro template file you don’t need to include a macro for every element you want to render differently. You can start the file with an include of a default macro file or any other macro file you want to use, and then just override the macros for desired elements. An include of another macro file within your file will look something like:

```
<#include "runtime://template/screen-macro/DefaultScreenMacros.html.ftl"/>
```

Default macros live in `runtime/template/screen-macro/` (`DefaultScreenMacros.html.ftl`, `.vuet.ftl`, `.qvt.ftl`, and so on). The example component includes the vuet macros that way in `ExampleScreenMacros.vuet.ftl`.

The location here can also be any location supported by the Resource Facade.

You can use this approach to add your own custom elements. In other words, the macros in your custom macro template file don’t have to be an override of one of the stock elements in Moqui, they can be anything you want.

Use this approach to add your own widget elements and form field types that you want to be consistent across screens in your applications. For example you can add macros for special containers with dynamic HTML like the dialogs in the default macros, or a special form field like a slider or a custom form field widget you create with JavaScript.

When you add a macro for a custom element you can just start using it in your XML Screen files even though they are not validated by the XSD file. If you want them to be validated:

1.  create your own custom XSD file
2.  include one or more of the default Moqui XSD files
3.  add your element definitions to your custom XSD
4.  refer to your custom XSD file in the *screen*.**xsi:noNamespaceSchemaLocation** attribute of your XML Screen file

## CSV, XML, PDF and Other Screen Output

Because a single XML Screen file can support output in multiple render modes the render mode to use is selected using a parameter to the screen: the **renderMode** parameter. For web-based applications this can be a URL parameter. For any application this can be set in a screen action, usually a pre-action (i.e., under the *screen.pre-actions* element).

The value of this parameter can be any string matching a *screen-text-output*.**type** attribute in the Moqui Conf XML file. This includes the OOTB types as well as any you add in your runtime conf file. Default types include csv, html, text, xml, xsl-fo, plus the SPA modes vuet, js, vue, qvt, qjs, and qvue.

All screens in the render path are rendered regardless of the render mode, so for output types where you only want the content of the last screen in the path to be included (like CSV), use the **lastStandalone**=true parameter along with the **renderMode** parameter.

