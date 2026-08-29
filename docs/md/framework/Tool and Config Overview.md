# Framework Tool and Configuration Overview

[TOC levels=2-4]

What follows is a summary of the various tools in the Moqui Framework and corresponding configuration elements in the Moqui Conf XML file. The default settings are in the MoquiDefaultConf.xml file, which is included in the executable WAR file in a binary distribution of Moqui Framework. This is a great file to look at to see some of the settings that are available and what they are set to by default. If you downloaded a binary distribution of Moqui Framework you can view this file online at (note that this is from the master branch on GitHub and may differ slightly from the one you downloaded):

[**https://github.com/moqui/moqui-framework/blob/master/framework/src/main/resources/MoquiDefaultConf.xml**](https://github.com/moqui/moqui-framework/blob/master/framework/src/main/resources/MoquiDefaultConf.xml)

Any setting in this file can be overridden in the Moqui Conf XML file that is specified at runtime along with the runtime directory (and generally in the conf directory under the runtime directory). The two files are merged before any settings are used, with the runtime file overriding the default one. Because of this, one easy way to change settings is simply copy from the default conf file and paste into the runtime one, and then make changes as desired.

## Execution Context and Web Facade

The Execution Context is the central object in the Moqui Framework API. This object maintains state within the context of a single server interaction such as a web screen request or remote service call. Through the ExecutionContext object you have access to a number of "facades" that are used to access the functionality of different parts of the framework. There is detail below about each of these facades.

The main state tracked by the Execution Context is the variable space, or "context", used for screens, actions, services, scripts, and even entity and other operations. This context is a hash or map with name/value entries. It is implemented with the ContextStack class and supports protected variable spaces with **push**() and **pop**() methods that turn it into a stack of maps. As different artifacts are executed they automatically **push**() the context before writing to it, and then **pop**() the context to restore its state before finishing. Writing to the context always puts the values into the top of the stack, but when reading the named value is searched for at each level on the stack starting at the top so that fields in deeper levels are visible.

In some cases, such as calling a service, we want a fresh context to better isolate the artifact from whatever called it. For this we use the **pushContext**() method to get a fresh context, then the **popContext**() method after the artifact is run to restore the original context.

The context is the literal variable space for the executing artifact wherever possible. In screens when XML actions are executed the results go in the local context. Even Groovy scripts embedded in service and screen actions share a variable space and so variables declared exist in the context for subsequent artifacts.

Some common expressions you’ll see in Moqui-based code (using Groovy syntax) include:

-   refer to the current variable context: ec.context
-   refer to the "exampleId" field from the context: ec.context.exampleId
-   set the exampleId to "foo": ec.context.exampleId = "foo"
-   for inline scripts you can also just do: exampleId = "foo"

For an ExecutionContext instance created as part of a web request (HttpServletRequest) there will be a special facade called the Web Facade. This facade is used to access information about the servlet environment for the context including request, response, session, and application (ServletContext). It is also used to access the state (attributes) of these various parts of the servlet environment including request parameters, request attributes, session attributes, and application attributes.

### Web Parameters Map

The request parameters "map" (ec.web.requestParameters) is a special map that contains parameters from the URL parameter string, inline URL parameters (using the "/~name=value/" format), and multi-part form submission parameters (when applicable). There is also a special parameters map (ec.web.parameters) that combines all the other maps in the following order (with later overriding earlier): request parameters, application attributes, session attributes, and request attributes. That parameters map is a stack of maps just like the context so if you write to it the values will go in the top of the stack which is the request attributes.

For security reasons the request parameters map is canonicalized and filtered. This and the Service Facade validation help to protect against XSS and injection attacks.

### Factory, Servlet & Listeners

Execution Context instances are created by the Execution Context Factory. This can be done directly by your code when needed, but is usually done by a container that Moqui Framework is running in.

The most common way to run Moqui Framework is as a webapp through either a WAR file deployed in a servlet container or app server, or by running the executable WAR file and using the embedded Jetty Servlet Container (Jakarta Servlet). In either case the Moqui root webapp is loaded and the WEB-INF/web.xml file tells the servlet container to load the MoquiServlet, the MoquiSessionListener, and the MoquiContextListener. These are default classes included in the framework, and you can certainly create your own if you want to change the lifecycle of the ExecutionContextFactory and ExecutionContext.

With these default classes the ExecutionContextFactory is created by the MoquiContextListener on the **contextInitialized**() event, and is destroyed by the same class on the **contextDestroyed**() event. The ExecutionContext is created using the factory by the MoquiServlet for each request in the **doGet**() and **doPost**() methods, and is destroyed by the MoquiServlet at the end of each request by the same method.

## Resource and Cache Facades

The Resource Facade is used to access and execute resources such as scripts, templates, and content. The Cache Facade is used to do general operations on caches, and to get a reference to a cache as an implementation of the Cache interface (`javax.cache.Cache`, JSR-107). Along with supporting basic get/put/remove/etc operations you can get statistics for each cache, and modify cache properties such as timeouts, size limit, and eviction algorithm. The default implementation is **MCache** (`org.moqui.jcache.MCache`), configured with `cache-list.@local-factory="MCache"` in the Moqui Conf XML file. There is no ehcache.xml file.

The Resource Facade uses the Cache Facade to cache plain text by its source location (for **getLocationText**() method), compiled Groovy and XML Actions scripts by their locations (for the runScriptInCurrentContext method), and compiled FreeMarker (FTL) templates also by location (for the **renderTemplateInCurrentContext**() method).

There is also a cache used for the small Groovy expressions that are scattered throughout XML Screen and Form definitions, and that cache is keyed by the actual text of the expression instead of by a location that it came from (for the **evaluateCondition**(), **evaluateContextField**(), and **evaluateStringExpand**() methods).

For more generic access to resources the **getLocationReference**() method returns an implementation of the ResourceReference interface. This can be used to read resource contents (for files and directories), and get information about them such as content/MIME type, last modified time, and whether it exists. These resource references are used by the rest of the framework to access resources in a generic and extensible way. Implementations of the ResourceReference interface can be implemented as needed and default implementations exist for the following protocols/schemes: http, https, file, ftp, jar, classpath, component, and content (JCR, i.e., Apache Jackrabbit).

## Screen Facade

The API of the Screen Facade is deceptively simple, mostly just acting as a factory for the ScreenRender interface implementation. Through the ScreenRender interface you can render screens in a variety of contexts, the most common being in a service with no dependence on a servlet container, or in response to a HttpServletRequest using the ScreenRender.**render**(request, response) convenience method.

Generally when rendering a screen you will specify the root screen location, and optionally a subscreen path to specify which subscreens should be rendered (if the root screen has subscreens, and instead of the default-item for each screen with subscreens). For web requests this sub-screen path is simply the request "pathInfo" (the remainder of the URL path after the location where the webapp/servlet are mounted).

### Screen Definition

The real magic of the Screen Facade is in the screen definition XML files. Each screen definition can specify web-settings, parameters, transitions with responses, subscreens, pre-render actions, render-time actions, and widgets. Widgets include subscreens menu/active/panel, sections, container, container-panel, render-mode-specific content (html, vuet, qvt, xml, csv, text, xsl-fo, etc), and forms.

There are two types of forms: form-single and form-list. They both have a variety of layout options and support a wide variety of field types. While Screen Forms are primarily defined in Screen XML files, they can also be extended for groups of users with the DbForm and related entities.

One important note about forms based on a service (using the auto-fields-service element) is that various client-side validations will be added automatically based on the validations defined for the service the form field corresponds to.

### Screen/Form Render Templates

The output of the ScreenRender is created by running a template with macros for the various XML elements in screen and form definitions. If a template is specified through the ScreenRender.**macroTemplate**() method then it will be used, otherwise a template will be determined with the **renderMode** and the configuration in the screen-facade.screen-text-output element of the Moqui Conf XML file. You can create your own templates that override the default macros, or simply ignore them altogether, and configure them in the Moqui Conf XML file to get any output you want. There is an example of one such template in the `runtime/template/screen-macro/ScreenHtmlMacros.ftl` file, with the override configuration in the `runtime/conf/MoquiDevConf.xml` file.

The default HTML screen and form template (`DefaultScreenMacros.html.ftl`, used for `/apps`) uses jQuery Core and UI for dynamic client-side interactions. Other JS libraries could be used by modifying the screen HTML macros as described above, and by changing the theme data (defaults in `runtime/base-component/webroot/data/WebrootThemeData.xml`) to point to the desired JavaScript and CSS files. The default application UI is Quasar under `/qapps` using `DefaultScreenMacros.qvt.ftl`.

## Service Facade

The Service Facade is used to call services through a number of service call interfaces for synchronous, asynchronous, scheduled and special (TX commit/rollback) service calls. Each interface has different methods to build up information about the call you want to do, and they have methods for the name and parameters of the service.

When a service is called the caller doesn’t need to know how it is implemented or where it is located. The service definition abstracts that out to the service definition so that those details are part of the implementation of the service, and not the calling of the service.

### Service Naming

Service names are composed of 3 parts: path, verb, and noun. When referring to a service these are combined as: "**${path}.${verb}#${noun}**", where the hash/pound sign is optional but can be used to make sure the verb and noun match exactly. The path should be a Java package-style path such as org.moqui.impl.UserServices for the file at classpath://service/org/moqui/impl/UserServices.xml. While it is somewhat inconvenient to specify a path this makes it easier to organize services, find definitions based on a call to the service, and improve performance and caching since the framework can lazy-load service definitions as they are needed.

That service definition file will be found based on that path with location patterns: "classpath://service/$1" and "component://.\*/service/$1" where $1 is the path with ‘.’ changed to ‘/’ and ".xml" appended to the end.

The verb (required) and noun (optional) parts of a service name are separate to better to describe what a service does and what it is acting on. When the service operates on a specific entity the noun should be the name of that entity.

The Service Facade supports CrUD operations based solely on entity definitions. To use these entity-implicit services use a service name with no path, a noun of create, update, or delete, a hash/pound sign, and the name of the entity. For example to update a UserAccount use the service name **update#UserAccount**. When defining entity-auto services the noun must also be the name of the entity, and the Service Facade will use the in- and out-parameters along with the entity definition to determine what to do (most helpful for create operations with primary/secondary sequenced IDs, etc).

The full service name combined from the examples in the paragraphs above would look like this:

org.moqui.impl.UserServices.**update#UserAccount**

### Parameter Cleaning, Conversion and Validation

When calling a service you can pass in any parameters you want, and the service caller will clean up the parameters based on the service definition (remove unknown parameters, convert types, etc) and validate parameters based on validation rules in the service definition before putting those parameters in the context for the service to run. When a service runs the parameters will be in the ec.context map along with other inherited context values, and will be in a map in the context called parameters to access the parameters segregated from the rest of the context.

One important validation is configured with the parameter.**allow-html** attribute in the service definition. By default no HTML is allowed, and you can use that attribute to allow any HTML or just safe HTML for the service parameter. Safe HTML is determined using the OWASP ESAPI and Antisamy libraries, and configuration for what is considered safe is done in the antisamy-esapi.xml file.

### Job Scheduler

The Service Facade has a job scheduler configured using the `ServiceJob` entity. It uses standard `java.util.concurrent` classes including **ThreadPoolExecutor** and **ScheduledThreadPoolExecutor** for asynchronous and scheduled service calls from a single worker pool managed by the framework. There are screens in the System app for scheduling jobs, reviewing job history and results, and other job related administration.

### Web Services

#### JSON-RPC

For RPC web services the Service Facade uses custom code with Moqui JSON and web request tools for incoming and outgoing JSON-RPC 2.0 calls. Outgoing JSON-RPC calls are handled by RemoteJsonRpcServiceRunner, configured in the `service-facade.service-type` element in the Moqui Conf XML file. Remote REST calls use RemoteRestServiceRunner. To add support for other outgoing service calls through the Service Facade implement the ServiceRunner interface and add a `service-facade.service-type` element for it.

Incoming JSON-RPC is handled using a default transition defined in `runtime/base-component/webroot/screen/webroot/rpc.xml`. The remote URL, if webroot.xml is mounted on the root ("/") of the server, is `http://hostname/rpc/json`. To handle other types of incoming services similar screen transitions can be added to the rpc.xml screen, or to any other screen.

#### REST API

The main tool for building a REST API based on internal services and entity operations is to define resource paths in a *Service REST API* XML file such as the `moqui.rest.xml` file in **moqui-framework** and the `mantle.rest.xml` file in **mantle-usl**. With your own Service REST API XML files you can define sets of web services to match the structure of the applications you are building, and grant authorization to different paths for different sets of users just like with XML Screens. In the Tools app you can view Service REST API details using automatic Swagger output produced by the framework based on the REST XML file and the entities and services used within it.

Another alternative for REST style services: a screen transition can be declared with an HTTP request method (get, put, etc) as well as a name to match against the incoming URL. For more flexible support of parameters in the URL beyond the transition’s place in the URL path values following the transition can be configured to be treated the same as named parameters. To make things easier for JSON payloads they are also automatically mapped to parameters and can be treated just like parameters from any other source, allowing for easily reusable server-side code. To handle these REST service transitions an internal service can be called with very little configuration, providing for an efficient mapping between exposed REST services and internal services.

## Entity Facade

The Entity Facade is used for common database interactions including create/update/delete and find operations, and for more specialized operations such as loading and creating entity XML data files. While these operations are versatile and cover most of the database interactions needed in typical applications, sometimes you need lower-level access, and you can get a JDBC Connection object from the Entity Facade that is based on the entity-facade datasource configuration in the Moqui Conf XML file.

Entities correspond to tables in a database and are defined primarily in XML files. These definitions include list the fields on the entity, relationships betweens entities, special indexes, and so on. Entities can be extended using database record with the UserField and related entities.

Each individual record is represented by an instance of the EntityValue interface. This interface extends the Map interface for convenience, and has additional methods for getting special sets of values such as the primary key values. It also has methods for database interactions for that specific record including create, update, delete, and refresh, and for getting setting primary/secondary sequenced IDs, and for finding related records based on relationships in the entity definition. To create a new EntityValue object use the EntityFacade.**makeValue**() method, though most often you’ll get EntityValue instances through a find operation.

To find entity records use the EntityFind interface. To get an instance of this interface use the EntityFacade.**makeFind**() method. This find interface allows you to set various conditions for the find (both where and having, more convenience methods for where), specify fields to select and order by, set offset and limit values, and flags including use cache, for update, and distinct. Once options are set you can call methods to do the actual find including: **one**(), **list**(), **iterator**(), **count**(), **updateAll**(), and **deleteAll**().

### Connection Pool and Database

The Entity Facade uses the [Bitronix](https://github.com/moqui/bitronix) transaction manager fork for XA-aware database connection pooling. To configure Bitronix use the `bitronix-default-config.properties` file. With configuration in the entity-facade element of the Moqui Conf XML file you can change this to use any DataSource or XADataSource in JNDI instead. The community Atomikos transaction manager is deprecated and is not a bundled option.

The default database included with Moqui Framework is **H2**. This is easy to change with configuration in the entity-facade element of the Moqui Conf XML file or with `entity_ds_*` environment variables. To add a database not yet supported in the MoquiDefaultConf.xml file, add a new `database-list.database` element. Databases supported by default include H2, Apache Derby, DB2, HSQL, MySQL (including `mysql8`), Postgres, Oracle, and MS SQL Server.

### Database Meta-Data

The first time (in each run of Moqui) the Entity Facade does a database operation on an entity it will check to see if the table for that entity exists (unless configured not to). You can also configure it to check the tables for all entities on startup. If a table does not exist it will create the table, indexes, and foreign keys (for related tables that already exist) based on the entity definition. If a table for the entity does exist it will check the columns and add any that are missing, and can do the same for indexes and foreign keys.

## Transaction Facade

Transactions are used mostly for services and screens. Service definitions have transaction settings, based on those the service callers will pause/resume and begin/commit/rollback transactions as needed. For screens a transaction is always begun for transitions (if one is not already in place), and for rendering actual screens a transaction is only begun if the screen is setup to do so (mostly for performance reasons).

You can also use the TransactionFacade for manual transaction demarcation. The JavaDoc comments have some code examples with recommended patterns for begin/commit/rollback and for pause/begin/ commit/rollback/resume to use try/catch/finally clauses to make sure the transaction is managed properly.

When debugging transaction problems, such as tracking down where a rollback-only was set, the TransactionFacade can also be use as it keeps a stack trace when **setRollbackOnly**() is called. It will automatically log this on later errors, and you can manually get those values at other times too.

### Transaction Manager (JTA)

By default the Transaction Facade uses the Bitronix TM library (also used for a connection pool by the Entity Facade), class `org.moqui.impl.context.TransactionInternalBitronix`. To configure Bitronix use the `bitronix-default-config.properties` file.

Any JTA transaction manager, such as one from an application server, can be used instead through JNDI by configuring the locations of the UserTransaction and TransactionManager implementations in the `transaction-facade.transaction-jndi` element of the Moqui Conf XML file.

## Artifact Execution Facade

The Artifact Execution Facade is called by other facades to keep track of which artifacts are "run" in the life of the ExecutionContext. It keeps both a history of all artifacts, and a stack of the current artifacts being run. For example if a screen calls a subscreen and that calls a service which does a find on an entity the stack will have (bottom to top) the first screen, then the second screen, then the service and then the entity.

### Artifact Authorization

While useful for debugging and satisfying curiosity, the main purpose for keeping track of the stack of artifacts is for authorization and permissions. There are implicit permissions for screens, transitions, services and entities in Moqui Framework. Others may be added later, but these are the most important and the one supported for version 1.0 (see the "ArtifactType" Enumeration records in the SecurityTypeData.xml file for details).

The ArtifactAuthz\* and ArtifactGroup\* entities are used to configure authorization for users (or groups of users) to access specific artifacts. To simplify configuration authorization can be "inheritable" meaning that not only is the specific artifact authorized but also everything that it uses.

There are various examples of setting up different authorization patterns in the ExampleSecurityData.xml file. One common authorization pattern is to allow access to a screen and all of its subscreens where the screen is a higher-level screen such as the ExampleApp.xml screen that is the root screen for the example app. Another common pattern is that only a certain screen within an application is authorized but the rest of it is not. If a subscreen is authorized, even if its parent screen is not, the user will be able to use that subscreen.

### Artifact Hit Tracking

There is also functionality to track performance data for artifact "hits". This is done by the Execution Context Factory instead of the Artifact Execution Facade because the Artifact Execution Facade is created for each Execution Context, and the artifact hit performance data needs to be tracked across a large number of artifact hits both concurrent and over a period of time. The data for artifact hits is persisted in the ArtifactHit and ArtifactHitBin entities. The ArtifactHit records are associated with the Visit record (one visit for each web session) so you can see a history of hits within a visit for auditing, user experience review, and various other purposes.

## User, L10n, Message, and Logger Facades

The User Facade is used to manage information about the current user and visit, and for login, authentication, and logout. User information includes locale, time zone, and currency. There is also the option to set an effective date/time for the user that the system will treat as the current date/time (through ec.user.nowTimestamp) instead of using the current system date/time.

The L10n (Localization) Facade uses the locale from the User Facade and localizes the message it receives using cached data from the LocalizedMessage entity. The EntityFacade also does localization of entity fields using the LocalizedEntityField entity. The L10n Facade also has methods for formatting currency amounts, and for parsing and formatting for Number, Timestamp, Date, Time, and Calendar objects using the Locale and TimeZone from the User Facade as needed.

The Message Facade is used to track messages and error messages for the user. The error message list (ec.message.errors) is also used to determine if there was an error in a service call or other action.

The Logger Facade is used to log information to the system log. This is meant for use in scripts and other generic logging. For more accurate and trackable logging code should use the SLF4J Logger class (org.slf4j.Logger) directly. The JavaDoc comments in the LoggerFacade interface include example code for doing this.

## Extensions and Add-ons

### The Compelling Component

A Moqui Framework component is a set of artifacts that make up an application built on Moqui, or reusable artifacts meant to be used by other components such as the mantle-udm and mantle-usl components, a theme component, or a component that integrates some other tool or library with Moqui Framework to extend the potential range of applications based on Moqui.

### Component Directory Structure

The structure of a component is driven by convention as opposed to configuration. This means that you must use these particular directory names, and that all Moqui components you look at will be structured in the same way.

-   **classes** - files under this directory will be added to the Java classpath
-   **data** - Entity XML data files with root element entity-facade-xml, loaded by **type** attribute matching types specified on the command line (`java -jar moqui.war load types=...`), or all types if no type specified
-   **entity** - All Entity Definition and Entity ECA XML files in this directory will be loaded; Entity ECA files must be in this directory and have the dual extension ".eecas.xml"
-   **lib** - JAR files in this directory will be added to the Java classpath
-   **screen** - Screens are referenced explicitly (usually by "component://\*" URL), so this is a convention
-   **script** - Scripts are referenced explicitly (usually by "component://\*" URL), so this is a convention; Groovy, XML Action, and any other scripts should go under this directory
-   **service** - Services are loaded by path to the Service Definition XML file they are defined in, and those paths are found either under these component service directories or under "classpath://service/"; Service ECA files must be in this directory and have the dual extension ".secas.xml"; Email ECA files must be in this directory and have the extension ".emecas.xml"
-   **build.gradle** - if this optional file exists the moqui root gradle module will add it to the gradle modules for build tasks (see moqui-framework/settings.gradle); see examples in core moqui add on components such as in the *moqui/moqui-fop* component for framework build dependencies and the *copyDependencies* task to put jar files in the **lib** directory
-   **component.xml** - optional XML file describing the component including name, version, and component dependencies; used by Moqui on startup to validate dependencies, and by the build.gradle for determining dependencies to add when getting components configured in addons.xml and myaddons.xml
-   **MoquiConf.xml** - optional XML file that is merged into the Moqui Conf XML file on startup to override settings, add ToolFactory and other configurable classes, mount servlets and filters, and so on

### Installing a Component

#### Load the Component

There are two ways to tell Moqui about a component:

-   put the component directory in the runtime/component directory
-   add a component-list.component element in the Moqui Conf XML file

#### Mounting Screen(s)

Each webapp in Moqui (including the default webroot webapp) must have a root screen specified in the moqui-conf.webapp-list.webapp.**root-screen-location** attribute. The default root screen is called webroot which is located at `runtime/base-component/webroot/screen/webroot.xml` (default subscreen: `qapps`).

For screens from your component to be available in a screen path under the webroot screen you need to make each top-level screen in your component (i.e. each screen in the component’s screen directory) a subscreen of another screen already under webroot. There are three ways to do this (this does not include putting it in the webroot directory as an implicit subscreen since that is not an option for screens defined elsewhere):

- add a `screen.subscreens.subscreen-item` element to the parent screen (what the subscreen will be under)
- add `screen-facade.screen` and `subscreens-item` elements in the Moqui Conf XML file (including MoquiConf.xml in a component); this subscreens-item element is much like the subscreens.subscreens-item element within a XML Screen
- add a record in the `SubscreensItem` entity, specifying the parent screen in the **screenLocation** field, the subscreen in the **subscreenLocation** field, the "mount point" in the **subscreenName** field (equivalent to the subscreens-item.**name** attribute), and either ALL_USERS in the **userGroupId** field for it to apply to all users, or an actual userGroupId for it to apply to just that user group

If you want your screen to use its own decoration and be independent from other screens, put it under the webroot screen directly. To have your screen part of the default apps menu structure and be decorated with the default apps decoration, put it under the apps screen (reachable as `/qapps/...` by default, and also as `/vapps/...` and `/apps/...`).

#### Moqui Conf XML File Settings

You may want to have things in your component add to or modify various things that come by default with Moqui Framework, including:

-   **Resource Reference**: see the moqui-conf.resource-facade.resource-reference element
-   **Template Renderer**: see the moqui-conf.resource-facade.template-renderer element
-   **Screen Text Output Template**: see the moqui-conf.screen-facade.screen-text-output element
-   **Service Type Runner**: see the moqui-conf.service-facade.service-type element
-   Explicit **Entity Data and Definition** files: see the moqui-conf.entity-facade.load-entity and moqui-conf.entity-facade.load-data elements

There are examples of all of these in the MoquiDefaultConf.xml file since the framework uses the Moqui Conf XML file for its own default configuration.
