# Web Service
[TOC levels 2-3]

## XML-RPC and JSON-RPC

Moqui has tools for providing and consuming XML-RPC and JSON-RPC services. Any Service Facade service can be exposed as a remote callable service by setting the *service*.**allow-remote** attribute to true.

The Web Facade has methods to receive these RPC calls: *ec.web*.**handleXmlRpcServiceCall()** and *ec.web*.**handleJsonRpcServiceCall()**. In the OOTB webroot component there is a rpc.xml screen that has **xml** and **json** transitions that call these methods. With the setup the URL paths for the remote service calls are /rpc/xml and /rpc/json.

Below is an example of a JSON-RPC service call, using curl as the client. It calls the *org.moqui.example.ExampleServices*.**createExample** service with name, type, and status parameters. It also passes in the username and password to use for authentication before running the service (following a pattern that can be used for any Service Facade service call).

The **id** field is always something like 1. This JSON-RPC field is used for multi-message requests Each message in the request would have a different **id** value and that value is used in the **id** field in the response. To use this the JSON string would have an outer list containing the individual messages like the one in this example.

```
curl -X POST -H "Content-Type:application/json"
 --data{  
  "jsonrpc":"2.0",
  "method":"org.moqui.example.ExampleServices.createExample",
  "id":1,
  "params":{  
    "authUsername":"john.doe",
    "authPassword":"moqui",
    "exampleName":"JSON-RPC Test 1",
    "exampleTypeEnumId":"EXT_MADE_UP",
    "statusId":"EXST_IN_DESIGN"
  }
  ```

 http://localhost:8080/rpc/json

When you run this you will get a response like (the **exampleId** value will vary):

```
{  
  "jsonrpc":"2.0",
  "id":1,
  "result":{  
    "exampleId":"100050"
  }
}
```

The JSON-RPC implementation in Moqui follows the JSON-RPC 2.0 specification available at: [*http://www.jsonrpc.org/specification*](http://www.jsonrpc.org/specification).

XML-RPC requests follow a similar pattern. Moqui uses Apache XML-RPC library ([*http://ws.apache.org/xmlrpc/*](http://ws.apache.org/xmlrpc/)) which implements the XML-RPC specification available at: [*http://xmlrpc.scripting.com/spec.html*](http://xmlrpc.scripting.com/spec.html).

While you can write code call remote XML-RPC and JSON-RPC services by directly using a library (or custom JSON handling code like in RemoteJsonRpcServiceRunner.groovy), the easiest way to call remote services is to use a proxy service definition. To do this:

-   define a service
-   use remote-xml-rpc or remote-json-rpc for the *service*.**type** attribute
-   set *service*.**location** to the URL of the RPC server and path (such as http://localhost:8080/rpc/json), or to a value matching a service location name in the Moqui Conf XML file (i.e. *service-facade.service-location*.**name**); there are two OOTB service locations for the purpose of calling remote services: main-xml and main-json; these and additional desired one can be configured in the runtime Moqui Conf XML file and then used in your service locations to simplify configuration, especially when you have different URLs for test and production environments
-   set *service*.**method** to the name of the remote service to call; in JSON-RPC this maps to the **method** field; in XML-RPC this maps to the *methodName* element; when calling another Moqui server this is the name of the service that will be called
-   the service can have parameters to define that match the remote service definition, or can be setup to not validate input; you can also define parameters with defaults and specify types for type conversion which are done before the remote service is called

When you call this service locally the Service Facade will call the remote service and return the results. In other words, you call a local service that is a configured proxy to the remote service.

## Sending and Receiving Simple JSON

Sometimes an API spec calls for a particular JSON structure or something other than the envelope structure of JSON-RPC. There are some feature in the Web Facade that make this easier.

When a HTTP request is received (really when the Web Facade is initialized) if the **Content-Type** (MIME type) of the request is application/json it will parse the JSON string in the request body and if the outer element is a Map (in JSON an object) then the entries in that Map will be added to the web parameters (ec.web.parameters), and web parameters are automatically added to the context (ec.context) with a screen is rendered or a screen transition run. If the outer element is a List (in JSON an array) then it is put in a **\_requestBodyJsonList** web parameter, and again from there available in the context.

This makes it easy to get at the JSON data in a web request. It also resolves issues with getting the request body after the Web Facade automatically looks for multi-part content in the request body (which the Web Facade always does) because the Servlet container may not allow reading the request body again after this.

For a JSON response you can manually put together the response by setting various things on the *HttpServletResponse* and using the Groovy *JsonBuilder* to produce the JSON text. For convenience the *ec.web*.**sendJsonResponse**(Object responseObj) method does all of this for you.

To go in the other direction, doing a request to a URL that accepts and responds with JSON, there are special tools because the Groovy and other utilities make this pretty simple. For example, this a variation on the actual code that remotely calls a JSON-RPC service:

*Map* jsonRequestMap = \[ jsonrpc:"2.0", id:1, method:method, params:parameters \]

*JsonBuilder* jb = new *JsonBuilder*()

jb.**call**(jsonRequestMap)

*String* jsonResponse = `StupidWebUtilities`.**simpleHttpStringRequest**(location,

 jb.**toString**(), "application/json")

*Object* jsonObj = new *JsonSlurper*().**parseText**(jsonResponse)

This uses the *JsonBuilder* and *JsonSlurper* classes from Groovy and the `StupidWebUtilities`.**simpleHttpStringRequest**() method which internally uses the Apache HTTP Client library.

## RESTful Interface

A RESTful service uses a URL pattern and request method to identify a service instead of a method name like JSON-RPC and XML-RPC. The general idea is to have things like a record represented by URL with the type of record (like an entity or table) as a path element and the ID of the record as one or more path elements (often one for simplicity, i.e., a single field primary key).

When interacting with this record as a web resource the HTTP request method specifies what to do with the record. This is much like the create, update, and delete service verbs for Moqui entity-auto services. The GET method generally does a record lookup. The POST method generally maps to creating a record. The PUT method generally maps to updating a record. The DELETE method does the obvious, a delete.

For examples, such as the one below, see the ExampleApp.xml file.

To support RESTful web services we need a way for transitions to be sensitive to the HTTP request method when running in a web-based application. This is handled in Moqui Framework using the transition.**method** attribute, like this:

```
<transition name="ExampleEntity" method="put">
 <path-parameter name="exampleId"/>
 <service-call name="org.moqui.example.ExampleServices.updateExample"
 in-map="ec.web.parameters" web-send-json-response="true"/>
 <default-response type="none"/>
</transition>
```

To test this transition use a curl command something like this to update the **exampleName** field of the Example entity with an **exampleId** of 100010:

```
curl -X PUT -H "Content-Type: application/json" \
 -H "Authorization: Basic am9obi5kb2U6bW9xdWk=" \
 --data '{ "exampleName":"REST Test - Rev 2" }' \
```

 http://.../apps/example/ExampleEntity/100010

There are some important things to note about this example that make it easier to create REST wrappers around internal Moqui services:

-   uses HTTP Basic authentication (john.doe/moqui), which Moqui automatically recognizes and uses for authentication
-   uses the automatic JSON body input mapping to parameters (the JSON string must have a Map root object)
-   the **exampleId** is passed as part of the path and treated as a normal parameter using the *path-parameter* element
-   uses the ec.web.parameters *Map* as the **in-map** to explicitly pass the web parameters to the service (could also use ec.context for the entire context which would also include the web parameters, but this way is more explicit and constrained)
-   sends a JSON response with the *service-call.web-send-json-response* convenience attribute and a type none response

There are various other examples of handling RESTful service requests in the `ExampleApp`.xml file.
