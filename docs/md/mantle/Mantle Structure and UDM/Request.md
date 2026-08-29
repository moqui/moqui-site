# Request
[TOC levels=2]

## Request (mantle.request)

A Request can be from a party (**filedByPartyId**) inside an organization such as an employee for things like inventory or general purchases, or outside an organization such as a client or customer for things like a quote, proposal, or in the software world for things like a bug fix or new feature. These are specified in the **requestTypeEnumId** field and while there are a few general ones defined OOTB you may want to define others by adding Enumeration records of type RequestType.

The default Request statuses (**statusId**) include Draft, Submitted, Reviewed, In Progress, Completed, and Cancelled. It also has a resolution (**requestResolutionEnumId**) that is by default Unresolved and default options include Fixed, Can't Reproduce, Won't Fix, Duplicate, Rejected, and Insufficient Information. Additional resolutions can be added as Enumeration records of type RequestResolution. If the result should be sent where to send it is specified with the **fulfillContactMechId** field.

A Request has a name (**requestName**), **description**, and if there is a story with additional details in Resource Facade content it is referred to with the **storyLocation** field. To help determine the order to work on requests and for general information it has **priority**, **requestDate**, and **responseRequiredDate** fields. A request may be associated with a Facility (**facilityId**) and ProductStore (**productStoreId**).

The details for a request are in its RequestItem records. An item can have its own **statusId** (using the same statuses as a request) and **requiredByDate** and typically has a **description**. If the request is for Product use the **productId**, **quantity**, and (if applicable) **selectedAmount** fields to specify details.

For quotes and other similar types of requests where there is a maximum amount/price to pay for the item, specify it in the **maximumAmount** field on the item. The unit for this amount is on the Request record in the **maximumAmountUomId** field. These types of requests also typically result in an order and the RequestItem is associated with an OrderItem using the RequestItemOrder entity.

For manual organization of requests use RequestCategory to specify hierarchical (with **parentCategoryId**) request categories associated with requests using the Request.**requestCategoryId** field.

A request may be associated with CommunicationEvent for communication related to the request (RequestCommEvent), Resource Facade content for additional content or documents (RequestContent), Party for parties working on or otherwise related to the request (RequestParty), and WorkEffort for tasks and other efforts related to handling the request (RequestWorkEffort). A request may also have notes (RequestNote).

As an example a Request may be created for a software bug fix. The request is assigned to someone with a RequestParty record. That person creates a task (WorkEffort) which is associated with the request using a RequestWorkEffort record. That task may be assigned to the same person or someone else, or even a group. Once the task is done its status is updated as is the status on the request.

![MantleDataModel-request](/docs/attachment/100469/MantleDataModel-request.svg)

## Requirement (mantle.request.requirement)

A Requirement may be for work, inventory, general customer or internal requirements, etc (**requirementTypeEnumId**). Add your own types with Enumeration records of type RequirementType. Its statuses (**statusId**) include Proposed, Created, Approved, Ordered, and Rejected. Inventory requirements and other types as applicable may be for a specific Facility (**facilityId**), and Product (**quantity**).

A requirement will typically have a **requirementStartDate** and a **requiredByDate**. To describe the requirement in detail, especially for software requirements, the **useCase** and **reason** fields are there for you. Parties may be associated with the requirement using the RequirementParty entity.

For automatic inventory replenishment inventory requirements can be created based on the ProductStore **requirementMethodEnumId** setting. Common options include creating a requirement based on every order, when ATP or QOH fall below the level configured on the relevant ProductFacility record, or for drop-ship third party ordering purposes. After requirements are created they can be summarized by Product and Facility then after a supplier is selected an order with the total quantity can be created and associated with the RequirementOrderItem entity.

Work requirements follow a different path. They may have an order associated with them for the labor, but more commonly result in a specific RequestItem (associated with RequirementRequestItem) or directly to a WorkEffort (with WorkRequirementFulfillment). The work effort can be for Implements, Fixes, Deploys, Tests, or Delivers (**fulfillmentTypeEnumId**).

The Requirement entity has a simple **estimatedBudget** field, and for more complex budgeting requirements or to include it in a larger budget plan it can be associated with a BudgetItem using the RequirementBudgetAllocation entity.

![MantleDataModel-requirement](/docs/attachment/100469/MantleDataModel-requirement.svg)
