# Transactional Emails

## Email Configuration

There are a few emails generated in other ways (like the Password Reset and general Notification emails), but transactional emails in general are all configured per ProductStore using records for the ProductStoreEmail entity. There is a [tab on the Store screens in Marble ERP for Emails](https://demo.moqui.org/qapps/marble/ProductStore/FindProductStoreEmails?productStoreId=POPC_DEFAULT). The demo store ID is `POPC_DEFAULT` (from Mantle and PopCommerce demo data). POP Commerce mounts the same SimpleScreens tab.

Those records refer to an EmailTemplate record. There is no specific UI for that, so it is easiest to look at in the [Auto Screens in the Tools app for the EmailTemplate entity](https://demo.moqui.org/qapps/tools/AutoScreen/AutoFind?aen=moqui.basic.email.EmailTemplate&emailTemplateId=%25&emailTemplateId_op=begins).

For an example see the [POPC Order Placed EmailTemplate](https://demo.moqui.org/qapps/tools/AutoScreen/AutoEdit/AutoEditMaster?emailTemplateId=PopcOrderPlaced&aen=moqui.basic.email.EmailTemplate) (`PopcOrderPlaced`). Marble ERP does not define separate template IDs; the OOTB samples are in PopCommerce demo data.

On the EmailTemplate record there is a Subject field with the template for the subject, i.e. it can have `${}` to expand variables that are part of the data available to the template. The data available to an EmailTemplate is determined by code, and that code lives in the body screen for the template, specified in the Body Screen Location field of the EmailTemplate entity. OOTB body screens are in SimpleScreens (`component://SimpleScreens/screen/email/`).

## Build a New Email

To build a new email the basic steps are:

1. build the body screen (including actions for data prep and widgets for the email HTML and optionally plain text)
2. create an EmailTemplate record to configure the template
3. create a ProductStoreEmail record to make it live for orders, shipments, invoices, etc. associated with that store

## Existing Emails in Mantle

The mantle-usl code currently automatically generates emails based on status changes for the following store email types (from ProductStoreEmail records):

* Order Placed (`PsetOrderPlaced`)
* Order Approved (`PsetOrderApproved`)
* Shipment Shipped (`PsetShipmentShipped`)
* Shipment Delivered (`PsetShipmentDelivered`)
* Invoice Finalized (`PsetInvoiceFinalized`)

There is also an Invoices Past Due email (`PsetInvoicesPastDue`). It can be sent from the Invoice screen and by the `send_SalesInvoicePastDueEmails` service job (paused by default).

PopCommerce demo data includes templates for Order Placed, Shipment Shipped, Invoice Finalized, and Invoices Past Due. Order Approved and Shipment Delivered send only if you add ProductStoreEmail records for those types (there are no OOTB body screens for those two).

Sample config data, with references to the OOTB email templates, is in PopCommerce demo data:

https://github.com/moqui/PopCommerce/blob/master/data/PopCommerceDemoData.xml

## Editing by Non-Technical End Users

The Subject is fairly easily editable and the only complexity is dealing with the `${}` syntax and knowing which data is available (which depends on the Body Screen data prep actions). The template for the email body is generally more involved. The Body Screen could be implemented to pull the template from a wiki page and make it technically end user editable, but they would have to know a bit about both HTML and the template language (default in Moqui is FreeMarker, aka FTL). This is a bit more difficult for emails because the HTML supported by email readers is a small subset of the full HTML/CSS/JS supported by modern browsers.

More generally there are content management tools for both web and email that help by providing OOTB general templates with configurable layout, content, and other widgets. The tradeoff with those is a sacrifice of flexibility to simplify editing. Those are not trivial things to design and build, and need mechanisms to plug in custom scripts and templates (dropping down to artifacts that are no longer easily editable) to avoid making them useless for unanticipated real-world requirements... but when you do that you lose some or all of the easy end-user editing. For now this sort of thing is outside the scope of Moqui and unless someone designs, builds, and contributes a decent quality web and/or email easy building sort of tool along with a bunch of end user configurable pluggable widgets it will likely remain outside the scope of Moqui.
