# Data View

The data view screens are used to define a simple view entity stored in the database (using the DbViewEntity and related entities) and then view the results and export them as a CSV file. These screens are a simple form of ad-hoc report and data export that leverage the concept of master and dependent entities and allow for easy aliasing of fields on a master entity and all directly related dependents with an optional function. More elaborate DB view entities can be defined and viewed/exported from these screens, but the Edit DB View screen only supports a master entity and the entities directly related to it.

Open them at `http://localhost:8080/qapps/tools/DataView`.

NOTE: For reports that need fields more than one relationship hop away, the Data Document screens in the System app (`http://localhost:8080/qapps/system/DataDocument`) are a more flexible replacement. Data View remains useful for simple master-and-direct-dependent views and CSV export.

## Find DB View

The find screen has a form at the top to create a DbViewEntity and then a table with all existing DB view entities and links to Edit or View them.

<img src="/docs/attachment/100211/findDbView2.png"  width="880" height="260" />

## Edit DB View

The screen to edit a DB view entity has a form at the top to change the package the entity is in. Note that view entities defined in DbViewEntity can be used in the Entity Facade just like any other entity or view entity.

Next on the screen is a form to set the master entity, or the main entity in the view that all other entities will be related to. Once this is set the list form below shows all of the fields on that entity and directly related entities. In this screenshot below the master entity is the Example entity and the fields shown are for it and the ExampleType Enumeration, and Example StatusItem. The screen is cut off partway down and if you view the full screen you’ll also see fields further down for the *ExampleContent*, *ExampleFeatureAppl*, and *ExampleItem* entities (which all have a cardinality of many).

The fields selected to include in the view are the Enumeration.**description** and StatusItem.**description** fields, the **exampleId** and **exampleName** from the Example entity (the master entity), and further off screen the ExampleItem.**exampleItemSeqId** field is selected with a count function to get a count of items on the example.

<img src="/docs/attachment/100211/editDbView1.png" width="880" height="600" />

## View DB View

This screen displays the results of querying the defined DB view entity, paginated if needed, and with a Filter button that pops up a form with filter options for the fields on the view entity (using the default auto fields in a form-single). There is a link to go back to the Edit DB View screen, and a link to get the results in a CSV file.

<img src="/docs/attachment/100211/viewDbView.png" width="880" height="200" />

Here is a sample of the CSV export from the same ExampleDbView results as the screenshot:

```
Description,Description2,Example ID,Example Item Seq ID,Example Name
Made Up,In Design,TEST2,1,Test Example Name 2
Made Up,In Design,TEST1,2,Test Example Name 
```
