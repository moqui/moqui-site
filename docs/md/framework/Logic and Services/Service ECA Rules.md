# Service ECA Rules

An ECA (event-condition-action) rule is a specialized type of rule to conditionally run actions based on events. For Service ECA (SECA) rules the events are the various phases of executing a service, and these are triggered for all service calls.

*Service ECAs* are meant for triggering business processes and for extending the functionality of existing services that you don't want to, or can't, modify. Service ECAs should NOT generally be used for maintenance of data derived from other entities, Entity ECA rules are a much better tool for that.

Here is an example of an *SECA* rule from the *AccountingInvoice.secas.xml* file in Mantle Business Artifacts that calls a service to create invoices for orders when a shipment is packed:
```
<seca id="ShipmentOutgoingPackedCreateInvoices" service="update#mantle.shipment.Shipment" when="post-service">
    <condition><expression>statusChanged &amp;&amp; statusId == 'ShipPacked' &amp;&amp; !(oldStatusId in ['ShipShipped', 'ShipDelivered'])</expression></condition>
    <actions>
        <entity-find-one entity-name="mantle.shipment.Shipment" value-field="shipment"/>
        <set field="shipmentTypeEnum" from="shipment.'ShipmentType#moqui.basic.Enumeration'"/>
        <if condition="shipmentTypeEnum?.enumId == 'ShpTpOutgoing' || shipmentTypeEnum?.parentEnumId == 'ShpTpOutgoing'">
            <service-call name="mantle.account.InvoiceServices.create#SalesShipmentInvoices" in-map="[shipmentId:shipmentId]"/>
       </if>
    </actions>
</seca>
```

The required attributes on the *seca* element are **service** with the service name, and **when** which is the phase within the service call. These two attributes together make up the event that triggers the SECA rule. There is also a **run-on-error** attribute which defaults to false and if set to true the SECA rule will be triggered even if there is an error in the service call. Set **name-is-pattern** to true if **service** is a regular expression to match multiple service names. An optional **id** is recommended; another SECA rule with the same id overrides a previously found rule (use empty actions to disable one).

The options for the **when** attribute include:

-   *pre-validate*: Runs before input parameters are validated; useful for adding or modifying parameters before validation and data type conversion
-   *pre-auth*: Runs before authentication and authorization checks, but after the authUsername and authPassword parameters are used and the specified user is logged in; useful for any custom behavior related to authc or authz
-   *pre-service*: Runs before the service itself is run; best place for general things to be done before running the service
-   *post-service*: Runs just after the service is run; best place for general things to be done after the service is run and independent of the transaction
-  *post-commit*: Runs just after the commit would be done, whether it is actually done or not (depending on service settings and existing TX in place, etc); to run something on the actual commit use the tx-commit option
-   *tx-commit*: Runs when the transaction the service is running in is successfully committed. Gets its data after the run of the service so will have the output/results of the service run as well as the input parameters.
-   *tx-rollback*: Runs when the transaction the service is running in is rolled back. Gets its data after the run of the service so will have the output/results of the service run as well as the input parameters.

When the actions run the context will be whatever context the service was run in, plus the input parameters of the service for convenience in using them. If **when** is before the service itself is run there will be a context field called parameters with the input parameters Map in it that you can modify as needed in the ECA actions. If **when** is after the service itself the parameters field will contain the input parameters and a results field will contain the output parameters (results) that also may be modified.

The condition element is the same condition as used in XML Actions and may contain expression and compare elements, combined as needed with or, and, and not elements.

The actions element is the same as actions elements in service definitions, screens, forms, etc. It contains an XML Actions script. See the [Overview of XML Actions](/docs/framework/Logic+and+Services/Overview+of+XML+Actions) section for more information.
