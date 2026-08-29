# Procure to Pay
The **Procure to Pay** process is the one you use when you purchase goods or services from your suppliers. In this process you are "the customer" and the order can be made to your supplier in different ways (for example internet, phone, fax, or sales representative). To your business the process appears the same: you order and pay for the products, and the products are delivered.

NOTE: You may have minor variations to this, where the product is delivered before the supplier payment.

[TOC levels=2]

## Add Supplier

## Create Purchase Order

1. purchaser creates purchase order (products to order with quantities and supplier prices)
1. purchaser sends PO to supplier using Order PDF

## Receive Shipment

1. sometime later supplier ships product and a carrier drops it off at the warehouse
1. receiver looks up the PO and creates a shipment from it then records the receipt of each product (setting shipment quantities to quantity actually received, recording received vs rejected quantities)
1. receiver marks the shipment as Delivered, system automatically generates an invoice for the product actually received and connected to the PO and incoming shipment

## Receive Payable Invoice

1. supplier sends an invoice, with the shipment or separately
1. AP clerk looks up the PO, sees the invoice(s) associated with it, and goes to the system generated invoice for the received shipment
1. AP clerk updates invoice for info from supplier invoice (date, their order and invoice numbers, etc)
1. AP clerk reviews generated invoice items against the supplier invoice; if there are any differences contact shipping, purchasing, etc to find out what to do
1. AP clerk adds any shipping or other charges from the supplier on their invoice; after this the invoice totals should match (between supplier invoice and invoice in system)
1. AP clerk marks the payable invoice as Received
1. AP clerk (or accountant, manager, etc) reviews the Received invoice and if they look good marks them as Approved (this generates the AP GL transaction)

## Send Payment (Accounts Payable)

1. sometime later AP clerk reviews Approved invoices coming due and on the Invoice screen creates a Payment for the invoice (generally with a Company Check or ACH instrument, initially in the Promised or Authorized status; if the Promised status is used someone periodically reviews Promised outgoing payments and approves them; may also specify a Bank Account, which is a Payment Method, to issue the payment from)
1. periodically AP clerk looks at the list of Approved payments with a Company Check instrument using the Bulk Print Checks screen and generates a PDF for the checks then prints it on check stock; similar for ACH payments if a NACHA file can be used AP clerk goes to the Party => Payment Method => Files screen and generates a NACHA file for Approved payments

## Supplier Returns

## Inventory Management

## General Notes

Both the receiver and the AP clerk start by looking up a PO when something (shipment or invoice) is received from a supplier. That is intended to be the first step and can be done most quickly by using the Quick Search field at the top of the Marble ERP dashboard (it includes lookup by ID), or if the PO number/ID is not known then using the Find Order screen and searching for orders by Vendor (the supplier is the Vendor for purchase orders).

The reasons for system-generated Payable invoices include:

1. reduce data entry effort
1. when reviewing a system generated invoice against the actual invoice from the supplier you can compare your record of what was received to their record of what they are billing you for
1. ensure at least product items are posted to the correct GL accounts (and correct item type)
1. automatically associate with related order and shipment (currently this can't be done manually)
