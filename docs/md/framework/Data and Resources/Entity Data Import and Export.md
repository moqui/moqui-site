# Entity Data Import and Export

[TOC levels=2-3]

## Loading Entity XML, CSV, and JSON

Entity records can be imported from XML, CSV, and JSON files using the *EntityDataLoader*. This can be done through the Entity Facade API using the *ec.entity*.**makeDataLoader**() method to get an object that implements the interface and using its methods to specify which data to load and then load it (using the **load**() method), get an EntityList of the records (using the **list**() method), or validate the data against the database (using the **check**() method).

There are a few options for specifying which data to load. You can specify one or more locations using the **location**(String location) and **locationList**(List&lt;String&gt; locationList) methods. You can use text directly with the **xmlText**(String xmlText), **csvText**(String csvText), and **jsonText**(String jsonText) methods. You can also load from component data directories and the *entity-facade.load-data* elements in the *Moqui Conf XML* file by specifying the types of data to load (only the files with a matching type will be loaded) using the **dataTypes**(Set&lt;String&gt; dataTypes) method.

To set the transaction timeout to something different from the default, usually larger to handle processing large files, use the **transactionTimeout**(int tt) method. If you expect mostly inserts you can pass true to the **useTryInsert**(boolean useTryInsert) method to improve performance by doing an insert without a query to see if the record exists and then if the insert fails with an error try an update.

To help with foreign keys when records are out of order, but you know all will eventually be loaded, pass true to the **dummyFks**(boolean dummyFks) method and it will create empty records for foreign keys with no existing record. When the real record for the FK is loaded it will simply update the empty dummy record. To disable Entity ECA rules as the data is loaded pass true to the **disableEntityEca**(boolean disableEeca) method.

For CSV files you can specify which characters to use when parsing the file(s) with **csvDelimiter**(char delimiter) (defaults to ','), **csvCommentStart**(char commentStart) (defaults to '#'), and **csvQuoteChar**(char quoteChar) (defaults to '"').

Note that all of these methods on the EntityDataLoader return a self reference so you can chain calls, i.e. it is a DSL style API. For example:
```
ec.entity.makeDataLoader().dataTypes(['seed', 'demo']).load()
```
In addition to directly using the API you can load data using the Tools application **Entity** → **Import** screen (`http://localhost:8080/qapps/tools/Entity/DataImport`). You can also load data using the command line with the executable WAR file using the `load` argument. Here are the command line arguments available for the data loader:

```
load -------- Run data loader
    types=<type>[,<type>] ------- Data types to load (can be anything, common are: seed, seed-initial, install, demo, ...)
    components=<name>[,<name>] -- Component names to load for data types; if none specified loads from all
    location=<location> --------- Location of data file to load
    timeout=<seconds> ----------- Transaction timeout for each file, defaults to 600 seconds (10 minutes)
    no-fk-create ---------------- Don't create foreign-keys, for empty database to avoid referential integrity errors
    dummy-fks ------------------- Use dummy foreign-keys to avoid referential integrity errors
    use-try-insert -------------- Try insert and update on error instead of checking for record first
    disable-eeca ---------------- Disable Entity ECA rules
    disable-audit-log ----------- Disable Entity Audit Log
    disable-data-feed ----------- Disable Entity DataFeed
    raw ------------------------- For raw data load to an empty database; short for no-fk-create, use-try-insert, disable-eeca, disable-audit-log, disable-data-feed
```

If no types or location argument is used, all known data files of all types will be loaded. For example:
```
$ java -jar moqui.war load types=seed,demo
```
The entity data XML file must have the entity-facade-xml root element which has a **type** attribute to specify the type of data in the file, which is compared with the specified types (if loading by specifying types) and only loaded if the type is in the set or if all types are loaded. Under that root element each element name is an entity or service name. For entities each attribute is a field name and for services each attribute is an input parameter.

Here is an example of an entity data XML file:
```
<entity-facade-xml type="seed">
    <moqui.basic.LocalizedMessage original="Example" locale="es" localized="Ejemplo"/>
    <moqui.basic.LocalizedMessage original="Example" locale="zh" localized="样例"/>
</entity-facade-xml>
```

JSON files are a List of Maps. Each object has an **_entity** entry (entity or service name, or short-alias) and field or parameter values. An object with **_dataType** sets the type for following records, matching the XML **type** attribute.

Here is an example CSV file that calls a service (the same pattern applies for loading entity data):

```
# first line is ${entityName or serviceName},${dataType}
moqui.example.ExampleServices.create#Example, demo
# second line is list of field names
exampleTypeEnumId, statusId, exampleName, exampleSize, exampleDate
# each additional line has values for those fields
EXT_MADE_UP, EXST_IN_DESIGN, Test Example Name 3, 13, 2014-03-03 15:00:00
```

## Writing Entity XML

The easiest way to export entity data to an XML file is to use the *EntityDataWriter*, which you can get with *ec.entity*.**makeDataWriter**(). Through this interface you can specify the names of entities to export from and various other options, then it does the query and exports to a file (with the int **file**(String filename) method), a directory with one file per entity (with the int **directory**(String path) method), or to a Writer object (with the int **writer**(Writer writer) method). All of these methods return an int with the number of records that were written.

The methods for specifying options return a self reference to enable chaining calls. These are the methods for the query and export options:

-   **entityName**(String entityName): Specify the name of an entity to query and export. Data is queried and exported from entities in the order they are added by calling this or **entityNames**() multiple times.
-   **entityNames**(List&lt;String&gt; entityNames): A List of entity names to query and export. Data is queried and exported from entities in the order they are specified in this list and other calls to this or **entityName**().
-   **dependentRecords**(boolean dependents): If true export dependent records of each record. This dramatically slows down the export so only use it on smaller data sets. See the **Dependent Entities** section for details about what would be included.
-   **filterMap**(Map&lt;String, Object&gt; filterMap): A Map of field name, value pairs to filter the results by. Each name/value is only used on entities that have a field matching the name.
-   **orderBy**(List&lt;String&gt; orderByList): Field names to order (sort) the results by. Each name only used on entities with a field matching the name. May be called multiple times. Each entry may be a comma-separated list of field names.
-   **fromDate**(Timestamp fromDate), **thruDate**(Timestamp thruDate): The from and thru dates to filter the records by, compared with the **lastUpdatedStamp** field which the Entity Facade automatically adds to each entity (unless turned off in the entity definition).

Here is an example of an export of all OrderHeader records within a time range plus their dependents:
```
ec.entity.makeDataWriter().entityName("mantle.order.OrderHeader").dependentRecords(true).orderBy(["orderId"]).fromDate(lastExportDate).thruDate(ec.user.nowTimestamp).file("/tmp/TestOrderExport.xml")
```
Another way to export entity records is to do a query and get an EntityList or EntityListIterator object and call the int **writeXmlText**(Writer writer, String prefix, int dependentLevels) method on it. This method writes XML to the writer, optionally adding the prefix to the beginning of each element and including dependents that many levels deep (zero for no dependents).

Similar to the entity data import UI you can export data using the Tools application **Entity** → **Export** screen (`http://localhost:8080/qapps/tools/Entity/DataExport`).

## Views and Forms for Easy View and Export

A number of tools come together to make it very easy to view and export database data that comes from a number of different tables. We have explored the options for static (XML), dynamic, and database defined entities. In the **User Interface** chapter there is detail about XML Forms, and in particular list forms.

When a form-list has **dynamic**=true and a ${} string expansion in the auto-fields-entity.**entity-name** attribute then it will be expanded on the fly as the screen is rendered, meaning a single form can be used to generate tabular HTML or CSV output for any entity given an entity name as a screen parameter.

To make things more interesting results viewed can be filtered generically using a dynamic form-single with an auto-fields-entity element to generate a search form based on the entity, and an entity-find with search-form-inputs to do the query based on the entity name parameter and the search parameters from the search form.

Below is an example of these features along with a transition (*DbView.csv*) to export a CSV file. Don’t worry too much about all the details for screens, transitions, forms, and rendering options, they are covered in detail in the **User Interface** section. This screen definition is an excerpt from the *ViewDbView.xml* screen in the tools component that comes by default with Moqui Framework:

```
<screen>
        <parameter name="dbViewEntityName" required="true"/>
        <transition name="filter">
             <default-response url="."/>
        </transition>
        <transition name="DbView.csv">
        <default-response url="."><parameter name="renderMode" value="csv"/>
            <parameter name="pageNoLimit" value="true"/><parameter name="lastStandalone" value="true"/></default-response>
        </transition>
        <actions>
            <entity-find entity-name="${dbViewEntityName}" list="dbViewList">
                <search-form-inputs/>
            </entity-find>
        </actions>
       <widgets>
              <container>
                  <link url="edit" text="Edit ${dbViewEntityName}"/>
                  <link url="DbView.csv" text="Get as CSV"/>
              </container>
              <label text="Data View for: ${dbViewEntityName}" type="h2"/>
              <container-dialog id="FilterViewDialog" button-text="Filter ${ec.entity.getEntityDefinition(dbViewEntityName).getPrettyName(null, null)}">
                  <form-single name="FilterDbView" transition="filter" dynamic="true">
                      <auto-fields-entity entity-name="${dbViewEntityName}" field-type="find"/>
                      <field name="dbViewEntityName"><default-field><hidden/></default-field></field>
                      <field name="submitButton"><default-field title="Find"><submit/></default-field></field>
                  </form-single>
              </container-dialog>
              <form-list name="ViewList" list="dbViewList" dynamic="true">
                  <auto-fields-entity entity-name="${dbViewEntityName}" field-type="display"/>
              </form-list>
    </widgets>
</screen>
```
While this screen is designed to be used by a user it can also be rendered outside a web or other UI context to generate CSV output to send to a file or other location. If you were to just write a screen for that it would be far simpler, basically just the parameter element, the single entity-find action, and the simple form-list definition. The transitions and the search form would not be needed.

The code to do this through the screen renderer would look something like:
```
ec.context.putAll([pageNoLimit:"true", lastStandalone:"true", dbViewEntityName: "moqui.example.ExampleStatusDetail"])
String csvOutput = ec.screen.makeRender().rootScreen("component://tools/screen/Tools/DataView/ViewDbView.xml").renderMode("csv").render()
```
