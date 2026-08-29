# Entity ECA Rules

Entity ECA (EECA) rules can be used to trigger actions to run when data is modified or searched. It is useful for maintaining entity fields (database columns) that are based on other entity fields or for updating data in a separate system based on data in this system. EECA rules should not generally be used for triggering business processes because the rules are applied too widely. Service ECA rules are a better tool for triggering processes.

For example here is an EECA rule from the *Work.eecas.xml* file in Mantle Business Artifacts that calls a service to update the total time worked on a task (WorkEffort) when a TimeEntry is created, updated, or deleted:
```
<eeca entity="mantle.work.time.TimeEntry" on-create="true" on-update="true" on-delete="true" get-entire-entity="true">
        <condition><expression>workEffortId</expression></condition>
        <actions><service-call name="mantle.work.TaskServices.update#TaskFromTime" in-map="context"/></actions>
</eeca>
```

An ECA (event-condition-action) rule is a specialized type of rule to conditionally run actions based on events. For Entity ECA rules the events are the various find and modify operations you can do with a record. Set any of these attributes (of the eeca element) to true to trigger the EECA rule on the operation: **on-create**, **on-update**, **on-delete**, **on-find-one**, **on-find-list**, **on-find-iterator**, **on-find-count**.

By default the EECA rule will run after the entity operation. To have it run before set the **run-before** attribute to true. There is also a **run-on-error** attribute which defaults to false and if set to true the EECA rule will be triggered even if there is an error in the entity operation.

When the actions run the context will be whatever context the service was run in, plus the entity field values passed into the operation for convenience in using the values. There are also special context fields added:

-   entityValue: A *Map* with the field values passed into the entity operation. This may not include all field values that are populated in the database for the record. To fill in the field values that are not passed in from the database record set the eeca.**get-entire-entity** attribute to true.
-   originalValue: If the *eeca*.**get-original-value** attribute is set to true and the EECA rule runs before the entity operation (**run-before=**true) this will be an EntityValue object representing the original (current) value in the database.
-   eecaOperation: A String representing the operation that triggered the EECA rule, basically the **on-\*** attribute name without the "on-".

The condition element is the same condition as used in XML Actions and may contain expression and compare elements, combined as needed with or, and, and not elements.

The actions element is the same as actions elements in service definitions, screens, forms, etc. It contains a XML Actions script. See the **Overview of XML Actions** section for more information.
