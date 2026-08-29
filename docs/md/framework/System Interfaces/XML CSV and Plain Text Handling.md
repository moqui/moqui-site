# XML, CSV and Plain Text Handling

There are various ways to produce and consume XML, CSV, JSON, and other text data using Moqui Framework.

Groovy has a good API for producing and consuming XML with:

-   ***groovy.util.Node***: The Groovy class that represents a tree node with attributes and child nodes. For XML data each element is represented as a Node.
-   ***groovy.xml.XmlNodePrinter***: Print XML text from a tree of Node objects.
-   ***groovy.xml.XmlParser***: Read XML text into a tree of Node objects.
-   ***groovy.xml.XmlSlurper***: Read XML text into a GPathResult object which can be used in Groovy with a syntax similar to XPath expressions to pull out specific parts of an XML element tree.
-   ***groovy.xml.MarkupBuilder***: Offers a Groovy DSL (domain-specific language) for writing code that has a structure similar to the structure of the XML output. Most useful for scripts that explicitly create an XML tree as opposed to building more dynamically.

There are many other XML libraries written in Java that can be used with Moqui such as dom4j and JDOM. If you prefer these just include the JAR files in the Gradle build and code away.

For CSV files Moqui uses the Apache Commons CSV library, and just like with XML files other libraries can be used too. You can see how Moqui uses this in the `org.moqui.impl.entity.EntityDataLoaderImpl.EntityCsvHandler` class.

In Moqui Framework the main tool for reporting and exporting data is the XML Form, especially the list form. XML Screens and Forms can be rendered in various modes including XML, CSV, and plain text. To do this set the **renderMode** field in the context either in screen actions or for web requests with a request parameter. This is matched against the *screen-facade.screen-text-output*.**type** attribute in the Moqui Conf XML file and can be set to any value defined there, including the default Moqui ones (csv, html, text, xml, xsl-fo, plus UI modes such as vuet and qvt) or any that you define in your runtime Moqui Conf XML file.

The XML Form is probably set up for pagination (this is the default). To get all results instead of pagination for an export (or any other reason) set the **pageNoLimit** field to true. In some cases you will not want to render any of the parent screens that normally decorate the final screen to render, especially for XML files. For CSV files other screen elements are generally ignored. This can be done by setting the **lastStandalone** field to true meaning that the last screen is rendered standalone and not within parent screens in the screen path. These can be set in screen actions or for web requests as a request parameter.

Just as with other XML Screen and XML Form output modes the FTL macro template used to produce output can be customized by include and override/add. With this approach you can get custom output for a particular screen (including subscreens, so for an entire app or app section, etc) or for everything running in Moqui.

For a detailed example of a screen and form that has CSV, XML, and XSL-FO (PDF) output options see the **List Form View/Export Example** section in [XML Form](/docs/framework/User+Interface/XML+Form).
