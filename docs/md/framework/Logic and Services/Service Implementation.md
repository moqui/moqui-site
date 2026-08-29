# Service Implementation

Some service types have local implementations while others have no implementation (interface) or the service definition is a proxy for something else and the location refers to an external implementation (*remote-xml-rpc*,* remote-json-rpc*, and *camel*). The remote and *Apache Camel* types are described in detail in the System Interfaces section.

[TOC levels=2-3]
## Service Scripts

A script is generally the best way to implement a service, unless an automatic implementation for entity CrUD operations will do. Scripts are reloaded automatically when their cache entry is clear, and in development mode these caches expire in a short time by default to get updates automatically.

Scripts can run very efficiently, especially *Groovy* scripts which compile to Java classes at runtime and are cached in their compiled form so they can be run quickly. XML Actions scripts are transformed into a Groovy script (see the* XmlActions.groovy.ftl* file for details) and then compiled and cached, so have a performance profile just like a plain *Groovy* script.

Any script that the Resource Facade can run can be used as a service implementation. See the **Rendering Templates and Running Scripts** section for details. In summary the scripts supported by default are Groovy, XML Actions, and JavaScript. Any scripting language can be supported through the *javax.script* or Moqui-specific interfaces. Here is an example of a service implemented with a Groovy script, defined in the *org.moqui.impl.EmailServices.xml* file:
```
<service verb="send" noun="Email" type="script"
             location="classpath://org/moqui/impl/sendEmailTemplate.groovy" allow-remote="false">
        <implements service="org.moqui.EmailServices.send#EmailTemplate"/>
</service>
```
In this case the **location** is a classpath location, but any location supported by the Resource Facade can be used. See the **Resource Locations** section for details on how to refer to files within components, in the local file system, or even at general URLs.

At the beginning of a script all of the input parameters passed into the service, or set through defaults in the service definition, will be in the context as fields available for use in the script. As with other artifacts in Moqui there is also an **ec** field with the current *ExecutionContext* object.

Note that the script has a context isolated from whatever called it using the *ContextStack*.**pushContext**() and **popContext**() methods meaning not only do fields created in the context not persist after the service is run, but the service does not have access to the context of whatever called it even though it may be running locally and within the same *ExecutionContext* as whatever called it.

For convenience there is a result field in the context that is of type Map&lt;String, Object&gt;. You can put output parameters in this Map to return them, but doing so is not necessary. After the script is run the script service runner looks for all output parameters defined on the service in the context and adds them to the results. The script can also return (evaluate to) a Map object to return results.

### Inline Actions

The service definition example near the beginning of this section shows a service with the default service type, inline. In this case the implementation is in the *service.actions* element, which contains a XML Actions script. It is treated just like an external script referred to by the service location but for simplicity and to reduce the number of files to work with it can be inline in the service definition.

## Java Methods

A service implementation can also be a Java method, either a class (static) method or an object method. If the method is not static then the service runner creates a new instance of the object using the default (no arguments) constructor.

The method must take a single *ExecutionContext* argument and return a Map&lt;String, Object&gt;, so the signature of the method would be something like:

```
Map<String, Object> myService(ExecutionContext ec)
```

## Entity Auto Services

With entity-auto type services you don’t have to implement the service, the implementation is automatic based on the **verb** and **noun** attribute values. The verb can be *create*, *update*, *delete*, or *store* (which is a create if the record does not exist, update if it does). The noun is an entity name, either a full name with the package or just the simple entity name with no package.

Entity Auto services can be implicitly (automatically) defined by just calling a service named like ${verb}#${noun} with no path (package or filename). For example:

```
ec.service.sync().name("create", "moqui.example.Example").parameters([exampleName:’Test Example’]).call()
```

When you define a service and use the entity-auto implementation you can specify which input parameters to use (must match fields on the entity), whether they are required, default values, etc. When you use an implicitly defined entity auto service it determines the behavior based on what is passed into the service call. In the example above there is no **exampleId** parameter passed in, and that is the primary key field of the `moqui.example.Example` entity, so it automatically generates a sequenced ID for the field, and returns it as an output parameter.

For create operations in addition to automatically generating missing primary sequenced IDs it will also generate a secondary sequenced ID if the entity has a 2-part primary key and one is specified while the other is missing. There is also special behavior if there is a **fromDate** primary key field that is not passed in, it will use the now Timestamp to populate it.

The pattern for is update to pass in all primary key fields (this is required) and any non-PK field desired. There is special behavior for update as well. If the entity has a **statusId** field and a statusId parameter is passed in that is different then it automatically returns the original (DB) value in the oldStatusId output parameter. Whenever the entity has a statusId field it also returns a *statusChanged* boolean parameter which is true if the parameter is different from the original (DB) value, false otherwise. Entity auto services also enforce valid status transitions by checking for the existing of a matching `moqui.basic.StatusFlowTransition` record. If no valid transition is found it will return an error.

## Add Your Own Service Runner

To add your own service runner, with its own service type, implement the `org.moqui.impl.service.ServiceRunner` interface and add a `service-facade.service-type` element in the Moqui Conf XML file.

The ServiceRunner interface has 3 methods to implement:
```
ServiceRunner init(ServiceFacadeImpl sfi);
Map<String, Object> runService(ServiceDefinition sd, Map<String, Object> parameters) throws ServiceException;
void destroy();
```

Here is an example of a *service-facade.service-type* element from the *MoquiDefaultConf.xml* file:
```
<service-type name="script"  runner-class="org.moqui.impl.service.runner.ScriptServiceRunner"/>
```
The service-type.**name** attribute matches against the service.**type** attribute, and the **runner-class** attribute is simply the class that implements the ServiceRunner interface.
