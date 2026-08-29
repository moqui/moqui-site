# Order
[TOC levels=2]

## Order (mantle.order)

The primary entity for an order is OrderHeader. An order can be a purchase or sales order, and in fact with the OrderPart structure supports multi-party orders since each order part has a **customerPartyId** and a **vendorPartyId**. Order parts are used to split the order for other purposes such as shipping to different locations or by different methods, to ship from different locations, and so on. Order parts can have other parties associated with them using the OrderPartParty entity. Order parts are also used to split orders by different shipping addresses, shipment options, delivery dates, etc.

The shipping address (a type of contact mechanism) is referenced in the OrderPart.**postalContactMechId** field and there is an optional **telecomContactMechId** field to point to a phone (telecommunications) number. Additional contact mechs can be associated with the order part by purpose (such as billing phone, shipping address) using the OrderPartContactMech entity.

With a wide variety of statuses an order can be a shopping cart (Open/Tentative), quote (Proposed by Vendor), or a placed order (Accepted by Customer). There are also statuses so an order can be a wish list, gift registry, and auto reorder (order stays open for automatic recurring orders, each of which is a separate order).

After an order is Placed it can be fulfilled and is eventually either Completed, Cancelled by the customer, or Rejected by the vendor. It can also be Held or put in a special Being Changed status temporarily to avoid automatic calculation of things like shipping and taxes. Both OrderHeader and OrderPart have **statusId** fields to track statuses independently. Order items do not have a **statusId** field, their status is determined by looking at quantities on the item and quantities fulfilled, etc.

The items on an order are recorded as OrderItem records. For simplicity each OrderItem is associated with a single OrderPart record. OrderItem records are hierarchical so that they can be used for adjusting or detailing a parent item. This is useful for things like sales tax and discounts that apply to a single item. It is also useful for highly complex orders where items are organized under other items, such as specific building materials that are used for different parts of a structure of phases of building it.

Order items use the same set of types as other items including mantle.account.invoice.InvoiceItem and mantle.order.return.ReturnItem. These shared item types are defined in the ItemTypeData.xml file. There are a wide variety of types for things like sales, purchase, expenses, commissions, and payroll. For sales orders the most common types are product, time entry, shipping charges, sales taxes, and discounts.

When an OrderItem is billed (invoiced) it is associated with the InvoiceItem using the OrderItemBilling entity. Often billing of physical goods is done when a Shipment is sent (actually packed) or received, so there is a **shipmentId** on the OrderItemBilling entity. For outgoing shipments there is an inventory issuance modeled as an AssetIssuance record and we have the **assetIssuanceId** field to point to it. Similarly for incoming shipments there is an AssetReceipt record pointed to by the **assetReceiptId** field.

When an OrderItem is associated with a task, project or other type of WorkEffort (usually for work/service orders) it is associated with it using the OrderItemWorkEffort entity.

Orders may have a number of other records associated with them, including communication events (OrderCommunicationEvent), content such as documents or images (OrderContent), notes (OrderNote), and payment or other terms on an order part (OrderPartTerm).

![MantleDataModel-order](/docs/attachment/100466/MantleDataModel-order.svg)

## Return (mantle.order.return)

A return (ReturnHeader) tracks the details of requesting and processing order item returns from the customer (**customerPartyId**) to the vendor (**vendorPartyId**). Note that either Party may be an internal organization, or in other words the return may be incoming (receiving a return from a customer) or outgoing (sending a return to a supplier).

Each ReturnItem record points to an OrderItem record and specifies the **returnQuantity** for that item. There is a separate field, **receivedQuantity**, to track the quantity of the item actually received for the return. Each ReturnItem also has a **itemTypeEnumId** just like the OrderItem so that any type of item can be "returned" (including products, taxes, shipping charges, discounts, etc) and considered in the refund or other response.

Each ReturnItem has a **returnReasonEnumId** (like did not want, defective, mis-shipped, etc) for tracking purpose. Each item also has a **returnResponseEnumId** to specify how the organization should respond to the returned item (like refund, store credit, various methods of replacement, etc). There are fields on the item for tracking related records for the response (**replacementOrderId**, **refundPaymentId**, **finAccountTransId**). For refunds there will be an invoice based on the return for financial tracking (which will result in GL posting, etc) and the ReturnItemBilling is used to associate each ReturnItem with an InvoiceItem.

Both ReturnHeader and ReturnItem have a **statusId** field to track the progress of each item, and as major steps are completed the status of the return as a whole. OOTB statuses include: Created, Requested, Approved, Shipped, Received, Completed, Manual Response Required, and Cancelled.

![MantleDataModel-order.return](/docs/attachment/100466/MantleDataModel-order.return.svg)
