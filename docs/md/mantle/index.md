# Mantle Business Artifacts
Mantle Business Artifacts is an open source project separate from and built on Moqui Framework. Moqui Framework is a set of tools to build applications. Mantle Business Artifacts is a library of lower-level artifacts that act as a foundation for business applications. The main benefits of using Mantle are cost savings, design and implementation risk reduction, adoption of common and standardized business structures and processes, and consistency with other applications built on Moqui and Mantle.

Mantle has three main parts: Universal Data Model (UDM), Universal Service Library (USL), and Universal Business Process Library (UBPL).

UBPL is a set of business process stories and other generic business requirement documents that drive the design of business applications. They are a good source for understanding the business concepts, actors, and processes that the data model and service library are based on. They are also generic enough to be used as a starting point for real-world business and modified as needed.

Mantle is a foundation for building enterprise automation applications such as:

-   Enterprise Resource Planning (ERP)
-   Project ERP
-   Professional Services Automation (PSA)
-   Customer Relationship Management (CRM)
-   Supply Chain Management (SCM)
-   Manufacturing Resource Planning (MRP)
-   Enterprise Asset Management (EAM)
-   Point-of-Sale (POS)
-   eCommerce

Together Moqui Framework and Mantle Business Artifacts form a foundation for an ecosystem of applications that are implicitly integrated. Applications can extend the Mantle data model and will always have their own services, but using the data model and services as intended will make applications work readily with data and services from other applications built on the same.

When such applications are deployed together the data is automatically shared. For example you will have a single structure for customer data that is used across all ecommerce, customer service, fulfillment, project management, and accounting applications and any other type of application that needs it.

NOTE: This section uses a large number of business terms. If you run across terms you are not familiar with you may look them up as you go (the internet is a wonderful thing, as is full text search of this documentation) or just take note of them, move on, and don’t worry too much about each one. The **Mantle Structure and UDM** section goes through a lot of terms with only data structures as context. When you get to the **USL Business Processes** section you will see the terms used in context of a process along with examples and they may make more sense, especially if you have spent some time reading about the data structures.
