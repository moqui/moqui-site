# USL Business Processes

This section contains overviews of the main high-level business processes supported in Mantle. This is an introduction to the business process concepts and the specific services and entities involved with each process. There are other services and entities not covered here, so this is not a complete reference of all services and options available. This will give you a good idea of the general functionality that exists and how it is structured, and from there you can review the source or the Service Reference to find related artifacts.

Mantle Business Artifacts has a wide variety of functionality, including the **procure to pay**, **order to cash**, and **work plan to cash** processes, with:

-   Purchase and Sales Orders (for goods, services, materials, etc.; POs for inventory and equipment/supplies/etc.)
-   Project, Task, and Request management with time and expense recording, billable/payable rates by project/task/client/worker/etc.
-   Incoming and Outgoing Invoices with a wide variety of item types and an XSL:FO template for print or email
-   Automatic invoice generation for purchase orders (AP), sales orders (AR), project client time and expenses (AR), project vendor/worker time and expenses (AP)
-   Payments, both manually recorded and automatic through payment processing interfaces; applying payments to invoices
-   Fulfillment of sales orders (including basic picking and packing) and receiving of purchase orders
-   Inventory management including issuance and receipt, and inventory reservation for sales orders
-   Automated GL account posting of incoming and outgoing invoices, outgoing and incoming payments, payment application, and inventory receipt and issuance
-   General GL functionality for time periods, validation of transactions to post, time period closing
-   Balance Sheet and Income Statement reports (and basic posted amounts and account balance by time period summaries)
-   Optional Drools/KIE rules for product pricing and shipping charge calculation (requires the `moqui-kie` component; without it, USL uses product price lookup only and skips rule-based shipping totals). Tax uses a `calculate#SalesTax` service interface; a local Drools tax table is not implemented out of the box.

The Tools application, included with moqui-runtime, has a Service Reference with detailed information on each service including descriptions, parameters, inline actions, etc. from the service definition files active in the system. This is best to review on customized or local instances (`http://localhost:8080/qapps/tools/Service/ServiceReference`) but is also available on the Moqui Demo server:

[https://demo.moqui.org/qapps/tools/Service/ServiceReference](https://demo.moqui.org/qapps/tools/Service/ServiceReference)
