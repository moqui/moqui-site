# OAGIS Order to Cash

[TOC levels=2-3]

NOTE: These pages describe OAGIS document-exchange scenarios. The `mantle-oagis` component is listed in addons.xml with no releases and is not required to run Moqui, Mantle USL, or Marble ERP.

## Introduction

This process covers Customer and Supplier processes from Order through Cash plus Quotes and GL.

## OAGIS Scenarios

### Incorporated Scenarios

* 1 - General Ledger to Sub Ledgers
* 5 - Order Management to Accounts Receivable and General Ledger
* 7 - Purchasing to Accounts Payable to General Ledger
* 8 - Purchasing to Accounts Payable to General Ledger Posting from Purchasing
* 12 - Basic Purchase Order Process
* 25 - Invoice Matching, Matching in Accounts Payable
* 27 - Sales Force Automation to Order Management, Updating Orders
* 28 - Sales Force Automation to Order Management, Inquiry of Orders
* 29 - Sales Force Automation to Order Management and Shipping
* 30 - Supply Chain Integration
* 37 - Catalog and Price List Exchange
* 39 - Request for Quote and Quote Exchange
* 47 - Full Cycle Purchasing
* 53 - Inventory Visibility
* 54 - Mid Market Order to Cash Procure to Pay
* 55 - High Tech Procure to Pay
* 56 - High Tech Invoicing
* 58 - Metals Industry Order to Cash Procure to Pay
* 59 - High Tech Logistics - Direct Ship Model
* 60 - High Tech Logistics - Standard VMI With Outsourced - Customer Agent
* 61 - High Tech Logistics - Customer Operated Hub

### Related Scenarios

* 3 - Order Management to Accounts Receivable
* 4 - Order Management to Credit Management to Accounts Receivable
* 14 - Plant Data Collection / Warehouse Management / Issues
* 15 - Plant Data Collection / Warehouse Management / Transfers
* 19 - Plant Data Collection / Warehouse Management / Shipping
* 21 - Manufacturing to Purchasing (Requisitions, Purchasing, Inspection, Receiving, MRP)
* 22 - Manufacturing with Available to Promise to Order Management
* 23 - Manufacturing to Order Management Financials with Manufacturing for Engineer to Order and Configure to Order (Engineering - BOM, Inventory - Finished Goods, Order Management, Manufacturing, Inventory - Work In Progress, GL, Costing, AR)
* 31 - Customer Service Integration, Field Service, No Returns
* 48 - Sales Lead
* 49 - Sales Opportunity

## Actors

* Customer - purchase product from Supplier
* Supplier - sells product to Customer
* Carrier - transports product from Supplier to Customer
* Organization - general organization, may be Customer or Supplier or other

## Process Story

### Catalog

Supplier Catalog Management sends SyncCatalog to Supplier Order Management and Purchasing, and each sends ConfirmBOD to Catalog.
Catalog sends SyncPriceList to OM and Purchasing, and each sends ConfirmBOD to Catalog.
Inventory sends SyncItemMaster to OM, Catalog, and Purchasing and each sends ConfirmBOD to Inventory.

Customer sends GetCatalog to Supplier and Supplier sends ShowCatalog to Customer (alternatively Supplier Sync and Customer Confirm).
Customer sends GetPriceList to Supplier and Supplier sends ShowPriceList to Customer (alternatively Supplier Sync and Customer Confirm).

Customer sends GetInventoryBalance to Supplier and Supplier sends ShowInventoryBalance to Customer.
Alternatively, Supplier sends SyncInventoryBalance to Customer and Customer sends ConfirmBOD to Supplier (and optionally vice-versa).

### Quote

Customer sends ProcessRFQ to Supplier and Supplier sends AcknowledgeRFQ to Customer.
To change a RFQ, Customer sends ChangeRFQ to Supplier and Supplier sends RespondRFQ to Customer.
To get RFQ details, Supplier sends GetRFQ to Customer and Customer sends ShowRFQ to Supplier.
To cancel an RFQ, Customer sends CancelRFQ to Supplier and Supplier sends ConfirmBOD to Customer.

Supplier sends ProcessQuote to Customer and Customer sends AcknowledgeQuote to Supplier.
To change a quote, Supplier sends ChangeQuote to Customer and Customer sends RespondQuote to Supplier.
To get quote details, Customer sends GetQuote to Supplier and Supplier sends ShowQuote to Customer.
To cancel a quote, Supplier sends CancelQuote to Customer and Customer sends ConfirmBOD to Supplier.

### Order

Customer sends ProcessPurchaseOrder to Supplier (supplier internally creates SalesOrder) and Supplier sends AcknowledgePurchaseOrder to Customer.
To change a purchase order Customer sends ChangePurchaseOrder to Supplier and Supplier sends RespondPurchaseOrder to Customer.
To cancel a purchase order Customer sends CancelPurchaseOrder to Supplier and Supplier sends ConfirmBOD to Customer.
To get purchase order info Supplier sends GetPurchaseOrder to Customer and Customer sends ShowPurchaseOrder to Supplier.

Supplier Sales sends SyncPurchaseOrder to Supplier Order Management.
Supplier Order Management sends SyncPurchaseOrder to Manufacturing, Shipping, and/or Billing and each sends ConfirmBOD to OM.

For separate internal Sales/SFA within Supplier:
Sales (SFA) sends ProcessSalesOrder to Order Management and OM sends AcknowledgeSalesOrder to Sales.
To change a sales order Sales sends ChangeSalesOrder to OM and OM sends RespondSalesOrder to Sales.
To cancel a sales order Sales sends CancelSalesOrder to OM and OM sends ConfirmBOD to Sales.
To get sales order info OM sends GetSalesOrder to Sales and Sales sends ShowSalesOrder to OM.
If Supplier has separate Manufacturing, Shipping, or Billing (or Dispatch, Weight Bridge) Supplier OM sends SyncSalesOrder to each and each sends ConfirmBOD to OM.

### Shipping

Customer sends ProcessPlanningSchedule to Supplier and Supplier sends AcknowledgePlanningSchedule to Customer.

(pick/pack) Supplier Manufacturing sends UpdatePickList to Supplier Shipping and Supplier Shipping sends RespondPickList to Supplier Manufacturing.
Supplier Shipping sends PostJournalEntry to Supplier GL and GL sends PostAcknowledgeJournalEntry to Shipping.

(carrier) Supplier sends ProcessShipment to Carrier and Carrier sends AcknowledgeShipment to Supplier.
Supplier sends ProcessCommercialInvoice, NotifyShippersLetterOfInstruction, NotifyExportDeclaration, and NotifyHazardousMaterialShipmentDocument to Carrier (as needed) and Carrier sends ConfirmBOD to Supplier.

Carrier picks up shipment from Supplier.

Supplier sends NotifyShipment to Customer and Customer sends ConfirmBOD to Supplier.
Supplier sends NotifyShipment to Carrier and Carrier sends ConfirmBOD to Supplier.

Carrier delivers shipment to Customer.

Carrier sends NotifyShipmentUnit to Supplier and Customer, and each send ConfirmBOD to Carrier.
Carrier sends ProcessInvoice (for freight) to Supplier and/or Customer, and Supplier and/or Customer send AcknowledgeInvoice to Carrier.
Carrier sends NotifyReceiveDelivery to Supplier and Supplier sends ConfirmBOD to Carrier.

Customer sends NotifyReceiveDelivery to Supplier and Supplier sends ConfirmBOD to Customer.

### Supplier AR

Supplier AR sends ProcessInvoice to Customer AP and Customer AP sends AcknowledgeInvoice to Supplier.

Supplier Billing sends PostJournalEntry to Supplier General Ledger and GL sends PostAcknowledgeJournalEntry to Billing.
Alternatively, Supplier Billing sends LoadReceivable to Supplier AR and AR sends ConfirmBOD to Billing, then Supplier AR sends PostJournalEntry to Supplier GL and GL sends PostAcknowledgeJournalEntry to AR.
Alternatively, Supplier Order Management sends LoadReceivable to Supplier AR and AR sends ConfirmBOD to OM, then AR sends PostJournalEntry to GL and GL sends PostAcknowledgeJournalEntry to AR.

### Customer AP

Customer Purchasing sends SyncPartyMaster to AP and AP sends ConfirmBOD to Purchasing (and vice-versa to keep in sync).

Customer Purchasing sends LoadPayable to AP and AP sends ConfirmBOD to Purchasing. AP or Purchasing sends PostJournalEntry to GL and GL sends ConfirmBOD back.

Customer sends NotifyRemittanceAdvice to Supplier and Supplier sends ConfirmBOD to Customer.

### Sub-Ledger

If Organization has separate General Ledger and Sub-Ledger(s), Organization GL sends SyncChartOfAccounts to Sub-Ledger and SL sends
ConfirmBOD to GL. SL sends PostJournalEntry to GL and GL sends PostAcknowledgeJournalEntry to SL.

## Simple Order to Cash Scenario

Customer sends ProcessPurchaseOrder to Supplier (supplier internally creates SalesOrder) and Supplier sends AcknowledgePurchaseOrder to Customer.

Supplier sends NotifyShipment to Customer and Customer sends ConfirmBOD to Supplier. TODO: NotifyBOM?

Customer optionally sends NotifyReceiveDelivery to Supplier and Supplier sends ConfirmBOD to Customer.

Supplier sends ProcessInvoice to Customer and Customer sends AcknowledgeInvoice to Supplier.

Customer sends NotifyRemittanceAdvice to Supplier and Supplier sends ConfirmBOD to Customer.

## OAGIS Documents Used

### Party
* SyncPartyMaster - ConfirmBOD

### Catalog and Inventory
* SyncCatalog - ConfirmBOD
* SyncPriceList - ConfirmBOD
* SyncItemMaster - ConfirmBOD
* GetCatalog - ShowCatalog
* SyncInventoryBalance - ConfirmBOD

### RFQ and Quote
* ProcessRFQ - AcknowledgeRFQ
* ChangeRFQ - RespondRFQ
* GetRFQ - ShowRFQ
* CancelRFQ - ConfirmBOD
* ProcessQuote - AcknowledgeQuote
* ChangeQuote - RespondQuote
* GetQuote - ShowQuote
* CancelQuote - ConfirmBOD

### Purchase Order
* ProcessPurchaseOrder - AcknowledgePurchaseOrder
* ChangePurchaseOrder - RespondPurchaseOrder
* CancelPurchaseOrder - ConfirmBOD
* GetPurchaseOrder - ShowPurchaseOrder
* SyncPurchaseOrder - ConfirmBOD

### Sales Order
* ProcessSalesOrder - AcknowledgeSalesOrder
* ChangeSalesOrder - RespondSalesOrder
* CancelSalesOrder - ConfirmBOD
* GetSalesOrder - ShowSalesOrder
* SyncSalesOrder - ConfirmBOD

### Shipping
* ProcessPlanningSchedule - AcknowledgePlanningSchedule
* UpdatePickList - RespondPickList
* ProcessShipment - AcknowledgeShipment
* ProcessCommercialInvoice, NotifyShippersLetterOfInstruction, NotifyExportDeclaration, NotifyHazardousMaterialShipmentDocument - ConfirmBOD
* NotifyShipment - ConfirmBOD
* NotifyShipmentUnit - ConfirmBOD
* NotifyReceiveDelivery (aka NotifyDeliveryReceipt?) - ConfirmBOD

### AR, Invoice, AP, Payment
* LoadReceivable - ConfirmBOD
* ProcessInvoice - AcknowledgeInvoice
* LoadPayable - ConfirmBOD
* NotifyRemittanceAdvice - ConfirmBOD

### Ledger
* PostJournalEntry - PostAcknowledgeJournalEntry
* SyncChartOfAccounts - ConfirmBOD

## Initial Documents to Support

* ProcessPurchaseOrder - AcknowledgePurchaseOrder
* NotifyShipment - ConfirmBOD
* ProcessInvoice - AcknowledgeInvoice
* NotifyRemittanceAdvice - ConfirmBOD
