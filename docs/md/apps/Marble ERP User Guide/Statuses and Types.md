# Statuses and Types Reference
[TOC levels=2-3]

## Introduction

Before reading this read the [Concepts and Definitions](/docs/apps/Marble+ERP+User+Guide#concepts-and-definitions) section of the Marble ERP User Guide.

Many records have a Status to manage their current state and track their lifecycle over time. In some cases statuses have meaning only to users of the system and there is no automation (code) that behaves differently based on status. In other cases the system treats records differently based on their status and there is sometimes significant automation that behaves differently for different statuses. A set of statuses also has a status flow with valid transitions between statuses defined, a sort of work flow for the record. The statuses documented here are out-of-the-box statuses for the open source applications based on Mantle UDM (where default statuses are defined) and may be modified or extended in the Moqui-based system you are using.

A type is used to distinguish records that are mostly similar but have different properties or behaviors. Based on a record's type there might be different system behavior and the UI for interacting with the record might vary.

## Party

## Product

### Product Type

### Asset Status

| Status | Description |
| -------- | --------- |
| *Incoming* | Not yet received but some details are known and recorded before receiving |
| **Available** | Key status used to determine assets that may be reserved, picked, etc; assets in any other status are not 'Available' for sale, reservation, or issuance |
| *On Hold* | General holding status, not Available for reservation or issuance |
| *Returned* | Returned by Customer, usually pending quality control or disposal |
| Promised | Promised or reserved, generally for serialized inventory (1 quantity per Asset record) |
| Delivered | Delivered to Customer, generally for serialized inventory |
| Activated | Activated by Customer, generally for serialized inventory |
| Deactivated | Deactivated by Customer, generally for serialized inventory |
| In Use | Being used internally, generally for equipment and supplies assets |
| In Storage | Being stored for future use or sales availability |
| In Transfer | Being transferred from one facility location to another |
| In Transfer (Promised) | Reserved for transfer but move not started |
| Defective | Known defective but not yet disposed |
| Quarantine | Temporary status pending quality control and kept separate from other assets to prevent and manage contamination |
| Morgue | Long term storage for quality control over time |

### Asset Type

### Asset Class

## Facility

### Location Type

## Order

### Order Header and Part Status

| Status | Description |
| -------- | --------- |
| **Open (Tentative)** | The initial status for most orders; Orders in this status may be changed by Customer or by Vendor |
| Being Changed | Temporary status while an order is being edited after it has already been proposed or otherwise locked; returns to Open or another status when changes are complete |
| Quote Requested | Quote requested by **Customer** instead of going directly from Open to Placed, followed by Proposed By Vendor before being Placed by Customer |
| Proposed By Vendor | Quote proposed by **Vendor**, but not yet accepted (placed) by Customer |
| **Placed** | Placed by **Customer** agreeing to terms and details in the Order |
| Processing | This is an interim status between Placed and Approved used only when an order has started review and processing for approval |
| Held | Use this status to hold an order after it has been Placed and before it is Approved |
| **Approved** | Approved by **Vendor** agreeing to terms and details in the Order, ready for fulfillment by Shipment or other means; partial fulfillment and billing is tracked per order item by quantity using relationships to Shipment and Invoice Items |
| Sent | Generally used only for purchase orders (Customer is an Internal Organization) to denote that the order has been sent to Vendor |
| **Completed** | An order, or part of an order, goes into this status once all quantities of all items have been fulfilled |
| *Rejected* | Rejected by **Vendor** |
| *Cancelled* | Cancelled by **Customer** |
| Wish List | A special status for orders that represent a wish list. Orders in this status do not typically change status |
| Gift Registry | A special status for orders that represent a gift registry list. Orders in this status do not typically change status |
| Auto Reorder | A special status for orders that represent an automatic reorder. Orders in this status do not typically change status until they are placed |

## Shipment

### Shipment Status

| Status | Description |
| -------- | --------- |
| Input | Initial status for a Shipment being input and prepared |
| Scheduled | The shipment is scheduled, or at least the input is complete and the shipment ready to be processed |
| Picked | Items for the shipment have been picked from storage locations |
| Packed | Items for the shipment have been packed into final packaging and packages have been weighed, etc; for outgoing shipments system will create a receivable invoice for items not already billed |
| Shipped | Effectively 'shipped' with label, tracking code, etc; may not yet be loaded or picked up by Carrier; Shipment Shipped email gets sent if configured |
| Delivered | Has been delivered to the To party; for incoming shipments has been fully received and system creates a payable invoice for items not already billed; Shipment Delivered email sent if configured |
| Rejected | Rejected on attempt to deliver |
| Cancelled | Cancelled before shipping |

#### Incoming Shipment Flow

- Input
- Scheduled
- Picked (optional, if notified by From party)
- Packed (optional, if notified by From party)
- Shipped (optional, if notified by From party)
- Delivered (received)

To be received an incoming shipment must be in the Scheduled or later status. A shipment may be marked Delivered if it is at least partially received and means that no further items are expected. When a shipment goes into the Delivered status an incoming (payable/purchase) invoice will be generated for items not already billed.

#### Outgoing Shipment Flow

- Input
- Scheduled
- Picked (optional)
- Packed (required)
- Shipped (optional)
- Delivered (optional)

To be packed an outgoing shipment must be in the Scheduled or later status. Note that as item quantities are packed (independent of the packed status) they are issued to the shipment and accounting transactions are posted. The most important status for an outgoing shipment is Packed. In this status the shipment is considered final and may be invoiced. For outgoing shipments with items associated with order items, an outgoing (receivable/sales) invoice will be generated and authorized payments captured when a shipment changes to the Packed status.

## Invoice

### Invoice Status

#### Receivable (Outgoing/Sales) Invoice Status

| Status | Description |
| -------- | --------- |
| In-Process | This is the initial status for an outgoing invoice and used while the invoice is being entered and edited before finalizing |
| Finalized | The invoice is finalized and ready to be sent, invoice may not be changed and triggers GL posting |
| Sent | Optional, has been sent to the To Party |
| Acknowledged | Optional, To Party has acknowledged the invoice |
| Payment Received | Payment has been received and applied, set automatically when sufficient payments applied; if status changed to Finalized all applied payments will be unapplied (and application GL postings reversed) |
| Write Off | Not expected to be paid and should be written off using Customer Credit Memo Invoice |
| Cancelled | Cancelled by From or To Party, if Cancelled after Finalized status unapplies all applied payments and credit memos and reverses related GL transactions |

#### Payable (Incoming/Purchase) Invoice Status

| Status | Description |
| -------- | --------- |
| Incoming | The initial status for incoming invoices to use when recording invoice details |
| Received | Fully entered and awaiting approval for payment |
| Approved | Approved for payment, invoice may not be changed and triggers GL posting |
| Payment Sent | Payment has been sent to the invoice From party, set automatically when sufficient payments applied; if status is changed back to Approved all applied payments will be unapplied (and application GL postings reversed) |
| Billed Through | Receivable (outgoing) invoice has been created to bill the invoice through to a third party |
| Cancelled | Cancelled by From or To Party, if Cancelled after Approved status unapplies all applied payments and credit memos and reverses related GL transactions |

## Payment

### Payment Status

| Status | Description |
| -------- | --------- |
| Proposed | Initial status of a payment, unless already Delivered; tentative and generally being modified before a promise or authorization |
| Promised | Promised for some purpose such as payment for an Order |
| Authorized | Outgoing payments: authorized to be sent to the To Party; Incoming payments: payment instrument based such as credit card authorization |
| Delivered | Outgoing payments: has been sent; Incoming payments: has been received |
| Confirmed Paid | Outgoing payments: the To Party has verified they have received the payment; Incoming payments: confirmed received such as reconciliation with a bank account |
| *Cancelled* | The payment was cancelled before funds were sent |
| *Void* | The payment was voided before funds were transferred |
| *Declined* | The payment was declined (such as a credit card decline) or failed to clear |

## Return

### Return Header and Item Status

## Work Effort

### Work Effort Type

### Work Effort Purpose

### Work Effort Status
