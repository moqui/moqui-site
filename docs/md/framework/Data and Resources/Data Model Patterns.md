# Data Model Patterns
There are various useful data model patterns that Moqui Framework has conventions and functionality to help support. These data model patterns are also used extensively in the Moqui and Mantle data models.
[TOC levels=2-3]

## Master Entities

A Master Entity is one whose records exist independent of other entities, and generally has a single field primary key. Examples of this include the `moqui.example.Example`, `moqui.security.UserAccount`, `mantle.party.Party`, `mantle.product.Product`, and `mantle.order.OrderHeader` entities.

To set a primary sequenced ID, which is the sequenced value for the primary key of a master entity, use the *EntityValue*.**setSequencedIdPrimary**() method. You can also manually set the primary key field to any value, as long as it is unique.

## Detail Entities

A Detail Entity adds detail to a Master Entity for fields that have a one-to-many relationship with the Master. The primary key is usually two fields and one of the fields is the single primary key field of the master entity. The second field is a special sort of sequenced ID that instead of having an absolute sequence value its value is in the context of the master entity’s primary key.

An example of a detail entity is *ExampleItem*, which is a detail to the master entity *Example*. *ExampleItem* has two primary keys: **exampleId** (the primary key field of the master entity) and **exampleItemSeqId** which is a sub-sequence to distinguish the detail records within the context of a master record.

To populate the secondary sequenced ID first set the master’s primary key (**exampleId** for *ExampleItem*), then use the *EntityValue*.**setSequencedIdSecondary**() method to automatically populate it (for *ExampleItem* the **exampleItemSeqId**).

A single master entity can have multiple detail entities associated with it to structure distinct data as needed.

## Join Entities

A Join Entity is used to associate Master Entities, usually two. A Join Entity is a physical representation of a many-to-many relationship between entities in a logical model.

A join entity is useful for tracking associated records among the master entities, and for any data that is associated with both master entities as opposed to just one of them. For example if you want to specify a sequence number for one master entity record in the context of a record of the other master entity, the sequence number field should go on the join entity and not on either of the master entities.

The join entity may have a single generated primary key, or a natural composite primary key consisting of the single primary key field of each of the master entities. If a relationship between two entities varies over time use the **Effective Date** pattern on the join entity with a **fromDate** field with a corresponding **thruDate** field that is not part of the join entity’s primary key.

One example of this is the *ExampleFeatureAppl* entity which joins the *Example* and *ExampleFeature* master entities. The *ExampleFeatureAppl* entity has three primary key fields: **exampleId** (the PK of the *Example* entity), **exampleFeatureId** (the PK of the *ExampleFeature* entity), and a **fromDate**. It also has a **thruDate** field that is not a primary key field to accompany the **fromDate** PK field.

To better describe the relationship between an *Example* and an *ExampleFeature*, the *ExampleFeatureAppl* entity also has a **sequenceNum** field for ordering features within an example, and an **exampleFeatureApplEnumId** field to describe how the feature applies to the example (Required, Desired, or Not Allowed).

To see the actual entity definition and seed data for the *ExampleFeatureAppl* entity see the *ExampleEntities.xml* file (in the **example** component).

### Query Patterns

Querying a join entity usually involves starting with one of the master entities and finding the related master entities using records for the join entity by specifying the ID of the known master entity and finding the ID(s) of related master entities.

If the Effective Date pattern is used (with fromDate and thruDate fields) then it should always be filtered by an anchor timestamp, which generally defaults to the current date/time. The general pattern for filtering is:

* **fromDate** <= anchor timestamp OR **fromDate** is null (when not a primary key field)
* **thruDate** >= anchor timestamp OR **thruDate** is null

In some cases the configuration and logic calls for a single join record to honor. An example of this is that multiple price records may be configured for a product but only one is valid at any point in time. The standard query pattern for this is to use the applicable join entity record with the **most recent fromDate** after applying all filters (including Effective Date conditions above). In the price example this allows for a long term price with a fromDate far in the past and no thruDate along with a temporary override that has a more recent fromDate along with a thruDate when the temporary price is no longer active. To get this effect in a query simply apply the Effective Date conditions above and order the results by fromDate descending (**-fromDate**).

## Dependent Entities

A few parts of the API and Tools app support the concept of "dependent" entities. Dependent entities can be found for any entity, but the concept is most useful for dependents of Master Entities. The general idea is that things like the items of an order (`mantle.order.OrderItem`) are dependent on the header (`mantle.order.OrderHeader`). It is useful to do operations such as data export including the master entity and all of its dependents.

Conceptually this is pretty simple, but the implementation is more complex because the information we have to work with for this is the entity relationships. The general idea is that each type one relationship points from a dependent entity to its master, and by this definition many dependent entities have more than one master entity and an entity can be both a dependent and a master entity so what an entity is depends on how you are treating it. When defining entities there is an automatic reverse type relationship for each type one relationship, and while it is generally a type many reverse relationship if the two entities have the same PK field(s) then it is a type one automatic reverse relationship.

For example, *OrderItem* has a type one relationship to *OrderHeader* so there is an automatic reverse relationship of type many from *OrderHeader* to *OrderItem*. This establishes *OrderItem* as a dependent of *OrderHeader*.

When getting dependents for an entity the method (which is part of the internal Entity Facade implementation: *EntityDefinition*.**getDependentsTree**()) runs recursively to get the dependents of dependents as well. The general idea is that for entities like *OrderHeader* you can get all records that define the order.

## Enumerations

An *Enumeration* is simply a pre-configured set of possible values. Enumerations are used to describe single records or relationships between records. An entity may have multiple fields with enumerated values.

The entity in Moqui where all enumerations are stored is named *Enumeration*, and values in it are split by type with a record in the *EnumerationType* entity.

When a field is to have a constrained set of possible enumerated values it should have the suffix "EnumId", like the **exampleTypeEnumId** field on the Example entity. For each field there should also be a relationship element to describe the relationship from the current entity to the Enumeration entity. The **title** attribute on the relationship element should have the same value as the **enumTypeId** that is used for the *Enumeration* records that are possible values for that field. Generally the **title** attribute should be the same as the enum field’s name up to the "EnumId" suffix. For example the relationship title for the **exampleTypeEnumId** field is *ExampleType*.

## Status, Flow, Transition and History

Another useful data concept is tracking the status of a record. Various business concepts have a lifecycle of some sort that is easily tracked with a set of possible status values. The possible status values are tracked using the *StatusItem* entity and exist in sets distinguished by a **statusTypeId** pointing to a record in the *StatusType* entity.

A set of status values are kind of like nodes in a graph and the transitions between those nodes represent possible changes from one status to another. The possible transitions from one status to another are configured using records in the *StatusFlowTransition* entity.

There can be multiple status flows for a set of status items with a given **statusTypeId**, each represented by a *StatusFlow* record. The *StatusItem* records are associated with a *StatusFlow* using *StatusFlowItem* records. For example the *WorkEffort* entity has a **statusFlowId** field to specify which status flow should be used for a project or task.

If an entity has only a single status associated with it the field to track the status can simply be named **statusId**. If an entity needs to have multiple status values then the field name should have a distinguishing prefix and end with "StatusId".

There should be a relationship defined for each status field to tie the current entity to the *StatusItem* entity. Similar to the pattern with the *Enumeration* entity, the **title** attribute on the relationship element should match the **statusTypeId** on each *StatusItem* record.

The audit log feature of the Entity Facade is the easiest way to keep a history of status changes including who made the change, when it was made, and the old and new status values. To turn this on just set the **enable-audit-log** attribute to true on the *entity.field* element. With this the field definition would look something like:
```
<field name="statusId" type="id" enable-audit-log="true"/>
```

## Units of Measure

A unit of measure is a standardized or custom unit for measures such as length, weight, temperature, data size, and even currency. These are the types of UOM. A `moqui.basic.Uom` record, identified by **uomId**, has type (**uomTypeEnumId**), **description**, and **abbreviation** fields. The out-of-the-box data for units of measure is in the UnitData.xml file.

Most UOM types have a conversion between different units of the same type. These conversions are modeled in the *UomConversion* entity. For example there are 1000 meters in a kilometer, and that is recorded this way:
```
<moqui.basic.UomConversion uomConversionId="LEN_km_m" uomId="LEN_km" toUomId="LEN_m" conversionFactor="1000"/>
```

The **conversionFactor** is multiplied by the value with the **uomId** unit to get a value in the **toUomId** unit. You can also divide to go in the other direction. For example 1km = 1000m so a 1 value with the LEN_km unit is multiplied by the **conversionFactor** of 1000 to get a value of 1000 for the LEN_m unit.

There is also a **conversionOffset** field for cases such as Celsius and Fahrenheit temperatures where a value must be added (or subtracted) to go from one unit to the other. The **conversionFactor** is multiplied first, then the **conversionOffset** is added to the result. When converting in the reverse direction the **conversionOffset** is subtracted first, then the result is divided by the **conversionFactor**.

Some UOM types, such as currency, have conversion factors that change over time. To handle this the *UomConversion* entity has optional effective date (**fromDate**, **thruDate**) fields.

## Geographic Boundaries and Points

A geographic boundary can be a political division, business region, or any other geographic area. Each `moqui.basic.Geo` record, identified by a **geoId**, has a type (**geoTypeEnumId**) such as city, country, or sales region. Each *Geo* has a name (**geoName**) and may have 2 letter (**geoCodeAlpha2**), 3 letter (**geoCodeAlpha3**), and numeric (**geoCodeNumeric**) codes following the ISO 3166 pattern for country code (see the *GeoCountryData.xml* file for the country data that comes with Moqui).

The *Geo* entity also has a **wellKnownText** field for machine-readable detail about the geometry of the geographic boundary. It is meant to contain text following the ISO/IEC 13249-3:2011 specification which is supported by various databases and tools (including Java libraries). For a good introduction to WKT see:

[https://en.wikipedia.org/wiki/Well-known_text](https://en.wikipedia.org/wiki/Well-known_text)

Use the *GeoAssoc* entity to associate *Geo* records. This has different types (**geoAssocTypeEnumId**) and can be used for regions of larger geographic boundaries (GAT_REGIONS; like cities within states, states within countries), for *Geo* records that are more general groups to associate them with the *Geo* records in the group (GAT_GROUP_MEMBER; like the lower 48 states in the USA), or other types you might define. The **geoId** field should point to the group or larger area, and the **toGeoId** to the group member or region within the area. See the *GeoUsaData.xml* file for examples of both.

A *GeoPoint* is a specific geographic point, i.e. a point on the Earth’s surface. It has **latitude**, **longitude**, and **elevation** fields and a **elevationUomId** field to specify the unit for the **elevation** (such as feet, which is LEN_ft). There is also a **dataSourceId** to specify where the data came from and an **information** field for general text about the point.
