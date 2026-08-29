# Resources: Content, Templates, and Scripts
[TOC levels=2-3]

## Resource Locations

A Resource Facade location string is structured like a URL with a protocol, host, optional port, and filename. It supports the standard Java URL protocols (http, https, ftp, jar, and file). It also supports some additional useful protocols:

-   **classpath://** for resources on the Java classpath
-   **content://** for resources in a content repository (JCR; optional, via `javax.jcr`). The first path element after the protocol prefix is the name of the content repository as specified in the repository.**name** attribute in the Moqui Conf XML file. No JCR repository is configured by default; Apache Jackrabbit can be used if the client libraries are on the classpath and a `repository` is configured. The `JackrabbitRunToolFactory` that can start a local Jackrabbit process is disabled by default.
-   **component://** for locations relative to a component base location, no matter where the component is located (file system, content repository, etc)
-   **dbresource://** for a virtual filesystem persisted with the Entity Facade in a database using the moqui.resource.DbResource and DbResourceFile entities
-   **runtime://** for locations relative to the runtime directory

Additional protocols can be added by extending the `org.moqui.resource.ResourceReference` class and adding a `resource-facade.resource-reference` element to the Moqui Conf XML file. The supported protocols listed above are configured this way in the MoquiDefaultConf.xml file.

## Using Resources

The simplest way to use a resource, and supported by all location protocols, is to read the text or binary content. To get the text from a resource location use the ec.resource.**getLocationText**(String location, boolean cache) method. To get an InputStream for binary or large text resources use the ec.resource.**getLocationStream**(String location) method.

For a wider variety of operations beyond just reading resource data use the ec.resource.**getLocationReference**(String location) method to get an instance of `org.moqui.resource.ResourceReference`. This class has methods to get text or binary stream data from the resource like the Resource Facade methods. It also has methods for directory resources to get child resources, find child files and/or directories recursively by name, write text or binary stream data, and move the resource to another location.

## Rendering Templates and Running Scripts

There is a single method for rendering a template in a resource at a location: ec.resource.**template**(String location, Writer writer). This method returns nothing and writes the template output to the writer. By default FTL (FreeMarker Template Language), GString (Groovy String), and Markdown (`.md`, `.markdown`) are supported.

Additional template renderers can be supported by implementing the `org.moqui.context.TemplateRenderer` interface and adding a `resource-facade.template-renderer` element to the Moqui Conf XML file.

To run a script through the Resource Facade use the Object ec.resource.**script**(String location, String method) method. Specify the location and optionally the method within the script at the location and this method will run the script and return the Object that the script returns or evaluates to. There is a variation on this method that also accepts a Map **additionalContext** parameter for convenience (it just pushes the Map onto the context stack, runs the script, then pops from the context stack). By default Moqui supports Groovy and XML Actions. Other languages are available through the `javax.script.ScriptEngineManager` when a matching engine is on the classpath (the default conf still registers `.js` that way).

To add a script runner you have two options. You can use the javax.script approach for any scripting language that implements the `javax.script.ScriptEngine` interface and is discoverable through the `javax.script.ScriptEngineManager`. Moqui uses this to discover the script engine using the extension on the script’s filename and execute the script. If the script engine implements the `javax.script.Compilable` interface then Moqui will compile the script and cache it in compiled form for faster repeat execution of a script at a given location.

The other option is to implement the `org.moqui.context.ScriptRunner` interface and add a `resource-facade.script-runner` element to the Moqui Conf XML file. Moqui uses Groovy and XML Actions through this interface as it provides additional flexibility not available through the javax.script interfaces.

Because Groovy is the default expression language in Moqui there are a few Resource Facade methods to easily evaluate expressions for different purposes:

-   boolean **condition**(String expression, String debugLocation) is used to evaluate a Groovy condition expression and return the boolean result
-   Object **expression**(String expr, String debugLocation) is used to evaluate the expression to return a field within the context, and more generally to evaluate any Groovy expression and return the result
-   String **expand**(String inputString, String debugLocation) is used to expand the inputString, treating it as a GString (Groovy String) and returns the expanded value

These methods accept a debugLocation parameter that is used in error messages. For faster evaluation these expressions are all cached, using the expression itself as the key for maximal reuse.
