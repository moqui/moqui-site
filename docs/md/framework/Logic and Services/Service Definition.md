# Service Definition

With Moqui Framework the main unit of logic is the service. This is a service-oriented architecture with services used as internal, granular units of logic as well as external, coarse aggregations of logic. Moqui services are:

-   transactional
-   secure (both authentication and authorization, plus tarpit for velocity limits)
-   validated (data types and various constraints for input parameters)
-   implemented with any of a wide variety of languages and tools including scripting languages, Java methods, an even an Apache Camel endpoint
-   run from a local or remote caller
-   run synchronously, asynchronously, or on a schedule
-   a source of triggers at various phases of execution to run other services using service event-condition-action (SECA) rules
-   optionally restricted to a single running instance with a database semaphore

*Services* are defined in a services XML file using the service element. A service name is composed of a path, a *verb* and a *noun* in this structure: **${path.verb#noun}**. Note that the noun is optional in a service definition, and in a service name the hash (#) between the verb and noun is also optional. Here is an example, the `mantle.party.PartyServices.create#Person` service (from Mantle Business Artifacts):
```
<service verb="create" noun="Person">
        <in-parameters>
            <auto-parameters entity-name="mantle.party.Party"/>
            <auto-parameters entity-name="mantle.party.Person" include="nonpk"/>
            <parameter name="firstName" required="true"/>
            <parameter name="lastName" required="true"/>
            <parameter name="roleTypeId"/>
        </in-parameters>
        <out-parameters><parameter name="partyId"/></out-parameters>
        <actions>
            <service-call name="create#mantle.party.Party" in-map="context + [partyTypeEnumId:'PtyPerson']" out-map="context"/>
            <service-call name="create#mantle.party.Person" in-map="context"/>
            <if condition="roleTypeId"><service-call name="create#mantle.party.PartyRole" in-map="[partyId:partyId, roleTypeId:roleTypeId]"/></if>
        </actions>
</service>
```

The only attribute that is required for a service is **verb**, though use of a **noun** is generally recommended. The **type** attribute is commonly used, but defaults to "inline" just like the service above which has an actions element containing the service implementation. For other types of services, i.e. other ways of implementing a service, the **location** and optional **method** attributes are used to specify what to run.

The example above has in-parameters including individual parameter elements and an auto-parameters element to pull in all non-PK fields on the `mantle.party.Person` entity. It also has one out-parameter, a *partyId* that in this case is either generated if no partyId is passed as an input parameter or the passed in value is simply passed through.

The actions element has the implementation of the service, containing a XML Actions script. In this case it calls a couple of services, and then conditionally calls a third if a *roleTypeId* is passed in. Note that there is no explicit setting of the *partyId* output parameter (in the result Map) as the *Service Facade* automatically picks up the context value for each declared output parameter after the service implementation is run to populate the output/results Map.

These are the attributes available on the service element:

-   **verb**: This can be any verb, and will often be one of: create, update, store, delete, or find. The full name of the service will be: "${path}.${verb}\#${noun}". The verb is required and the noun is optional so if there is no noun the service name will be just the verb.
-   **noun**: For entity-auto services this should be a valid entity name. In many other cases an entity name is the best way to describe what is being acted on, but this can really be anything.
-   **type**: The service type specifies how the service is implemented. The default available options include: inline, entity-auto, script, java, interface, remote-xml-rpc, remote-json-rpc, and camel. Additional types can be added by implementing the `org.moqui.impl.service.ServiceRunner` interface and adding a *service-facade.service-type* element in the Moqui Conf XML file. The default value is inline meaning the service implementation is under the *service.actions* element.
-   **location**: The location of the service. For scripts this is the Resource Facade location of the file. For Java class methods this is the full class name. For remote services this is the URL of the remote service. Instead of an actual location can also refer to a pre-defined location from the *service-facade.service-location* element in the Moqui Conf XML file. This is especially useful for remote service URLs.
-   **method**: The method within the location, if applicable to the service type.
-   **authenticate**: If not set to false (is true by default) a user much be logged in to run this service. If the service is running in an *ExecutionContext* with a user logged in that will qualify. If not then either a "authUserAccount" parameter or the "authUsername" and "authPassword" parameters must be specified and must contain valid values for a user of the system. An "authTenantId" parameter may also be specified to authenticate the user in a specific tenant instance. If specified will be used to run the service with that as the context tenant. Can also be set to anonymous-all or anonymous-view and not only will authentication not be required, but this service will run as if authorized (using the _NA_ UserAccount) for all actions or for view-only.
-   **allow-remote**: Defaults to false meaning this service cannot be called through remote interfaces such as JSON-RPC and XML-RPC. If set to true it can be. Before settings to true make sure the service is adequately secured (for authentication and authorization).
-   **validate**: Defaults to true. Set to false to not validate input parameters, and not automatically remove unspecified parameters.
-   **transaction**:

    -   ignore: Don't do anything with transactions (if one is in place use it, if no transaction in place don't begin one).
    -   use-or-begin: Use active transaction or if no active transaction begin one. This is the default.
    -   force-new: Always begin a new transaction, pausing/resuming the active transaction if there is one.
    -   cache: Like use-or-begin but with a write-through per-transaction cache in place (works even if active TX is in place). See notes and warnings in the JavaDoc comments of the *TransactionCache* class for details.
    -   force-cache: Like force-new with a transaction cache in place like the cache option.

-   **transaction-timeout**: The timeout for the transaction, in seconds. This value is only used if this service begins a transaction (force-new, force-cache, or use-or-begin or cache and there is no other transaction already in place).
-   **semaphore**: Intended for use in long-running services (usually scheduled). This uses a record in the database to lock the service so that only one instance of it can run against a given database at any given time. Options include none (default), fail, and wait.
-   **semaphore-timeout**: When waiting how long before timing out, in seconds. Defaults to 120s.
-   **semaphore-sleep**: When waiting how long to sleep between checking the semaphore, in seconds. Defaults to 5s.
-   **semaphore-ignore**: Ignore existing semaphores after this time, in seconds. Defaults to 3600s (1 hour).

The input and output of a service are each a Map with name/value entries. Input parameters are specified with the in-parameters element, and output parameters with the out-parameters element. Under these elements use the parameter element to define a single parameter, and the auto-parameters element to automatically define parameters based on primary key (pk), non-primary key (nonpk) or all fields of an entity.

An individual parameter element has attributes to define it including:

-   **name**: The name of the parameter, matches against the key of an entry in the parameters Map passed into or returned from the service.
-   **type**: The type of the attribute, a full Java class name or one of the common Java API classes (including String, Timestamp, Time, Date, Integer, Long, Float, Double, BigDecimal, BigInteger, Boolean, Object, Blob, Clob, Collection, List, Map, Set, Node).
-   **required**: Defaults to false, set to true for the parameter to be required. Can also set to disabled to behave the same as if the parameter did not exist, useful when overriding a previously defined parameter.
-   **allow-html**: Applies only to String fields. Only checked for incoming parameters (meant for validating input from users, other systems, etc). Defaults to none meaning no HTML is allowed (will result in an error message). If some HTML is desired then use safe which will follow the rules in the antisamy-esapi.xml file. This should be safe for both internal and public users. In rare cases when users are trusted or it is not a sensitive field the any option may be used to not check the HTML content at all.
-   **format**: Used only when the parameter is passed in as a String but the type is something other than String to convert to that type. For date/time uses standard Java SimpleDateFormat strings.
-   **default**: The field or expression specified will be used for the parameter if no value is passed in (only used if required=false). Like default-value but is a field name or expression instead of a text value. If both this and default-value are specified this will be evaluated first and only if empty will default-value be used.
-   **default-value**: The text value specified will be used for the parameter if no value is passed in (only used if required=false). If both this and default are specified default will be evaluated first and this will only be used if default evaluates to an empty value.
-   **entity-name**: Optional name of an entity with a field that this parameter is associated with.
-   **field-name**: Optional field name within the named entity that this parameter is associated with. Most useful for form fields defined automatically from the service parameter. This is automatically populated when parameters are defined automatically with the auto-parameters element.

For parameter object types that contain other objects (such as List, Map, and Node) the parameter element can be nested to specify what to expect (and if applicable, validate) within the parameter object.

In addition to the **required** attribute, validations can be specified for each parameter with these sub-elements:

-  *matches*: Validate the current parameter against the regular expression specified in the **regexp** attribute.
-  *number-range*: Validate the number within the **min** and **max** range.
-  *number-integer*: Validate that the parameter is an integer.
-  *number-decimal*: Validate that the parameter is a decimal number.
-  *text-length*: Validate that the length of the text is within the **min** and **max** range.
-  *text-email*: Validate that the text is a valid email address.
-   *text-url*: Validate that the text is a valid URL.
-   *text-letters*: Validate that the text contains only letters.
-   *text-digits*: Validate that the text contains only digits.
-  *time-range*: Validate that the date/time is within the **before** and **after** range, using the specified **format**.
-   *credit-card*: Validate that the text is a valid credit card number using Luhn MOD-10 and if specified for the given card **types**.

Validation elements can be combined using the *val-or* and *val-and* elements, or negated using the *val-not* element.

When a XML Form field is based on a service parameter with validations certain validations are automatically validated in the browser with JavaScript, including **required**, *matches*, *number-integer*, *number-decimal*, *text-email*, *text-url*, and *text-digits*.

Now that your service is defined, essentially configuring the behavior of the Service Facade when the service is called, it is time to implement it.
