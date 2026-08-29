# Order to Cash
[TOC levels=2-4]

## Introduction

The **Order to Cash** process manages the process of sales to your customers. In this process customers order something from you that you deliver to them. The order can be received via different ways (e.g. internet, phone, fax or sales representative). To the customer the process appears the same - they order and pay, then they receive the product. As the company managing the internal process, there may be different subprocesses involved in processing, sourcing or delivering the order that is hidden from the customer.

* Add Customer
* Customer Submits Sales Order
    * eCommerce Order
    * Phone, Email, Other Order
* Shipping Fulfills Approved Sales Order
* AR Sends Invoice and Receives Payment
* Over Payment and Short Payment
* Customer Returns
* Customer Service

## Notification Emails

Notification emails sent to Customers are configured on a Product Store and settings for a particular Order, Shipment, or Invoice come from the Product Store it is associated with. To view or change Product Store notification emails use the Product Store **Emails** tab.

Automatic emails are sent to a single Customer email address. If there is more than one email address for a given Email Purpose then the most recent active email address with the given Purpose is used.

Notification emails may also be sent manually to any email address on the Order Detail, Shipment Detail, and Edit Invoice screens.

| Type | Trigger | Email Purpose |
| ---- | ---- | ---- |
| **Order Placed** | Order Header status changed to **Placed** | *Order Notification*, if not found use *Primary* |
| **Order Approved** | Order Header status changed to **Approved** | *Order Notification*, if not found use *Primary* |
| **Shipment Shipped** | Shipment status changed to **Shipped** | *Shipping Destination*, if not found use *Primary* |
| **Shipment Delivered** | Shipment status changed to **Delivered** | *Shipping Destination*, if not found use *Primary* |
| **Invoice Finalized** | Invoice status changed from **In Process** to **Finalized** | *Billing (AP)*, if not found do not send email |
| **Invoice Past Due** | Sent by a job that **by default** runs each Monday at 2:00 AM and sends emails for Invoices with *Due Date more than 7 days* in the past OR *Invoice Date more than 40 days* in the past AND no Invoice Past Due *email sent in the last 2 days*; actual configuration settings may vary | *Billing (AP)*, if not found do not send email (default, may be changed in the job configuration) |
