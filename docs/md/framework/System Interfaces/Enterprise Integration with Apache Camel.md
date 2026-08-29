# Enterprise Integration with Apache Camel

Apache Camel ([http://camel.apache.org](http://camel.apache.org)) is a tool for routing and processing messages with tools for Enterprise Integration Patterns which are described here (and other pages on this site have much other good information about EIP): [http://www.eaipatterns.com/toc.html](http://www.eaipatterns.com/toc.html)

Apache Camel is **not** bundled with Moqui Framework. It lives in the optional **moqui-camel** component (`./gradlew getComponent -Pcomponent=moqui-camel`). That component registers a Camel ToolFactory and a Service Facade runner for *service*.**type**=camel, plus a Message Endpoint (*MoquiServiceEndpoint*) that ties Camel to the Service Facade.

With the component installed, services with **type**=camel send the service call as a message to Camel using the *MoquiServiceConsumer*. The endpoint also includes a message producer (*MoquiServiceProducer*) that is available in Camel routing strings as **moquiservice**.

Here are example Camel services from the example component (`ExampleServices.xml`). They only run if **moqui-camel** is installed. The same pair also exists in the component as `moqui.camel.CamelTestServices`.

```
<service verb="localCamelExample" type="camel"
 location="moquiservice:moqui.example.ExampleServices.targetCamelExample">
 <in-parameters><parameter name="testInput"/></in-parameters>
 <out-parameters><parameter name="testOutput"/></out-parameters>
</service>
<service verb="targetCamelExample">
 <in-parameters><parameter name="testInput"/></in-parameters>
 <out-parameters><parameter name="testOutput"/></out-parameters>
 <actions>
 <set field="testOutput" value="Input was: ${testInput}"/>
 <log level="info"
 message="targetCamelExample testOutput: '${testOutput}'"/>
 </actions>
</service>
```

When you call the **localCamelExample** service it calls the **targetCamelExample** service through Apache Camel. This is a very simple example of using services with Camel. To get an idea of the many things you can do with Camel the components reference is a good place to start:

[http://camel.apache.org/components.html](http://camel.apache.org/components.html)

The general idea is you can:

-   get message data from a wide variety of sources (file polling, incoming HTTP request, JMS messages, and many more)
-   transform messages (supported formats include XML, CSV, JSON, EDI, etc)
-   run custom expressions (even in Groovy!)
-   split, merge, route, filter, enrich, or apply any of the other EIP tools
-   send message(s) to endpoint(s)

Camel is a very flexible and feature rich tool so instead of trying to document and demonstrate more here I recommend these books:

-   *Instant Apache Camel Message Routing* by Bilgin Ibryam

    -   [**http://www.packtpub.com/apache-camel-message-routing/book**](http://www.packtpub.com/apache-camel-message-routing/book)
    -   This book is a quick introduction that will get you going quickly with lots of cool stuff you can do with Camel.

-   *Apache Camel Developer's Cookbook* by Scott Cranton and Jakub Korab

    -   [**http://www.packtpub.com/apache-camel-developers-cookbook/book**](http://www.packtpub.com/apache-camel-developers-cookbook/book)
    -   This book has hundreds of tips and examples for using Camel.

-   *Camel in Action* by Claus Ibsen and Jonathan Anstey

    -   [**http://manning.com/ibsen/**](http://manning.com/ibsen/)
    -   This is the classic book on Apache Camel. It covers general concepts, various internal details, how to apply the various EIPs, and a summary of many of the components. The web site for this book also has links to a bunch of useful online resources.
