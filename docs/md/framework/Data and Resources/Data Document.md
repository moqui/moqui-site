# Data Document

[TOC levels=2-4]

## Example

A Data Document is assembled from database records into a JSON document or a Java nested Map/List representation of the document.

Below is an example *Data Document* instance and the *DataDocument*\* records that define it. This example a selection from the HiveMind PM project, which is based on Moqui and Mantle. The document is for a project, which is a type of *WorkEffort*.
```
{
    "_index": "hivemind",
    "_type": "HmProject",
    "_id": "HM",
    "_timestamp": "2013-12-27T00:46:07",
    "WorkEffort": 
    {
        "workEffortId": "HM",
        "name": "HiveMind PM Build Out",
        "workEffortTypeEnumId": "WetProject"
    },
    "StatusItem": { "status": "In Progress" },
    WorkEffortType": { "type": "Project" },
    "Party": [
          {
          "Person": { "firstName": "John", "lastName": "Doe" },
          "RoleType": { "role": "Person - Manager" },
          "partyId": "EX_JOHN_DOE"
          },
          {
          "Person": { "firstName": "Joe", "lastName": "Developer" },
          "RoleType": { "role": "Person - Worker" },
          "partyId": "ORG_BIZI_JD"
          }
    ]
}
```

These are the database records defining the *Data Document*, in the format of records in an *Entity Facade XML* file:

```
<moqui.entity.document.DataDocument dataDocumentId="HmProject" indexName="hivemind" documentName="Project" primaryEntityName="mantle.work.effort.WorkEffort" documentTitle="${name}"/>

<moqui.entity.document.DataDocumentField dataDocumentId="HmProject" fieldPath="workEffortId"/>

<moqui.entity.document.DataDocumentField dataDocumentId="HmProject"  fieldPath="workEffortName" fieldNameAlias="name"/>

<!-- this is aliased so we can have a condition on it -->

<moqui.entity.document.DataDocumentField dataDocumentId="HmProject"  fieldPath="workEffortTypeEnumId"/>

<moqui.entity.document.DataDocumentField dataDocumentId="HmProject"  fieldPath="WorkEffort#moqui.basic.StatusItem:description"
fieldNameAlias="status"/>

<moqui.entity.document.DataDocumentField dataDocumentId="HmProject" fieldPath="mantle.work.effort.WorkEffortParty:partyId"/>

<moqui.entity.document.DataDocumentField dataDocumentId="HmProject" fieldPath="mantle.work.effort.WorkEffortParty:mantle.party.RoleType:description"
fieldNameAlias="role"/>

<moqui.entity.document.DataDocumentRelAlias dataDocumentId="HmProject" relationshipName="mantle.work.effort.WorkEffort" documentAlias="WorkEffort"/>

<moqui.entity.document.DataDocumentRelAlias dataDocumentId="HmProject" relationshipName="WorkEffort#moqui.basic.StatusItem"
documentAlias="StatusItem"/>

<moqui.entity.document.DataDocumentRelAlias dataDocumentId="HmProject" relationshipName="mantle.work.effort.WorkEffortParty" documentAlias="Party"/>

<moqui.entity.document.DataDocumentRelAlias dataDocumentId="HmProject"  relationshipName="mantle.party.RoleType" documentAlias="RoleType"/>

<moqui.entity.document.DataDocumentCondition dataDocumentId="HmProject"  fieldNameAlias="workEffortTypeEnumId" fieldValue="WetProject"/>

<moqui.entity.document.DataDocumentLink dataDocumentId="HmProject"  label="Edit Project"  linkUrl="/apps/hm/Project/EditProject?workEffortId=${workEffortId}"/>
```

## JSON Object

The top level object (the JSON term, Map in Java) of the Data Document instance has 3 fields that identify the document:

-   **\_index**: The index the document should live in, from the *DataDocument*.**indexName** field in the document definition
-   **\_type**: The type of document within the index, and the ID that Moqui Framework uses for the *DataDocument* definition, from the *DataDocument*.**dataDocumentId** field
-   **\_id**: The ID for a particular Data Document instance, based on the primary key of the primary entity as specified in the *DataDocument*.**primaryEntityName** field

The top level also contains a **\_timestamp** field with the date and time the document was generated.

These 4 fields are named the way they are for easy indexing with ElasticSearch, which is the tool used by the Data Search feature which is based on the Data Document feature. These fields, and Data Documents in general, are useful for notifications, integrations, and various things other than just search.

## Definition

A *Data Document* definition is made up of these records:

- *DataDocument*: The main record, identified by a **dataDocumentId** and contains the index name, document name (for display purposes)

    -   **primaryEntityName**: the primary (master) entity for the document that all other entities for document fields relate to and that plain field names belong to
    -   **documentTitle**: For display purposes, especially in search results and such. Note that the **documentTitle** value is expanded using a flattened Map from the Data Document, so names of expanded fields must match document field names (or aliases).

-   *DataDocumentField*: Each record specifies a field for the document.

    -   **fieldPath**: The field name, optionally preceded by a colon-separated list of relationship names from the primary entity to the entity the field is on.
    -   **fieldNameAlias**: Optionally specify a name for the field to use in the document if different from the name of the field on the entity it belongs to. The field name in the document must be unique for the entire document, not just within the entity the field belongs to. This is true whether the entity field name or an alias is used. The reasons for this are: this is the alias used in the query to get the data for the document from the database and to facilitate parametric searching.

- *DataDocumentRelAlias*: Use these records to produce a cleaner document by specifying an alias for relationships in **fieldPath** fields, and for the **primaryEntityName**.
-   *DataDocumentCondition*: These records constrain the query that gets data for the document from the database. In the example above this is used to constrain the query to only get WorkEffort records with the WetProject type so it only includes projects.
-   *DataDocumentLink*: In search results and other user and system interfaces it is useful to have a link to where more information about the document, especially the primary entity in it, is available. Use these records to specify such links. Note that the **linkUrl** value is expanded using a flattened Map from the Data Document, so names of expanded fields must match document field names (or aliases).

In the top level object of the example document there is a *WorkEffort* object for the primary entity in the document. There will always be an object like this in the document and its name will be the name of the primary entity. It will be the literal value of the *DataDocument*.**primaryEntityName** field unless it is aliased in a *DataDocumentRelAlias* record, which is why in this document that named of the object is `WorkEffort` and not `mantle.work.effort.WorkEffort`.

All *DataDocumentField* records with a **fieldPath** with plain field names (no colon-separated relationship prefix) map to fields on the primary entity and will be included in the primary entity’s object in the document.

All document fields with a colon-separated relationship name prefix will result in other entries in the top level document object (Map) with the entry key as the relationship name or the alias for the relationship name if one is configured. The value for that entry will be an object/Map if it is a type one relationship, or an array of objects (in Java a List of Maps) if it is a type many relationship.

The same pattern applies when there is more than one colon-separated relationship name in a **fieldPath**. The object/Map entries will be nested as needed to follow the path to the specified field. An example of this from the *HmProject* document example above is the "*mantle.work.effort.WorkEffortParty:mantle.party.RoleType:description*" **fieldPath** value. Note that the two relationship names are aliased to exclude the package names, and the field is aliased to be role instead of description. The result is this part of the JSON document:
```
    { "Party": [ { "RoleType": { "role": "Person - Manager" } } ] }
```
The JSON syntax for an object (Map) is curly braces ({ }) and for an array (List) is square braces ([ ]). So what we have above is the top-level object with a *Party* entry whose value is an array with an object in it that has a *RoleType* entry whose value is an object with a single entry with the key **role** and the value is from the RoleType.**description** entity field. The reason the **description** field is aliased as **role** is the one described above in the description for the *DataDocumentField*.**fieldNameAlias** field: each field in a Data Document must have a unique name across the entire document.

## Generate

There are a few ways to generate a Data Document from data in a database. The most generally useful approach is the Data Feed described below, but you can also get it through an API call that looks like this:
```
List<Map> docMapList = ec.entity.getDataDocuments(dataDocumentId, condition, fromUpdateStamp, thruUpdatedStamp)
```

In the List returned each Map represents a Data Document. The *condition*, *fromUpdatedStamp* and *thruUpdatedStamp* parameters can all be null, but if specified are used as additional constraints when querying the database. The condition should use the field alias names for the fields in the document. To see if any part of the document has changed in a certain time range the UpdatedStamp parameters are used to look for any record in any of the entities with the automatically added **lastUpdatedStamp** field in the from/thru range.

The Map for a Data Document is structured the same way as the example JSON document above. The *ElasticSearch API* supports this Map form of a document, but in some cases you will want it as a JSON String. To create a JSON String from the Map in Groovy use a simple statement like this:
```
String docString = groovy.json.JsonOutput.toJson(docMap)
```
If you want a more friendly human-readable version of the JSON String do this:
```
String prettyDocString = groovy.json.JsonOutput.prettyPrint(docString)
```
To go the other way (get a Map representation from a JSON String) use a statement like this:
```
Map docMap = (Map) new groovy.json.JsonSlurper().parseText(docString)
```

## Query

A Dynamic View Entity can be created automatically based on a Data Document definition to run queries (finds) on the joined in entities and aliased fields. To do this just use an entity name with the following pattern:
```DataDocument.${dataDocumentId}```

This is one reason to keep dataDocumentId values simple (letters, numbers, underscore; camel cased or underscore separated). For example, in Groovy:
```
EntityList productList = ec.entity.find("DataDocument.MantleProduct").list()
```
This will find all records using a Dynamic View Entity generated from the MantleProduct Data Document (from mantle-udm). The Dynamic View Entity will join in all entities needed for the aliased fields.
