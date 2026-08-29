
# Moqui Marble ERP User Guide

[TOC levels=2-4]

## Introduction

Marble is an ERP applications for retailers and wholesalers with comprehensive operational and managerial functionality including:

* Customer and Supplier Management
* Product Information, Content, and Pricing Management
* Internal and External Content Management
* Sales and Purchase Order Processing
* Customer and Supplier Returns
* Inventory and Warehouse Management
* Basic Manufacturing with Production Runs
* Incoming and Outgoing Shipments, Picklist Management and Streamlined Packing/Shipping
* Receivable and Payable Invoices
* Incoming and Outgoing Payments
* General Ledger with Automated Posting and Financial Reports
* Operational and other Reporting, Statistics, and Budgets

This guide is organized in sub-pages (see page tree to the left) by business activity with recommendations based on common business needs. The two primary operational flows are:

1. **Order to Cash**: general sales operations
1. **Procure to Pay**: general purchasing operations

There are also sections for **Configuration**, **Accounting**, **Warehouse**, etc that are for internal management and tracking and are not part of these two primary business processes.

## Supplier and Customer Diagram

While many business acitivties are internal to an organization most involve an interaction with an **external** Party. This diagram shows common interactions with the two primary external *Party Roles*:

1. **Supplier** for **Procure to Pay**
2. **Customer** for **Order to Cash**

![Supplier Customer Sequence Diagram](/docs/attachment/100051/PopcErpCustomerSupplier.svg)

## Concepts and Definitions

### Party

A **Party** is a *Person* or *Organization*. A **Role** describes how a Party is related to, or involved with, something in the system.

Many things in the system can be associated with many parties in different roles and many have certain parties that should always be specified. For example an Order always has a Vendor Party and a Customer Party, and an Invoice alway has a From Party and a To Party. A Role may also be *directly* assigned to a Party such as Customer, Supplier, and Employee to tell the system how to treat that Party. A Party may have multiple *direct* roles and may be associated in different roles with other records such as Orders, Payments, Work Efforts, etc.

An Organization using the system to manage and track operations is referred to as an **Internal Organization** (a Party with the *Internal* Role).

### Product & Asset

A **Product** is a model of anything you might buy, sell, use, store, etc. There are different types of Product for: *physical goods* (Assets) including inventory, equipment, and supplies; *digital goods*; good and facility *usage*; *services*; and others.

An **Asset** represents a physical instance of a *Product* such as inventory, equipment, and supplies. An **Asset Receipt** is a record of inventory or other types of Assets *received* from an Incoming Shipment or *produced* by a production run (a type of Work Effort). An **Asset Issuance** is a record of Assets *delivered* by a Shipment or *consumed* by a production run.

### Facility

A **Facility** is a place where inventory or other Assets are stored and used, or where business operations are done. Warehouses and retail stores are Facilities with Asset records for inventory in optionally configured Facility Locations. A Facility may have child Facilities like an office building with meetings rooms, each of which may have their own schedule.

### Order & Return

An **Order** is an agreement between two parties (a *Customer* and a *Vendor*) for the exchange of goods or services for Payment or like kind exchange. These agreements go through various phases dependending on circumstances and may optionally go through prelimary statuses such as *Quote Requested* and *Proposed by Vendor* for **Quoting**. Eventually an Order is *Placed* by the Customer, *Approved* by the Vendor, and once fulfilled is *Completed* by the Vendor.

For a **Sales Order** the *Vendor* is an Internal Organization, and for a **Purchase Order** the *Customer* is an Internal Organization. An Order may have multiple **Parts** to split it for fulfillment variations, multi-party agreements, and so on.

A **Return** represents the reversal of invoiced order items including products, fees, discounts, etc. The results of a Return may include a Return Shipment, Refund Payment, Credit Memo Invoice, Replacement Order, and so on. These can all exist indepdent of a Return but a Return is useful to tie these back to the original Order to better track what happened and why.

### Shipment

A **Shipment** represents a transfer of physical assets between locations. An **Outgoing Shipment** generally goes from an *Origin Facility* to a shipping address associated with the *To Party*. An **Incoming Shipment** generally goes from a shipping address associated with the *From Party* to a *Destination Facility*. A **Transfer Shipment** goes between two Facilities to move inventory, equipment, etc.

### Invoice & Payment

An **Invoice** represents a financial claim between two Parties and has details in Invoice Items to represent what the claim is for. For a **Payable Invoice** the *To Party* is always an Internal Organization and for a **Receivable Invoice** the *From Party* is an Internal Organization.

An Invoice is settled by applying a *Payment* or another *Invoice* (like a credit memo). A **Credit Memo** is a type of Invoice that is intended to be applied to another Invoice in lieu of payment and may be a Customer Credit Memo (payable) or a Supplier Credit Memo (receivable). The general rule for Payments and other Invoices that are *applicable* to an Invoice is that the From and To Parties must be reversed.

A **Payment** represents a transfer of funds *From* one Party and *To* another Party. An **Incoming Payment** is always *To* an Internal Organization and an **Outgoing Payment** is always *From* an Internal Organization. 

Each Payment has an *Instrument* for how the transfer was, or will be, done. A Payment may also have From and/or To *Payment Methods* representing specific bank accounts, credit cards, etc that are used for the transfer of funds. A Payment only represents the transfer of funds, not the details of why funds were transfered.

A Payment may be applied to an *Invoice* to settle payables or receivables or to another *Payment* for refund of overpayment, etc.

### Work Effort

A **Work Effort** is a task with status and/or an event with scheduled time. A Work Effort may have Child Work Efforts or a tree of Descendant Work Efforts under a single Root Work Effort (like a Project with task breakdowns).

Each Work Effort has a **Purpose** such as *Picklist* (Shipment Pick/Load/Ship), *Production Run*, *Meeting*, general *Task*, or more specific task like *Bug Fix* or *New Feature*.

