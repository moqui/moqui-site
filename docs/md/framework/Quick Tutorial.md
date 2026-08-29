# Moqui Framework Quick Tutorial

This tutorial is a step-by-step guide to creating and running your own Moqui component with a user interface, logic, and database interaction.

[TOC]

## Overview

**Part 1**: To get started you'll be creating your own component and a simple "Hello world!" screen.

**Part 2**: Continuing from there you'll define your own entity (database table) and add forms to your screen to find and create records for that entity.

**Part 3**: To finish off the fun you will create some custom logic instead of using the default CrUD logic performed by the framework based on the entity definition.

The running approach used in this document is a simple one using the embedded servlet container. For more complete coverage of running and deployment options, and of the general directory structure of Moqui Framework, please read the [Run and Deploy](/docs/framework/Run+and+Deploy) document.

## Part 1

### Download Moqui Framework

If you haven't already downloaded Moqui Framework, do that now.

Run Moqui using the [Running and Deployment Instructions](/docs/framework/Run+and+Deploy).

In your browser go to `http://localhost:8080/`, log in as John Doe, and look around a bit.

Now quit (<ctrl>-c in the command line) and you're ready to go...

### Create a Component

Moqui follows the "convention over code" principle for components, so all you really have to do to create a Moqui component is create a directory:

`$ cd runtime/component`
`$ mkdir tutorial`

Now go into the directory and create some of the standard directories that you'll use later in this tutorial:

`$ cd tutorial`
`$ mkdir data`
`$ mkdir entity`
`$ mkdir screen`
`$ mkdir script`
`$ mkdir service`

### Add a Screen

Using your favorite IDE or text editor add a screen XML file in:

`runtime/component/tutorial/screen/tutorial.xml`

For now let this be a super simple screen with just a "Hello world!" label in it. The contents should look something like:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<screen xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="http://moqui.org/xsd/xml-screen-2.1.xsd"
        require-authentication="anonymous-all">
    <widgets>
        <label type="h1" text="Hello world!"/>
    </widgets>
</screen>
```

Note that the `screen.@require-authentication` attribute is set to "anonymous-all". This effectively disables the default security settings of screens where both authentication (login) and authorization to access the screen are required. The `apps.xml` screen uses the "false" setting for this attribute which is similar but does not login an 'anonymous' user or disable authorization for 'all' (not just view) actions on the screen.

For more information on Moqui Artifact Authorization see the [Security](/docs/framework/Security) document.

Another thing to notice is the `xmlns:xsi` and `xsi:noNamespaceSchemaLocation` attribute which are used to specify the XSD file to use for validation and auto-completion in your IDE. Depending on your IDE you may need to go through different steps to configure it so that it knows how to find the local XSD file for the location specified (it is a valid HTTP URL but that's not how XSD URIs work). See the documents under the [IDE Setup](/docs/framework/IDE+Setup) document.

### Mount as a Subscreen

To make your screen available it needs to be added as a subscreen to a screen that is already under the root screen somewhere. In Moqui screens the URL path to the screen and the menu structure are both driven by the subscreen hierarchy, so this will setup the URL for the screen and add a menu tab for it.

For the purposes of this tutorial we'll use the existing root screen and header/footer/etc that are in the included runtime directory. This runtime directory has a `webroot` component with the root screen at:

`runtime/base-component/webroot/screen/webroot.xml`

On a side note, the root screen is specified in the Moqui Conf XML file using the `webapp-list.webapp.root-screen` element, and you can have multiple elements to have different root screens for different host names. See the Run and Deploy guide for more information on the Moqui Conf XML file.

To make the screen hierarchy more flexible this root screen only has a basic HTML head and body, with no header and footer content, so let's put our screen under the **apps** screen which adds a header menu and will give our screen some context.

There are 4 ways to make a screen a subscreen of another screen described in the [User Interface => XML Screen](/docs/framework/User+Interface/XML+Screen) document. For this tutorial we'll use the component MoquiConf.xml file approach which is merged into the MoquiDefaultConf.xml file included in the framework when Moqui starts along with MoquiConf.xml files in other components and the runtime Moqui Conf XML file optionally specified in a startup command line argument. This is the recommended approach for adding a new 'app' to Moqui and is used in PopCommerce, HiveMind, etc.

Add a MoquiConf.xml file to the root directory of your component:

`runtime/component/tutorial/MoquiConf.xml`

While you can include anything supported in the Moqui Conf XML file to mount a subscreen we'll just use the `screen-facade.screen` element like:

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<moqui-conf xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="http://moqui.org/xsd/moqui-conf-2.1.xsd">
    <screen-facade>
        <screen location="component://webroot/screen/webroot/apps.xml">
            <subscreens-item name="tutorial" menu-title="Tutorial" menu-index="99"
                    location="component://tutorial/screen/tutorial.xml"/>
        </screen>
    </screen-facade>
</moqui-conf>
```

With your component in place just start up Moqui (with `java -jar moqui.war` or the like).

The `subscreens-item.name` attribute specifies the value for the path in the URL to the screen, so your screen is now available in your browser at:

`http://localhost:8080/apps/tutorial`

It is also available in the new Vue JS based hybrid server + client application wrapper under `/vapps` which uses the screens mounted under `/apps`:

`http://localhost:8080/vapps/tutorial`

### Try Included Content

Instead of using the label element we can get the HTML from a file that is "under" the screen.

First create a simple HTML file located in a `tutorial` directory under our component's `screen` directory:

`runtime/component/tutorial/screen/tutorial/hello.html`

The HTML file can contain any HTML, and since this will be included in a screen whose parent screens take care of header/footer/etc we can keep it very simple:

```xml
<h1>Hello world! (from hello.html file)</h1>
```

Now just explicitly include the HTML file in the `tutorial.xml` screen definition using a `render-mode.text` element just after the `label` element from the first version of this file above. The full file should now look like:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<screen xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="http://moqui.org/xsd/xml-screen-2.1.xsd"
        require-authentication="anonymous-all">
    <widgets>
        <label type="h1" text="Hello world!"/>
        <render-mode>
            <text type="html,vuet" location="component://tutorial/screen/tutorial/hello.html"/>
        </render-mode>
    </widgets>
</screen>
```

So what is this `render-mode` thingy? Moqui XML Screens are meant to platform agnostic and may be rendered in various environments. Because of this we don't want anything in the screen that is specific to a certain mode of rendering the screen without making it clear that it is. Under the `render-mode` element you can have various sub-elements for different render modes, even for different text modes such as HTML, XML, XSL-FO, CSV, and so on so that a single screen definition can be rendered in different modes and produce output as needed for each mode.

Since Moqui 2.1.0 the Vue JS based hybrid client/server rendering functionality is available. This uses the render mode 'vuet' instead of 'html' because the output is actually a Vue template and not standard HTML. The `text.@type` attribute is "html,vuet" so that the HTML from the file is included for both render modes.

The screen is available at the same URL, but now includes the content from the HTML file instead of just having it inline as a `label` in the screen definition.

### Try Sub-Screen Content

One side effect of putting the `hello.html` file under a mounted screen using the matching directory name (`tutorial` for `tutorial.xml`) is that this file is also available for direct access with a URL like:

`http://localhost:8080/apps/tutorial/hello.html`

When you go to this URL you won't see the header from the `apps.xml` screen because it is directly accessing the file. This is can be used for other static (not server rendered) text files like CSS, JavaScript, and even binary files like images. Typically it's best to use a separate parent screen for static content as the SimpleScreens and HiveMind do, but it can be mixed with screens in any screen hierarchy.

What if you don't want the raw HTML from `hello.html` to be available through an HTTP request? What if you only want it to be usable as an include in a screen? To do that just don't put it in a directory that isn't under a mounted screen. A common approach to this is to add a `template` directory to your component and put the templates and files there. For example:

`runtime/component/tutorial/template/tutorial/hello.html`

With `hello.html` in that directory the location you specify to include it in the screen also changes, like:

```xml
        <render-mode>
            <text type="html,vuet" location="component://tutorial/template/tutorial/hello.html"/>
        </render-mode>
```

## Part 2

### My First Entity

An entity is a basic tabular data structure, and usually just a table in a database. An entity value is equivalent to a row in the database. Moqui does not do object-relational mapping, so all we have to do is define an entity, and then start writing code using the Entity Facade (or other higher level tools) to use it.

To create a simple entity called "Tutorial" with fields "tutorialId" and "description" create an entity XML file at:

`runtime/component/tutorial/entity/TutorialEntities.xml`

Add an entity definition to that file like:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<entities xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="http://moqui.org/xsd/entity-definition-2.1.xsd">
    <entity entity-name="Tutorial" package="tutorial">
        <field name="tutorialId" type="id" is-pk="true"/>
        <field name="description" type="text-medium"/>
    </entity>
</entities>
```

If you're running Moqui in dev mode the entity definition cache clears automatically so you don't have to restart, and for production mode or if you don't want to wait (since Moqui does start very fast) you can just stop and start the JVM.

How do you create the table in the database? When running with the embedded H2 database Moqui can create tables on the fly and will do so the first time to use the new entity. This used to also work with MySQL but due to transactional handling of create table it no longer does. Creating a table and other DB meta data operations are usually not allowed in the middle of an active transaction so it must be done in advance and for most databases Moqui Framework does adds missing tables, columns, foreign keys, and indexes only on startup (which can also be turned off by configuration or env var).

### Add Some Data

The Entity Facade has functionality to load data from, and write data to, XML files that basically elements that match entity names and attributes that map field names.

We'll create a UI to enter data later on, and you can use the Auto Screens or Entity Data Import screen in the Tools application to work with records in your new entity. Data files are useful for seed data that code depends on, data for testing, and data to demonstrate how a data model should be used. So, let's try it.

Create an Entity Facade XML data file at:

`runtime/component/tutorial/data/TutorialDemoData.xml`

In the file add an `entity-facade-xml` element with sub-elements for the full entity name which is the **package** and the **entity-name** together (`tutorial.Tutorial`):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<entity-facade-xml type="demo">
    <tutorial.Tutorial tutorialId="TestOne" description="Test one description."/>
    <tutorial.Tutorial tutorialId="TestTwo" description="Test two description."/>
</entity-facade-xml>
```

Note that the `type` attribute is set to "demo". This is used when running a general data load (`java -jar moqui.war load`) where limited data file types may be specified to load. You can use any simple text for the data file type but there are a few standard types used in the framework such as seed, seed-initial, install, demo, and test.

The standard set of types to load on production instances is **seed**, **seed-initial**, and **install**. The **demo** type is used for demo data used during development and testing. The **test** type is for file that overwrite production settings stored in the database so that clones of a production database are safer to use for end user experimenting or developer testing and gets loaded automatically when Moqui starts if the **instance_purpose** is set to "test".

For more information on data loading see the [Data and Resources => Entity Data Import and Export](/docs/framework/Data+and+Resources/Entity+Data+Import+and+Export) document.

The easiest way to load this is from the **Data Import** screen in the Tools app:

`http://localhost:8080/vapps/tools/Entity/DataImport`

Click on the **XML Text** section of the form, paste in the XML above, then click on the **Import Data - Create Only** button. You can also click on the **Import Data - Create or Update** button but because we know these records aren't already there we can use the Create Only variation which is intended for loading data on production servers where you don't want to replace existing records that may have been modified.

To load this from the command line, with Moqui not already running, just run `$ ./gradlew load` or one of the other load variations described in the [Run and Deploy](/docs/framework/Run+and+Deploy) document.

### Make a Real Application

We're about to add a sub-screen under our `tutorial.xml` screen but so far it doesn't do anything with sub-screens. We need to tell the framework where in the `widgets` to include the active sub-screen and we do that by adding a `subscreens-active` element.

For good measure it is best to always have a default sub-screen for each screen that supports sub-screens so that any partial URL still goes somewhere useful. That is done using the `subscreens.@default-item` attribute which we'll set to "FindTutorial" to match the name of the screen we're about to add.

While we're at it let's make our new application secure and add authorization configuration so it is accessible. To make it secure just remove the `screen.@require-authentication` attribute.

With those changes our `tutorial.xml` screen should now look like:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<screen xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="http://moqui.org/xsd/xml-screen-2.1.xsd">
    <subscreens default-item="FindTutorial"/>
    <widgets>
        <label type="h1" text="Hello world!"/>
        <render-mode>
            <text type="html,vuet" location="component://tutorial/screen/tutorial/hello.html"/>
        </render-mode>
        <subscreens-active/>
    </widgets>
</screen>
```

With the `subscreens-active` element below the `label` and `render-mode` elements from our previous screen the `tutorial.xml` screen is now a wrapper around all sub-screens so the "Hello world!" text gets displayed above the sub-screen widgets.

To configure authorization we'll need some data in the database, and we'll put it in a file for future reference even though for now it is easiest to just load through the Data Import screen in the Tools app as we did above. Create a new data XML file at:

`runtime/component/tutorial/data/TutorialSetupData.xml`

In the file we'll need 3 records:

- **ArtifactGroup** to define a group of artifacts (framework artifacts include screens, services, entities, etc)
- **ArtifactGroupMember** to specify which artifacts are in the group, in this case the `tutorial.xml` screen and with `inheritAuthz` set to "Y" also all sub-screens under that screen
- **ArtifactAuthz** is where the rubber hits the road and we define the authorization the User Group will have for the specified Artifact Group

Note that we're using the **ALL_USERS** group in this example. This group is a special one in the framework that all users are automatically a member of. That makes it different from any other group, like the OOTB **ADMIN** group which only includes members for records in the `UserGroupMember` entity.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<entity-facade-xml type="seed-initial">
    <moqui.security.ArtifactGroup artifactGroupId="TUT_APP"
            description="Tutorial App (via root screen)"/>
    <moqui.security.ArtifactGroupMember artifactGroupId="TUT_APP" 
            artifactName="component://tutorial/screen/tutorial.xml"
            artifactTypeEnumId="AT_XML_SCREEN" inheritAuthz="Y"/>
    <moqui.security.ArtifactAuthz artifactAuthzId="TUT_ALL" 
            userGroupId="ALL_USERS" artifactGroupId="TUT_APP"
            authzTypeEnumId="AUTHZT_ALWAYS" authzActionEnumId="AUTHZA_ALL"/>
</entity-facade-xml>
```

Load this data now thought the Data Import screen in the Tools app so that it is in place when we try our new find screen below.

### Find Screen with Automatic Find Form

Now we have a more complete shell for our new application and we're ready to add a find screen.

Add the XML screen definition below as a sub-screen of the `tutorial.xml` screen by putting it in a file at:

`runtime/component/tutorial/screen/tutorial/FindTutorial.xml`

This uses the Directory Structure approach for adding sub-screens described in the [User Interface => XML Screen](/docs/framework/User+Interface/XML+Screen) document.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<screen xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="http://moqui.org/xsd/xml-screen-2.1.xsd">
    <actions>
        <entity-find entity-name="tutorial.Tutorial" list="tutorialList">
            <search-form-inputs/></entity-find>
    </actions>
    <widgets>
        <form-list name="ListTutorials" list="tutorialList" header-dialog="true" skip-form="true">
            <auto-fields-entity entity-name="tutorial.Tutorial" field-type="find-display"/>
        </form-list>
    </widgets>
</screen>
```

This screen has a couple of key parts:

- **`actions.entity-find`** There is just one action run when this screen is rendered: an `entity-find`.
  - Normally with an `entity-find` element (or in the Java API an EntityFind object) you would specify conditions, fields to order by, and other details about the find to run.
  - In this case we are doing a find on an entity using standard parameters from an XML Form, so we can use the `search-form-inputs` sub-element to handle these automatically.
  - Note that an `entity-find` element can go directly under a `form-list` element but it behaves differently there, instead of the default of selecting all fields it only selects entity fields that have a corresponding field in the form-list and that field is either a hidden type or is shown when the form is rendered based on form or user settings with the `select-columns` option.
  - To get an idea of what the parameters should be like just view the HTML source in your browser that is generated by the XML Form.
- **`widgets.form-list`** This is the actual form definition, specifically for a "list" form for multiple records/rows (as opposed to a "single" form).
  - The `form-list.@name` here can be anything as long as it is unique within the XML Screen.
  - The `form-list.@list` attribute refers to the result of the `entity-find` in the `actions` block.
  - With `form-list.@header-dialog` set to "true" it will add a **Find Options** button that opens a dialog instead of putting the find fields inline in the table header.
  - The `form-list.@skip-form` attribute is set to "true" because we don't need an HTML form, the form-list is used for display only and this will trim down the HTML generated.
  - Since the goal was to have a form automatically defined based on an entity we use the `auto-fields-entity` element with the name of our Tutorial entity, and **find-display** option for the `auto-fields-entity.@field-type` attribute which creates find fields in the header and display fields for each record in the table body.

To view this screen use this URL:

`http://localhost:8080/vapps/tutorial/FindTutorial`

### An Explicit Field

Instead of the default for the description field, what if you wanted to specify how it should look at what type of field it should be?

To do this just add a `field` element inside the `form-list` element, and just after the `auto-fields-entity` element, like this:

```xml
<form-list name="ListTutorials" list="tutorialList" header-dialog="true" skip-form="true">
    <auto-fields-entity entity-name="tutorial.Tutorial" field-type="find-display"/>
    <field name="description">
        <header-field show-order-by="true"><text-find hide-options="true"/></header-field>
        <default-field><display/></default-field>
    </field>
</form-list>
```

Because the field `name` attribute is the same as a field already created by the `auto-fields-entity` element it will override that field. If the `name` was different an additional field would be created. The result of this is basically the same as what was automatically generated using the `auto-fields-entity` element except that the options are hidden for the text-find field (inspect it in your browser to see that other find parameters are still there with default options, ie this is different from a plain text-line).

### Add a Create Form

Let's add a button that will pop up a Create Tutorial form, and a transition to process the input.

Think of links between screens as an ordered graph where each screen is a node and the **transitions** defined in each screen are how you go from that screen to another (or back to the same), and as part of that transition optionally run server-side actions or a service. A single `transition` can have multiple responses with conditions and for errors resulting in transition to various screens as needed by your UI design.

First add a transition to the `FindTutorial.xml` screen you created before, just above the `actions` element:

```xml
<transition name="createTutorial">
    <service-call name="create#tutorial.Tutorial"/>
    <default-response url="."/>
</transition>
```

This transition calls the `create#tutorial.Tutorial` service, and then goes back to the current screen.

Where did the `create#tutorial.Tutorial` service come from? We haven't defined anything like that yet. The Moqui Service Facade supports a special kind of service for entity CrUD operations that don't need to be defined, let alone implemented. This service name consists of two parts, a verb and a noun, separated by a hash (#). As long as the verb is create, update, store, or delete and the noun is a valid entity name the Service Facade will treat it as an implicit entity-auto service and do the desired operation. It does so based on the entity definition and the parameters passed to the service call. For example, with the create verb and an entity with a single primary key field if you pass in a value for that field it will use it, otherwise it will automatically sequence a value using the entity name as the sequence key.

Next let's add the create form, in a hidden container that will expand when a button is clicked. Put this inside the `widget` element, just above the `form-list` element in the original `FindTutorial.xml` screen you created before so that it appears above the list form in the screen:

```xml
<container-dialog id="CreateTutorialDialog" button-text="Create Tutorial">
    <form-single name="CreateTutorial" transition="createTutorial">
        <auto-fields-entity entity-name="tutorial.Tutorial" field-type="edit"/>
        <field name="submitButton"><default-field title="Create"><submit/></default-field></field>
    </form-single>
</container-dialog>
```

The form definition refers to the `transition` you just added to the screen, and uses the `auto-fields-entity` element with **edit** for the `field-type` to generate edit fields. The last little detail is to declare a button to submit the form, and it's ready to go.

Try it out and see the records appear in the list form that was part of the original screen.

## Part 3

### Custom Create Service

The `createTutorial` transition from our screen above used the implicit entity-auto service `create#tutorial.Tutorial`. Let's see what it would look like to define and implement a service manually.

First lets define a service and use the automatic entity CrUD implementation:

`runtime/component/tutorial/service/tutorial/TutorialServices.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<services xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="http://moqui.org/xsd/service-definition-2.1.xsd">
    <service verb="create" noun="Tutorial" type="entity-auto">
        <in-parameters>
            <auto-parameters include="all"/>
        </in-parameters>
        <out-parameters>
            <auto-parameters include="pk" required="true"/>
        </out-parameters>
    </service>
</services>
```

This will allow all fields of the Tutorial entity to be passed in, including an optional `tutorialId` which is the primary key field and a sequenced ID will be generated no value is specified. It will always return the PK field (tutorialId). Note that with the `auto-parameters` element we are defining the service based on the entity, and if we added fields to the entity they would be automatically represented in the service.

One quirk with `service.@type` set to "entity-auto" is that it uses the `service.@noun` for the entity name. It works like this without the entity package included in the name because the framework allows using entity names without a package, though you may be inconsistent results if there are multiple entities with the same name in different packages.

Now change that service definition to add an inline implementation as well. Notice that the `service.@type` attribute has changed, and the `actions` element has been added.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<services xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="http://moqui.org/xsd/service-definition-2.1.xsd">
    <service verb="create" noun="Tutorial" type="inline">
        <in-parameters>
            <auto-parameters include="all"/>
        </in-parameters>
        <out-parameters>
            <auto-parameters include="pk" required="true"/>
        </out-parameters>
        <actions>
            <entity-make-value entity-name="tutorial.Tutorial" value-field="tutorial"/>
            <entity-set value-field="tutorial" include="all"/>
            <if condition="!tutorial.tutorialId">
                <entity-sequenced-id-primary value-field="tutorial"/>
            </if>
            <entity-create value-field="tutorial"/>
        </actions>
    </service>
</services>
```

Now to call the service instead of the implicit entity-auto one just change the `transition` to refer to this service:

```xml
<transition name="createTutorial">
    <service-call name="tutorial.TutorialServices.create#Tutorial"/>
    <default-response url="."/>
</transition>
```

Note that the service name for a defined service like this is like a fully qualified Java class name. It has a "package", in this case "tutorial", which is the directory (and may be a path with multiple directories separated by dots) under the `component/service` directory. Then there is a dot and the equivalent of the class name, in this case "TutorialServices" which is the name of the XML file the service is in, but without the .xml extension. After that is another dot, and then the service name with the verb and noun optionally separated by a hash (#).

### Groovy Service

What if you want to implement the service in Groovy (or some other supported scripting language) instead of the inline XML Actions? Try adding another service definition like this to the TutorialServices.xml file (to test change the service name in FindTutorial.xml):

```xml
    <service verb="create" noun="TutorialGroovy" type="script"
            location="component://tutorial/service/tutorial/createTutorial.groovy">
        <in-parameters>
            <auto-parameters entity-name="tutorial.Tutorial" include="all"/>
        </in-parameters>
        <out-parameters>
            <auto-parameters entity-name="tutorial.Tutorial" include="pk" required="true"/>
        </out-parameters>
    </service>
```

Notice that the `service.@type` attribute has changed to **script**, and there is now a `service.@location` attribute which specifies the location of the script.

Because we've change the `service.@noun` attribute to "TutorialGroovy" which is not a valid entity name we must specify the `entity-name` on the two `auto-parameters` elements. In other words by default it you don't specify `auto-parameters.@entity-name` the framework will try the `service.@noun` and in this case that will result in an error.

The script can be located anywhere in the component as we refer to it's location explicitly. For convenience we're adding it to the existing `service/tutorial` directory. Here is what the script would look like in that location:

```groovy
def tutorial = ec.entity.makeValue("tutorial.Tutorial")
tutorial.setFields(context, true, null, null)
if (!tutorial.tutorialId) tutorial.setSequencedIdPrimary()
tutorial.create()
```

When in Groovy, or other languages, you'll be using the Moqui Java API which is based on the ExecutionContext class which is available in the script with the variable name "ec". For more details on the API see the [API JavaDocs](/javadoc/index.html) and specifically the doc for the [ExecutionContext](/javadoc/org/moqui/context/ExecutionContext.html) class which has links to the other major API interface pages.

## What's Next?

Now that you have soiled your hands with the details of Moqui Framework you're ready to explore the other documentation here in the Moqui Framework wiki space on moqui.org. Most of the content from the "Making Apps with Moqui" book has been migrated here and updated for changes and new functionality in the framework.

There is also documentation for [Mantle Business Artifacts](/docs/mantle), including the UDM data model, available here on moqui.org.

If you will be doing any ERP related development the [documentation for the POPC ERP app](/docs/apps/POPC+ERP+User+Guide) is highly recommended for both reading and reference to better understand business concepts and how end users go about doing various business activities in the app. This is also useful to find services to use by looking at how things are meant to be done in the ERP app and then looking at the transitions in the screens to see which services are used.

You may also enjoy reading through the [Framework Features](/docs/framework/Framework+Features) document.
