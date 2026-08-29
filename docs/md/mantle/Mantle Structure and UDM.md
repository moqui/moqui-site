# Mantle Structure and UDM
The Mantle data model (UDM) is based on concepts found in *The Data Model Resource Book, Revised Edition, Volume 1* and *Volume 2* by Len Silverston. In addition to the material in this section these books are a good reference for the data model concepts that make up the foundation for Mantle UDM. UDM is a loose implementation of the data model concepts in these books. UDM has a number of entities that go beyond what is in these books, and consolidates some of them too (like quote and order).

Both the data model (UDM) and the service library (USL) follow the same pattern for organizing artifacts. The directory and file structure of each are based on this pattern.

The sections below are a summary of the structure and the entities in each part. These are in alphabetical order for easy reference and to show the structure. When initially learning about the data model I recommend reading the sections on the more fundamental entities first with an order somewhat like this:

-   The **Data Model Patterns** section in the **Data and Resources** chapter
-   Party (mantle.party)
-   Contact Mechanism (mantle.party.contact)
-   Facility (mantle.facility)
-   Definition - Product (mantle.product)
-   Asset - Asset (mantle.product.asset)
-   Account - Invoice (mantle.account.invoice)
-   Account - Payment (mantle.account.payment)
-   Work Effort (mantle.work.effort)
-   Order (mantle.order)
-   Shipment (mantle.shipment)

The data model diagrams have only selected entities to illustrate important structures, and only selected fields on those entities. They are not a complete reference of all entities and fields. In the diagrams the master entities have a blue border, the detail entities a purple border, and the join entities a green border.

The Tools application, included with moqui-runtime, has an Entity Reference with detailed information on each entity including descriptions, fields, relationships, etc from the entity definition files active in the system. This is best to review on customized or local instances but is available here on the Moqui Demo server:

[https://demo.moqui.org/vapps/tools/Entity/DataEdit/EntityList](https://demo.moqui.org/vapps/tools/Entity/DataEdit/EntityList)
