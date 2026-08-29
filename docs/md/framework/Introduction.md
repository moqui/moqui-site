
# Introduction to Moqui Framework

[TOC levels=2-3]

## What is the Moqui Ecosystem?

The Moqui Ecosystem is a set of software packages built on a common framework and universal business artifacts. The packages are organized as separate open source projects to keep their purpose, management, and dependencies focused and clean. All are managed with a moderated community model, much like the Linux Kernel.

![Moqui World](/docs/attachment/100153/MoquiWorld600.png)

The goal of the ecosystem is to provide a number of interoperating and yet competing enterprise applications, all based on a common framework for flexibility and easy customization, and a common set of business artifacts (data model and services) so they are implicitly integrated.

The ecosystem includes:

-   **Moqui Framework**: Synergistic tools for efficient and flexible application building
-   **Mantle Business Artifacts**: Universal business artifacts to make your applications easier to build and implicitly integrated with other apps built on Moqui and Mantle
    - Universal Data Model (UDM)
    - Universal Service Library (USL)
-   **Applications**: applications for different industries, company sizes, business areas, etc
    - Marble ERP, a general ERP application built on SimpleScreens
    - POP Commerce ERP and eCommerce for Retailers and Wholesalers
    - HiveMind Project Management and ERP for Service Organizations
-   **Add Ons**: themes, tool components, integration components

These documents focus on Moqui Framework. For the shared data model and services, see the [Mantle Business Artifacts](/docs/mantle) documentation.

## What is Moqui Framework?

Moqui Framework is an all-in-one, enterprise-ready application framework based on Groovy and Java. The framework includes tools for screens, services, entities, and advanced functionality based on them such as declarative artifact-aware security and multi-instance deployment (a separate runtime and database per instance).

The Framework is well suited for a wide variety of applications from simple web sites (like moqui.org) and small form-based applications to complex ERP systems. Applications built with Moqui are easy to deploy on a wide variety of highly scalable infrastructure software such as Jakarta Servlet containers (or app servers) and both traditional relational and more modern NoSQL databases.

Moqui Framework is based on a decade of experience with The Open For Business Project (now Apache OFBiz, see <https://ofbiz.apache.org>) and designed and written by the person who founded that project. Many of the ideas and approaches, including the pure relational data layer (no object-relational mapping) and the service-oriented logic layer, stem from this legacy and are present in Moqui in a more refined and organized form.

With a cleaner design, more straightforward implementation, and better use of other excellent open source libraries that did not exist when OFBiz was started in 2001, the Moqui Framework code is about 20% of the size of the OFBiz Framework while offering significantly more functionality and more advanced tools.

The result is a framework that helps you build applications and automatically handles many concerns that would otherwise require a significant percentage of overall effort for every application you build.

## Moqui Concepts

### Application Artifacts

The Moqui Framework toolset is structured around artifacts that you can create to represent common parts of applications. In Moqui the term artifact refers to anything you create as a developer and includes various XML files as well as scripts and other code. The framework supports artifacts for things like:

-   **entities** for the relational data model used throughout applications (used directly, no redundant object-relational mapping)
-   **screens** and **forms** for web-based and other user interfaces (base artifacts in XML files with general or user-specific extensions in the database)
-   screen **transitions** to configure flow from screen to screen and process input as needed along the way
-   **services** for logic run internally or exposed for remote execution
-   **ECA** (event-condition-action) rules triggered on system events like entity and service operations and received email messages

Here is a table of common parts of an application and the artifact or part of an artifact that handles each:

| Concept                                 | Tool              |
|-----------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| screen                                  | XML Screen (rendered as various types of text, or can be used to generate other UIs; OOTB support for html, xml, xsl-fo, csv, and plain text)                         |
| form                                    | XML Form (defined within a screen; various OOTB widgets and easy to add custom ones or customize existing ones)                                                       |
| prepare data for display                | screen actions (defined within a screen, can call external logic)                                                                                                     |
| flow from one screen to another         | screen transition with conditional and default responses (defined within the originating screen, response points to destination screen or external resource)          |
| process input                           | transition actions (either a single service defined to match the form and share validations/etc, or actions embedded in the screen definition or call external logic) |
| menu                                    | automatic based on sub-screen hierarchy and configured menu title and order for each screen, or define explicitly                                                     |
| internal service                        | XML service definition and various options for embedded or external service implementations                                                                           |
| RESTful web services                    | internal service called through REST interface configured in a Service REST XML file                                                                                  |
| JSON-RPC services                       | internal service with **allow-remote**=true and called through generic interfaces using the natural List and Map structure mappings                                   |
| remote service calls                    | define an internal service as a proxy with automatic JSON-RPC and other mappings, or use simple tools for RESTful and other service types                   |
| send email                              | screen designed to be rendered directly as html and plain text and configured along with subject, etc in an EmailTemplate record                                      |
| receive email                           | define an Email ECA rule to call an internal service that processes the email                                                                                         |
| use scripts, templates, and JCR content | access and execute/render through the Resource Facade                                                                                                                 |

### The Execution Context

The ExecutionContext is the central application-facing interface in the Moqui API. An instance is created specifically for executing edge artifacts such as a screen or service. The ExecutionContext, or "ec" for short, has various facade interfaces that expose functionality for the various tools in the framework.

The ec also keeps a context map that represents the variable space that each artifact runs in. This context map is a stack of maps and as each artifact is executed a fresh map is pushed onto the stack, then popped off it once the artifact is done executing. When reading from the map stack it starts at the top and goes down until it finds a matching map entry. When writing to the map stack it always writes to the map at the top of the stack (unless to explicitly reference the root map, i.e., at the bottom of the stack).

With this approach each artifact can run without concern of interfering with other artifacts, but still able to easily access data from parent artifacts (the chain of artifacts that called or included down to the current artifact). Because the ec is created for the execution of each edge artifact it has detailed information about every aspect of what is happening, including the user, messages from artifacts, and much more.

### The Artifact Stack

As each artifact is executed and includes or calls other artifacts the artifact is pushed onto a stack that keeps track of the active artifacts, and is added to an artifact history list tracking each artifact used.

As artifacts are pushed onto the stack authorization for each artifact is checked, and security information related to the artifact is tracked. With this approach authz settings can be simplified so that artifacts that include or call or artifacts can allow those artifacts to inherit authorization. With inherited authorization configurations are only needed for key screens and services that are accessed directly.

### Peeking Under the Covers

When working with Moqui Framework you’ll often be using higher-level artifacts such as XML files. These are designed to support most common needs and have the flexibility to drop down to lower level tools such as templates and scripts at any point. At some point though you’ll probably either get curious about what the framework is doing, or you’ll run into a problem that will be much easier to solve if you know exactly what is going on under the covers.

While service and entity definitions are handled through code other artifacts like XML Actions and the XML Screens and Forms are just transformed into other text using macros in FreeMarker template files. XML Actions are converted into a plain old Groovy script and then compiled into a class which is cached and executed. The visual (widget) parts of XML Screens and Forms are also just transformed into the specified output type (html, xml, xsl-fo, csv, text, etc) using a template for each type.

With this approach you can easily see the text that is generated along with the templates that produced the text, and through simple configuration you can even point to your own templates to modify or extend the OOTB functionality.

### Development Process

Moqui Framework is designed to facilitate implementation with natural concept mappings from design elements such as screen outlines and wireframes, screen flow diagrams, data statements, and automated process descriptions. Each of these sorts of design artifacts can be turned into a specific implementation artifact using the Moqui tools.

These design artifacts are usually best when based on requirements that define and structure specific activities that the system should support to interact with other actors including people and systems. These requirements should be distinct and separate from the designs to help drive design decisions and make sure that all important aspects of the system are considered and covered in the designs.

With this approach implementation artifacts can reference the designs they are based on, and in turn designs can reference the requirements they are based on. With implementation artifacts that naturally map to design artifacts both tasking and testing are straightforward.

When implementing artifacts based on such designs the order that artifacts are created is not so important. Different people can even work simultaneously on things like defining entities and building screens.

For web-based applications, especially public-facing ones that require custom artwork and design, the static artifacts such as images and CSS can be in separate files stored along with screen XML files using the same directory structure that is used for subscreens using a directory with the same name as the screen. Resources shared among many screens live naturally under screens higher up in the subscreen hierarchy.

The actual HTML generated from XML Screens and Forms can be customized by overriding or adding to the FreeMarker macros that are used to generate output for each XML element. Custom HTML can also be included as needed. This allows for easy visual customization of the generic HTML using CSS and JavaScript, or when needed totally custom HTML, CSS, and JavaScript to get any effect desired.

Web designers who work with HTML and CSS can look at the actual HTML generated and style using separate CSS and other static files. When more custom HTML is needed the web designers can produce the HTML that a developer can put in a template and parameterize as needed for dynamic elements.

Another option that sometimes works well is to have more advanced web designers build the entire client side as custom HTML, CSS, and JavaScript that interacts with the server through a service interface using some form of JSON over HTTP. This approach also works well with client applications for mobile or desktop devices that will interact with the application server using web services. The web services can use the automatic JSON-RPC or other custom automatic mappings, or can use custom wrapper services that call internal services to support any sort of web service architecture.

However your team is structured and however work is to be divided on a given project, with artifacts designed to handle defined parts of applications it is easier to split up work and allow people to work in parallel based on defined interfaces.

### Development Tools

For requirements and designs you need a group content collaboration tool that will be used by users and domain experts, analysts, designers, and developers. The collaboration tool should support:

-   hierarchical documents
-   links between documents and parts of documents (usually to headers within the target document)
-   attachments to documents for images and other supporting documents
-   full revision history for each document
-   threaded comments on each document
-   email notification for document updates
-   online access with a central repository for easy collaboration

There are various options for this sort of tool, though many do not support all the above and collaboration suffers because of it. One good commercial option is Atlassian Confluence. Atlassian offers a very affordable hosted solution for small groups along with various options for larger organizations. There are various open source options, including the wiki built into HiveMind PM which is based on Moqui Framework and Mantle Business Artifacts.

Note that this content collaboration tool is generally separate from your code repository, though putting requirement and design content in your code repository can work if everyone involved is able to use it effectively. Because Moqui itself can render wiki pages and pass through binary attachments you might even consider keeping this in a Moqui component. The main problem with this is that until there is a good wiki application built on Moqui to allow changing the content, this is very difficult for less technical people involved.

For the actual code repository there are various good options and this often depends on personal and organizational preferences. Moqui itself is hosted on GitHub and hosted private repositories on GitHub are very affordable (especially for a small number of repositories). If you do use GitHub it is easy to fork the moqui/moqui repository to maintain your own runtime directory in your private repository while keeping up to date with the changes in the main project code base.

Even if you don’t use GitHub a local or hosted git repository is a great way to manage source code for a development project. If you prefer other tools such as Subversion or Mercurial then there is no reason not to use them.

For actual coding purposes you’ll need an editor or IDE that supports the following types of files:

-   XML (with autocompletion, validation, annotation display, etc)
-   Groovy (for script files and scripts embedded in XML files)
-   HTML, CSS, and JavaScript
-   FreeMarker (FTL)
-   Java (optional)

My preferred IDE these days is IntelliJ IDEA from JetBrains. The free Community Edition has excellent XML and Groovy support. For HTML, CSS, JavaScript, and FreeMarker to go beyond a simple text editor you’ll have to pay for the Ultimate Edition. I implemented most of Moqui, including the complex FreeMarker macro templates, using the Community Edition. After breaking down and buying a personal license for the Ultimate Edition I am happy with it, but the Community Edition is impressively capable.

Other popular Java IDEs like Eclipse and NetBeans are also great options and have built-in or plugin functionality to support all of these types of files. I personally prefer having autocomplete and other advanced IDE functionality around, but if you prefer a more simple text editor then of course use what makes you happy and productive.

The Moqui Framework itself is built using Gradle. While I prefer the command line version of Gradle (and Git), most IDEs (including IntelliJ IDEA) include decent user interfaces for these tools that help simplify common tasks.

## A Top to Bottom Tour

![Framework Tour](/docs/attachment/100153/FrameworkTour.svg)

### Web Browser Request

A request from a web browser will find its way to the framework by way of the Servlet Container (the default is the embedded Jetty Servlet Container; it also works well with Apache Tomcat and other Jakarta Servlet implementations). The Servlet Container finds the requested path on the server in the standard way using the web.xml file and will find the MoquiServlet mounted there. The MoquiServlet is quite simple and just sets up an ExecutionContext, then renders the requested Screen.

The screen is rendered based on the configured "root" screen for the webapp, and the subscreens path to get down to the desired target screen. Beyond the path to the target screen there may be a transition name for a transition of that screen.

A transition is part of a screen definition and is used to go one from screen to another (or back to the same). Transitions are used to process input (not to prepare data for presentation), which is separated from the screen actions which are used to prepare data for presentation (not to process input).

If there is a transition name in the URL path the service or actions of the transition will be run, a response to the transition selected (based on conditions and whether there was an error), and then the response will be followed, usually to another screen.

When a service is called (often from a transition or screen action) the Service Facade validates and cleans up the input parameters to the service call using the defined input parameters on the service definition, and then calls the defined inline or external script, Java method, auto or implicit entity operation, or remote service.

Entity operations, which interact with the database, should only be called from services for write operations and can be called from actions anywhere for read operations (transition or screen actions, service scripts/methods, etc).

### Web Service Call

Web Service requests generally follow the same path as a form submission request from a web browser that is handled by a Screen Transition. The incoming data will be handled by the transition actions, and typically the response will be handled by an action that sends back the encoded response (in XML, JSON, etc) and the default-response for the transition will be of type "none" so that no screen is rendered and no redirecting to a screen is done.

### Incoming and Outgoing Email

Incoming email is handled through Email ECA rules which are called by the `org.moqui.impl.EmailServices.poll#EmailServer` service (configured using the EmailServer entity). These rules have information about the email received parsed and available to them in structured Maps. If the condition of a rule passes, then the actions of the rule will be run. Rules can be written to do anything you would like, typically saving the message somewhere, adding it to a queue for review based on content, generating an automated response, and so on.

Outgoing email is most easily done with a call to the `org.moqui.impl.EmailServices.send#EmailTemplate` service. This service uses the passed in emailTemplateId to lookup an EmailTemplate record that has settings for the email to render, including the subject, the from address, the XML Screen to render and use for the email body, screens or templates to render and attach, and various other options. This is meant to be used for all sorts of emails, especially notification messages and system-managed communication like customer service replies and such.

## High Level Overview of the Moqui Framework

Moqui Framework is a [server-side web framework](https://developer.mozilla.org/en-US/docs/Learn/Server-side/First_steps/Web_frameworks#overview) written primarily in [Java](https://java.com/en/download/help/whatis_java.html) and [Groovy](https://groovy-lang.org/).

### Web Server

When you run Moqui as an executable WAR file (`java -jar moqui.war`), Moqui Framework uses [Jetty](https://jetty.org/docs/) as its HTTP server, client, and [servlet container](https://en.wikipedia.org/wiki/Jakarta_Servlet). The embedded Jetty server is not used when the WAR file is dropped into an external Servlet Container (Jetty, Tomcat, or another Jakarta Servlet container).

### Start (`java -jar moqui.war`)

Moqui starts in [`MoquiStart.java`](https://github.com/moqui/moqui-framework/blob/master/framework/src/start/java/MoquiStart.java), which starts the embedded web server.

By default the Moqui server listens on port 8080. You can change that with the `port=<port>` argument. See more about Moqui Conf XML files [here](/docs/framework/Tool+and+Config+Overview#moqui-conf-xml-file-settings).

### Component Bundling and MoquiConf.xml Configuration Files

After the web server has started, Moqui Framework loads *components*. Components in `runtime/base-component` are added first, then those in `runtime/component`. They are then sorted by dependency. For example, if A depends on B and C depends on A, they would be sorted B, A, then C. For each configuration node, later components override earlier settings. If B changed a property and C changed the same property, C's setting would override B's. After running Moqui you can see the merged configuration in `runtime/log/MoquiActualConf.xml`. That is the configuration actually used; see [Moqui Conf XML file settings](/docs/framework/Tool+and+Config+Overview#moqui-conf-xml-file-settings).

### Pre Facade Init

After the conf files are built, the following happens:

1. Groovy scripts are added to `runtime/script-classes`
2. Java classes in JAR files are added to the `runtime/classes` directory
3. Library JAR files are added to the `runtime/lib` directory
4. Tool Factories are added

### Finish Facade Init

Note: the [Execution and Web](/docs/framework/Tool+and+Config+Overview#execution-context-and-web-facade), [Artifact Execution, L10n, Message, and User](/docs/framework/Tool+and+Config+Overview#user-l10n-message-and-logger-facades) facades are not initialized here; they are used later in the process.

Then the facades initialize in this order:

1. [Cache Facade](/docs/framework/Tool+and+Config+Overview#resource-and-cache-facades): key/value data storage (see the MCache class)
2. [Logger Facade](/docs/framework/Tool+and+Config+Overview#user-l10n-message-and-logger-facades): logging
3. [Resource Facade](/docs/framework/Data+and+Resources/Resources+and+Content): accessing resources by location string (`http://`, `jar://`, `component://`, `content://`, `classpath://`, and so on)
4. [Transaction Facade](/docs/framework/Tool+and+Config+Overview#transaction-facade): transaction manager for Atomicity, Consistency, Isolation, and Durability ([ACID](https://en.wikipedia.org/wiki/Atomicity_(database_systems)))
5. [Entity Facade](/docs/framework/Data+and+Resources/The+Entity+Facade): database-independent interaction through a [JDBC](https://en.wikipedia.org/wiki/Java_Database_Connectivity) driver
6. [Service Facade](/docs/framework/Tool+and+Config+Overview#service-facade): call Moqui, REST, and JSON-RPC services to perform logic
7. [Screen Facade](/docs/framework/Tool+and+Config+Overview#screen-facade): rendering screens for general use (including output other than web pages)
8. [Elastic Facade](/docs/framework/Data+and+Resources/Data+Search): OpenSearch and ElasticSearch client via ElasticFacade (`ec.elastic`)
