# Work Effort
[TOC levels=2]

## Work Effort (mantle.work.effort)

The most basic types of WorkEffort task and calendar event. More generally WorkEffort is used for projects, milestones, tasks, manufacturing routing, meetings, calls, travel, and even time off and work availability.

These are specified with the type (**workEffortTypeEnumId**) and purpose (**purposeEnumId**). Types have more automation around them and are more limited, currently including Project, Milestone, Task, Event, Available, and Time Off. The purposes are more flexible, there is a much larger set, and you can add more with Enumeration records of type WorkEffortPurpose.

Work efforts are hierarchical with the **rootWorkEffortId** to identify the root (such as a project) and **parentWorkEffortId** for the immediate parent in the hierarchy. For example with a Project type WorkEffort as the root the top-level tasks are Task type WorkEffort records with the **rootWorkEffortId** pointing to the project and no **parentWorkEffortId**. Sub-tasks have the same **rootWorkEffortId** value and their **parentWorkEffortId** field points to the top-level task.

WorkEffort has all the basic fields needed for a task or event including name (**workEffortName**), **description**, **location**, **infoUrl**, **estimatedStartDate**, **estimatedCompletionDate**, **percentComplete**, and **priority**. For iCal files and similar uses the **workEffortId** isn’t generally a universally unique identifier so there is a **universalId** field for that. For historical tracking it also has **actualStartDate** and **actualCompletionDate** fields.

A work effort may take place in an office, warehouse, or other type of Facility and that is tracked with the **facilityId** field. For additional location and contact information use the WorkEffortContactMech entity to associate contact mechs such a postal addresses, telephone numbers (for conference calls, etc), email addresses, and so on. To keep track of actual communication related to a work effort use the WorkEffortCommEvent entity and associated CommunicationEvent records.

A WorkEffort may be internal, sensitive, or totally public and this is specified with **visibilityEnumId**. The OOTB options for it are General (public access), Work Group (group only access), Restricted (private access), and Top Secret (confidential access).

For some types of efforts such as manufacturing tasks more detailed time allowances and tracking are needed. There are a few decimal number fields for this: **estimatedWorkTime**, **estimatedSetupTime**, **remainingWorkTime**, **actualWorkTime**, **actualSetupTime**, and **totalTimeAllowed**. The time unit for these fields is specified in the **timeUomId** field.

WorkEffort status (**statusId**) options include: In Planning, Approved/Scheduled, In Progress, Complete, Closed, On Hold and Cancelled. These are the statuses for the Default StatusFlow. To use a different StatusFlow use the **statusFlowId** field on either a particular WorkEffort or (depending on implementation) its root WorkEffort pointed to with **rootWorkEffortId**.

In addition to status WorkEffort has a resolution (**resolutionEnumId**). OOTB options include Unresolved (default), Completed, Incomplete, Won't Complete, Duplicate, Cannot Reproduce, and Insufficient Information. Additional resolutions can be added with Enumeration records of type WorkEffortResolution.

In addition to the hierarchical structure of work efforts they may be associated with others using the WorkEffortAssoc entity with types such as Depends On, Duplicates, Caused By, Independent Of (Concurrent), Routing Component, and Milestone. Note that milestones are associated with tasks through an association and are not as a parent WorkEffort. This is because a task may be associated with multiple milestones over time so we have a history and forward planning options. Additional association types can be added with Enumeration records of type WorkEffortAssocType.

For equipment or other types of Asset used (but not consumed) for a work effort use the WorkEffortAssetAssign entity. Asset records assigned this way are generally considered busy (otherwise unavailable) for the duration of the WorkEffort. To plan for a type of asset needed by the Product (**assetProductId**) that represents a type of asset, use the WorkEffortAssetNeeded entity. Product records may be associated with a WorkEffort for other reasons using WorkEffortProduct. Assets such as materials and supplies that are used (consumed) for a work effort are tracked with WorkEffortAssetUsed and asset produced by the work effort with WorkEffortAssetProduced.

Sometimes it is useful for organize work efforts by a more general Deliverable. Associate work efforts with it using WorkEffortDeliverableProd.

Use WorkEffortSkillStandard to record the skills (Enumeration of type SkillType from the HR/humanres entities) needed for a WorkEffort, usually as part of selection of parties to assign to the effort.

There are various reasons to associate a Party with a WorkEffort, and the party’s involvement with the work effort (just as a party’s association with other entities) is determined by the role (**roleTypeId**). This may be Manager, Worker, Operator, or any other role (including Not Applicable). For billing reasons a EmplPositionClass may be specified on the WorkEffortParty with the emplPositionClassId field.

Each Party association with a WorkEffort has a status (**statusId**; Offered, Assigned, Declined, Unassigned), availability (**availabilityEnumId**; Available, Busy, Away), expectation (**expectationEnumId**; For Your Information, Involvement Required, Involvement Requested, Immediate Response Requested) and in the case of delegation a reason for it (**delegateReasonEnumId**; Need Support or Help, My Part Finished, Completely Finished).

To associated a higher-level WorkEffort (such as a Project) with an Invoice using the WorkEffortInvoice entity. For more detail billing of particular tasks or other lower-level work efforts, or even a percentage of one, use the WorkEffortBilling entity.

General Resource Facade content and documents may be associated with a WorkEffort using the WorkEffortContent. Notes may be recorded for an effort using WorkEffortNote.

![MantleDataModel-work.effort](/docs/attachment/100472/MantleDataModel-work.effort.svg)

## Time Entry (mantle.work.time)

Use the TimeEntry entity to record the time worked (**hours**) on a task or other type of WorkEffort (by **workEffortId**) by a particular Party (**partyId**). The working time falls between the **fromDate** and **thruDate**, and if any time within that range was not spent working it can be recorded in **breakHours**. Generally **hours** + **breakHours**, if both specified, should match the time duration between **fromDate** and **thruDate**.

For billing purposes a RateType will generally be specified in **rateTypeId**. Common types include Standard, Discounted, Overtime, and On-site Work. This is used to lookup a RateAmount record along with other data applicable (may include **partyId**, **workEffortId**, **emplPositionClassId**, and **ratePurposeEnumId** as Client or Vendor). This may be done twice, once for the Client rate (client pays to vendor) and once for the Vendor rate (vendor pays to worker) and recorded in **rateAmountId** and **vendorRateAmountId**.

Once a TimeEntry is billed the relevant InvoiceItem is referenced with the **invoiceId** and **invoiceItemSeqId** fields for the invoice from vendor to client, and with the **vendorInvoiceId** and **vendorInvoiceItemSeqId** fields for the invoice from worker to vendor. When these are populated it means the time entry has been billed.

A Timesheet may be used to organize TimeEntry records, or to make time entry easier. There are generally two parties associated with a timesheet, the worker Party (**partyId**) and the client Party (**clientPartyId**). Other parties may be associated with it using TimesheetParty.

A Timesheet is generally used for just a specific date range (**fromDate**, **thruDate**). During its lifecycle a timesheet has a status (**statusId**) which is typically In-Process (work being done, time being recorded), Completed (all relevant work done and time recorded), or Approved (approved for billing).

![MantleDataModel-work.time](/docs/attachment/100472/MantleDataModel-work.time.svg)
