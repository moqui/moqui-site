# Data Model Definition
[TOC levels=2-3]

## Entity Definition XML

Let’s start with a simple entity definition that shows the most common elements. This is an actual entity that is part of Moqui Framework:

```
<entity entity-name="DataSource" package="moqui.basic" cache="true">
     <field name="dataSourceId" type="id" is-pk="true"/>
     <field name="dataSourceTypeEnumId" type="id"/>
     <field name="description" type="text-medium"/>
     <relationship type="one" title="DataSourceType" related="Enumeration">
        <key-map field-name="dataSourceTypeEnumId"/>
     </relationship>
     <seed-data>
         <moqui.basic.EnumerationType description="Data Source Type" enumTypeId="DataSourceType"/>
         <moqui.basic.Enumeration description="Purchased Data" enumId="DST_PURCHASED_DATA" enumTypeId="DataSourceType"/>;
     </seed-data>
</entity>
```
Just like a Java class an entity has a package name and the full name of the entity is the package name plus the entity name, in the format:

${package}.${entity-name}

Based on that pattern the full name of this entity is:

`moqui.basic.DataSource`

This example also has the entity.**cache** attribute set to true, meaning that it will be cached unless the code doing the find says otherwise.

The first field (**dataSourceId**) has the **is-pk** attribute set to true, meaning it is one of the primary key fields on this entity. In this case it is the only primary key field, but any number of fields can have this attribute set to true to make them part of the primary key.

The third field (**description**) is a simple field to hold data. It is not part of the primary key, and it is not a foreign key to another entity.

The field.**type** attribute is used to specify the data type for the field. The default options are defined in the MoquiDefaultConf.xml file with the `database-list.dictionary-type` element. These elements specify the default type settings for each dictionary type and there can be an override to this setting for each database using the `database.database-type` element.

You can use these elements to add your own types in the data type dictionary. Those custom types won’t appear in autocomplete for the field.**type** attribute in your XML editor unless you change the XSD file to add them there as well, but they will still function just fine.

The second field (**dataSourceTypeEnumId**) is a foreign key to the Enumeration entity, as denoted by the relationship element in this entity definition. The two records in under the seed-data element define the EnumerationType to group the Enumeration options, and one of the Enumeration options for the **dataSourceTypeEnumId** field. The records under the seed-data element are loaded with the command-line -load option (or the corresponding API call) along with the seed type.

There is an important pattern here that allows the framework to know which **enumTypeId** to use to filter Enumeration options for a field in automatically generated form fields and such. Notice that the value in the relationship.**title** attribute matches the enumTypeId. In other words, for enumerations anyway, there is a convention that the relationship.**title** value is the type ID to use to filter the list.

This is a pattern used a lot in Moqui and in the Mantle Business Artifacts because the Enumeration entity is used to manage types available for many different entities.

In this example there is a key-map element under the relationship element, but that is only necessary if the field name(s) on this entity does not match the corresponding field name(s) on the related entity. In other words, because the foreign key field is called **dataSourceTypeEnumId** instead of simply **enumId** we need to tell the framework which field to use. It knows which field is the primary key of the related entity (Enumeration in this case), but unless the field names match it does not know which fields on this entity correspond to those fields.

In most cases you can use something more simple without key-map elements like:
```
<relationship type="one" related="Enumeration"/>
```

The seed-data element allows you to define basic data that is necessary for the use of the entity and that is an aspect of defining the data model. These records get loaded into the database along with the entity-facade-xml files where the **type** attribute is set to seed.

With this introduction to the most common elements of an entity definition, lets now look at some of the other elements and attributes available in an entity definition.

-   Other entity attributes
    -   **group-name**: Each datasource available through the Entity Facade is used by putting an entity in the group for that datasource. The value here should match a value on the moqui-conf.entity-facade.datasource.**group-name** attribute in the Moqui Conf XML file. If no value is specified will default to the value of the moqui-conf.entity-facade.**default-group-name** attribute. By default configuration the valid values include transactional (default), analytical, tenantcommon, and nosql.
    -   **sequence-bank-size**: The size of the sequence bank to keep in memory. Each time the in-memory bank runs out the **seqNum** in the SequenceValueItem record will be incremented by this amount.
    -   **sequence-primary-stagger**: The maximum amount to stagger the sequenced ID. If 1 the sequence will be incremented by 1, otherwise the current sequence ID will be incremented by a random value between 1 and staggerMax.
    -   **sequence-secondary-padded-length**: If specified front-pads the secondary sequenced value with zeroes until it is this length. Defaults to 2.
    -   **optimistic-lock**: Set to true to have the Entity Facade compare the **lastUpdatedStamp** field in memory to the one in the database before doing an update on the record. If the timestamps don’t match an error will be generated. Defaults to "false" (no timestamp locking).
    -   **no-update-stamp**: By default the Entity Facade adds a single field (**lastUpdatedStamp**) to each entity for use in optimistic locking and data synchronization. If you do not want it to create that stamp field for this entity then set this to "false".
    -   **cache**: can be set to these values (defaults to false):
        -   true: use cache for finds (code may override this)
        -   false: no cache for finds (code may override this)
        -   never: no cache for finds (code may NOT override this)
    -   **authorize-skip**: can be set to these values (defaults to false):
        -   true: skip all authz checks for this entity
        -   false: do not skip authz checks
        -   create: skip authz checks for create operations
        -   view: skip authz checks for finds or read-only operations
        -   view-create: skip authz checks for find and create ops
-   Other field attributes
    -   **encrypt**: Set to true to encrypt this field in the database. Defaults to false (not encrypted).
    -   **enable-audit-log**: Set to *true* to log all changes to the field along with when it was changed and the user who changes. Set to *update* to log all changes but not the initial value (lighter weight when a field value does not change). The data is stored using the `EntityAuditLog` entity. Defaults to *false* (no audit logging).
    -   **enable-localization**: If set to true gets on this field will be looked up with the `LocalizedEntityField` entity and if there is a matching record the localized value will be returned instead of the original record's value. Defaults to false for performance reasons, only set to true for fields that will have translations.

While some database optimizations must be done in the database itself because so many such features vary between databases, you can declare indexes along with the entity definition using the index element. As an element under the entity element it would look something like this:
```
<index name="EX_NAME_IDX1" unique="true">
    <index-field name="exampleName"/>
</index>
 ```
 ## Entity Extension - XML

An entity can be extended without modifying the XML file where the original is defined. This is especially useful when you want to extend an entity that is part of a different component such as the Mantle Universal Data Model (mantle-udm) or even part of the Moqui Framework and you want to keep your extensions separate.

This is done with the extend-entity element which can mixed in with the entity elements in an entity definition XML file. This element has most of the same attributes and sub-elements as the entity element used to define the original entity. Simply make sure the **entity-name** and **package** match the same attributes on the original entity element and anything else you specify will add to or override the original entity.

Here is an example if a XML snippet to extend the moqui.example.Example entity:
```
<extend-entity entity-name="Example" package="moqui.example">
    <field name="auditedField" type="text-medium" enable-audit-log="true"/>
    <field name="encryptedField" type="text-medium" encrypt="true"/>
</extend-entity>
```
