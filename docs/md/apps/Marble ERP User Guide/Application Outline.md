# Application Outline

[TOC levels=2-3]

## General Screens

* Dashboard
* Quick Lookup
* Search
* Custom Reports
* Report Builder
  * Find Report
  * Report Viewer
  * Edit Report
  * View

## Parties

A **Party** is a *Person* or *Organization* and may have one or more *Roles* such as Customer, Supplier, Employee, etc. An organization using the system to manage and track operations is referred to as an **Internal Organization** (a Party with the *Internal* role). A Party may have multiple roles and may be associated in different roles with other records such as Orders, Payments, Work Efforts, etc.

* Find Party
* Party
  * Payment Method
    * Payment Method
    * Transactions
      * Create Payment
    * Checks
    * Files
    * Gateway Responses
  * Calendar
  * Emails
  * Messages
    * Message List
    * Message
    * Thread
  * Related
  * Time
  * Agreements
    * Edit Agreement
    * Find Agreement
  * Financial Info
  * Expired Contact Other
  * Expired Postal
  * Find Duplicates
  * Update Contact Info
  * Update Payment Method Info

## Suppliers

* Find Supplier
* Supplier
  * Financial Info

## Customers

* Find Customer
* Customer
  * Financial Info
* Customer Data

## Requests

* Find Request
* Request
* Items

## Orders

An **Order** is an agreement between two parties (a *Customer* and a *Vendor*) for the exchange of goods or services for Payment or like kind exchange. These agreements go through various phases dependending on circumstances and may optionally go through prelimary statuses such as *Quote Requested* and *Proposed by Vendor* for **Quoting**. Eventually an Order is *Placed* by the Customer, *Approved* by the Vendor, and once fulfilled is *Completed* by the Vendor. For a **Sales Order** the *Vendor* is an Internal Organization, and for a **Purchase Order** the *Customer* is an Internal Organization. An Order may have multiple **Parts** to split it for fulfillment variations, multi-party agreements, and so on.

* Find Order
* Order Detail
  * Item Reserve
  * Return Item
  * Update Contact Info
  * Update Payment Method Info
  * Print Order
  * Quick Items
* Order Issued and Invoiced
* Sales Order Analysis
* Sales Summary

## Shipments

A **Shipment** represents a transfer of physical assets between locations. An **Outgoing Shipment** generally goes from an *Origin Facility* to a shipping address associated with the *To Party*. An **Incoming Shipment** generally goes from a shipping address associated with the *From Party* to a *Destination Facility*. A **Transfer Shipment** goes between two Facilities to move inventory, equipment, etc.

* Find Shipments
* Shipment Detail
  * Item Reserve
  * Receive Item
  * Update Contact Info
  * Update Item Asset
* Package Tracking
* Shipment By Package
* Shipment Insert
* Shipment Pack
* Shipment Pick

## Shipping

* Dashboard
* Picklists
  * Picklists
  * Picklist
    * Add Orders
    * Add Shipments
    * Bulk Create Picklists
  * Shipment Load Pick
  * Shipment Load Pick And Pack
* Pick Location Moves
* Pack Shipment
  * Pack Completed
* Shipment By Package
* Shipment Insert
* Shipment Pack

## Returns

A **Return** represents the reversal of invoiced order items including products, fees, discounts, etc. The results of a Return may include a Return Shipment, Refund Payment, Credit Memo Invoice, Replacement Order, and so on. These can all exist indepdent of a Return but a Return is useful to tie these back to the original Order to better track what happened and why.

* Returns
* Return
  * Items
  * Add From Orders

## Catalog

* Dashboard

### Categories

* Find Category
* Category
  * Products
  * Content
    * Content Compare
    * Detail
    * List

### Features

* Find Feature
* Feature

### Feature Groups

* Find Feature Group
* Feature Group

### Products

A **Product** is a model of anything you might buy, sell, use, store, etc. There are different types of Product for: *physical goods* (Assets) including inventory, equipment, and supplies; *digital goods*; good and facility *usage*; *services*; and others. An **Asset** represents a physical instance of a *Product* such as inventory, equipment, and supplies.

* Find Product
* Product
  * Content
    * Content Compare
    * Detail
    * List
  * Associated
  * Categories
  * Prices
* Search Products

## Assets

* Dashboard

### Assets

* Find Asset
* Find Summary
* Move Asset
* Asset Detail
  * Detail History
  * Move
  * Calendar
  * Meter Readings
  * Maintenance
  * Registrations
  * Assignments

### Lots

### Containers

* Containers
* Container
  * Move

### Pools

* Pool
* Pools

## Survey

* Find Survey
* Survey
  * Fields
  * Responses
  * Response Details
  * Response Stats

## Manufacturing

* Dashboard

### Production Runs

* Production Runs
* Production Run
  * Run Products
    * Consume Asset
    * Consume Product
    * Produce Asset
  * Assets Consumed
  * Assets Produced
* Run Pick Document

## Facilities

* Find Facility
* Facility
* Locations
* Calendar
* Products

* Box Types
* Print Box Types
* Carrier Shipment Methods

## Stores

* Find Product Store
* Product Store
  * Promotions
    * Store Promotions
    * Promotion
    * Promo Codes
      * Find Promo Code
      * Edit Promo Code
  * Emails
  * Categories
  * Parties
  * Facilities
  * Settings

## Wiki/Content

* Edit Wiki Page
* Wiki Spaces
* Wiki Space
* Wiki View
* Wiki Compare
* Wiki Blog Posts
* Edit Blog Post

## Accounting

* Dashboard

### Org Settings

* Accounting Preferences
* GL Accounts
* Account Types
* Invoice Types
* Item Types
* Payment Types
* Payment Instruments
* Financial Acct Reasons
* Financial Acct Types
* Asset Types

### Invoices

An **Invoice** represents a financial claim between two Parties and has details in Invoice Items to represent what the claim is for. For a **Payable Invoice** the *To Party* is always an Internal Organization and for a **Receivable Invoice** the *From Party* is an Internal Organization. An Invoice is settled by applying a *Payment* or another *Invoice* (like a credit memo). A **Credit Memo** is a type of Invoice that is intended to be applied to another Invoice in lieu of payment and may be a Customer Credit Memo (payable) or a Supplier Credit Memo (receivable). The general rule for Payments and other Invoices that are *applicable* to an Invoice is that the From and To Parties must be reversed.

* Find Invoice
* Invoice
  * Items
  * Orders
  * Shipments
  * Budget Details
* Print Invoice
* Aging
* Receivable Statement

### Payments

A **Payment** represents a transfer of funds *From* one Party and *To* another Party. An **Incoming Payment** is always *To* an Internal Organization and an **Outgoing Payment** is always *From* an Internal Organization.  Each Payment has an *Instrument* for how the transfer was, or will be, done. A Payment may also have From and/or To *Payment Methods* representing specific bank accounts, credit cards, etc that are used for the transfer of funds. A Payment only represents the transfer of funds, not the details of why funds were transfered. A Payment may be applied to an *Invoice* to settle payables or receivables or to another *Payment* for refund of overpayment, etc.

* Find Payment
* Payment
* Payment Check
* Payment Detail
* Bulk Checks

### Financial Accounts

* Financial Account Statement
* Find Financial Account
* Financial Account
  * Transactions

### Transactions

* Find Transaction
* Find Transaction Entry
* Transaction
  * Move Entry

### GL Journals

### Time Period

* Find Time Period
* Time Period
  * Accounts

### GL Accounts

* Find Gl Account
* Gl Account Tree
* GL Account

### Budgets

* Budgets
* Budget
  * Accounts Entry
  * Items List
  * Expense Report

### Reports

* Report List
* Account Balance
* Account Ledger
* AR Aging Summary
* Asset On Hand
* Asset On Hand Summary
* Asset Receipt Transaction
* Asset Status by Receipt
* Inventory Valuation
* Balance Sheet
* Cash Flow Statement
* Financial Ratios
* Income Statement
* Aging Detail
* Invoice Item Summary
* Invoice Reconciliation
* Order Issued and Invoiced
* Order Item Summary
* Posted Amount Summary
* Posted Balance Summary
* Retained Earnings Statement
* Sales Order Analysis
* Sales Invoice Analysis
* Sales Summary
* Shipment Package Summary
