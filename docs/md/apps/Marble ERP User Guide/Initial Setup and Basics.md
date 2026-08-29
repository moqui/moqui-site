# Initial Setup and Basics

[TOC levels=2,4]

## Initial Setup

### Start with base install data (no demo, etc)
- easiest: start Moqui with an empty database (ie don't do a `./gradlew load` or `java -jar moqui.war load`)
- default empty DB data types: **seed,seed-initial,install**
- env var `entity_empty_db_load` OR Moqui Conf XML `moqui-conf.tools.@empty-db-load` attribute
- warning: **MoquiDevConf.xml** (default when starting with `java -jar moqui.war`) loads all data files found; don't do this!
- example: `java -jar moqui.war conf=conf/MoquiProductionConf.xml`
### Create Initial Admin user (a one time action)
- go to any screen that requires authentication and default Login screen will show a form to create initial admin user
- fill out all fields, including User Full Name and Email Address

### Create first Company (Internal Organization)
#### Create Organization
- **Marble ERP Dashboard** ==> **Internal** (*marble/Party/FindParty* with role *Internal Organization*)
- use **New Organization** dialog, enter name and submit
#### Add Internal role (direct role)
- on the **Marble ERP > Parties > Party** screen (*marble/Party/EditParty*)
- verify role *Internal Organization* (added automatically if New Organization used after Internal link from Dashboard)
- if needed use **Add Direct Role** on **Edit Party** screen
#### Add Contact Information
- on the **Marble ERP > Parties > Party** screen (*marble/Party/EditParty*)
- under *Phone, Email, and Other* use **Add New** drop-down menu for the **Phone**, **Email**, **URL**, and **Other** dialogs
- under *Postal Addresses* use **Add Address** dialog
#### Configure Accounting Settings
- **Marble ERP Dashboard** ==> **Accounting** (*marble/Accounting/dashboard*)
- choose an Internal Organization, and click on the **Settings** link (on the right)
- clone accounting settings
  - select Base Currency, and if a different Local Currency is used (for tax reporting, etc) also choose that
  - choose a Source Party to clone accounting settings from, generally the OOTB *DefaultSettings* party
- still on the **Accounting Preferences** screen, adjust fields as needed
  - recommend setting *Per-Transaction GL Summary* to Y (so GL summary records are immediately updated for each GL transaction, not recommended for high volume)
  - recommend choosing a *Default Receivables Term* (default time period for receivable invoices)
  - other fields optional, many such as tax and employer classifications have little impact with current app functionality, but are used in various services where entities and services exist but no screens yet in Marble ERP)

## Sales - Service & Product

### Create first Customer
- Person vs Organization
- Sales Account & Sales Contact (organization customer & contacts in the org)
#### Create a Sales Account
- **Marble ERP Dashboard** ==> **Customers** (*marble/Customer/FindCustomer*)
- use **New Sales Account (Organization Customer)** dialog
#### Add Contact Information
- on the **Marble ERP > Customers > Customer** screen (*marble/Customer/EditCustomer*)
- same as for the Internal Org on **Parties > Party** screen
#### Add Payment Information (optional)
- under *Payment Methods* use **Create Credit Card** or **Create Bank Account**
- warning about credit cards: storing credit card information in the local database is risky (and tough PCI compliance), better to avoid unless a third party vault like Authorize.NET PIM is in use
#### Add a Sales Contact
- on the **Marble ERP > Customers > Customer** screen (*marble/Customer/EditCustomer*)
- under *Sales Account Contacts* use the **Add Contact** dialog to add an existing Person party as a contact, or **New Contact** to create a new Person party and add them as a contact to this Sales Account
- select a *Role* as applicable
  - some roles have related functionality
  - use the *Client Billing Rep* role to show the contact on receivable invoices

### Create first Invoice - Service
#### Create an Employee
- employee in the general sense, may be an owner or contractor; employment classification is separate from the Employee role
- **Marble ERP Dashboard** ==> **Employees** (*marble/Party/FindParty* with role *Employee*)
- use the **New Employee** dialog
  - ID is optional, generated numeric ID will be used if none specified
  - select the created Internal Organization as *Employer/Branch*, this will add a Party Relationship of type Employee (see under *Internal Organization Relationships* section of the **Parties > Party** screen)
  - if a *User Group* is selected the employee will have authorization and permissions for that User Group
  - once created set a password for the employee's User Account with the **Reset Password** button (send email with reset password), or use the **Account Detail** button to go to the System App (if current user has authorization) where a password can be set directly
- to use the Person party from the Initial Admin account, find it on Find Party and add the *Employee* role
#### Create a Project
- **Marble ERP Dashboard** ==> **Projects** (*marble/Project/FindProject*)
- use the **New Project** dialog
  - ID is optional, defaults to generated numeric ID, use something SHORT - it will be the prefix for all Task IDs in the project
  - for *Client* select the Sales Account party created above
  - for *Vendor* select the Company (Internal Organization) created above
#### Create a Work Task
- **Marble ERP Dashboard** ==> **Tasks** (*marble/Task/FindTask*)
- use **New Task** dialog (right side of screen)
  - select the Project created above
  - for convenience, *Assign To* the current user (initial admin user)
  - specify a *Task Name*
  - other fields can be left as-is, consider different *Priority* (ascending: 1 high priority, 9 low priority), *Purpose*, initial *Status*, *Due Date*, etc
  - use *Description* for details about the task, can also link to Wiki Pages, etc for more detail
#### Setup Billing/Pay Rates
- **Marble ERP Dashboard** ==> **HR** ==> **Labor Rates** (*marble/HumanRes/EditRateAmounts*)
- use **Add Rate Amount** dialog
  - leave *Type*: Standard, *Purpose*: Client Billing
  - optionally select a *Project*, *Person*, etc
  - specify a *Rate Amount*, different *Currency* if needed
#### Record a Time Entry
- can be done on Task > Time, Party > Time, or My Account > Time screens
- in upper right open user dialog, click on any of the 4 my account icons to get to the My Account app OR under the **Applications** menu in the top left select the **My Account** app
- click on the **Time** tab
- can use **Clock In** and **Clock Out** dialogs for recording time on the fly
- use the **Record Time** dialog
  - for *Employer* use the Company (Internal Org) created above
  - for *Task* select the task created above, and assigned to the current user (initial admin user)
  - while different combinations are available, select a *From Date* and enter a number of *Hours* (can be decimal)
  - add *Comments* to describe work done (will show on the receivable invoice if item per time entry is selected)
- after adding a time entry click on the open dialog button to the left of the time entry to open the edit dialog, verify *Client Hour Calc* shows the desired rate (the rate added above)
#### Create Project Client Invoice (receivable)
- **Marble ERP Dashboard** ==> **Projects** (*marble/Project/FindProject*)
- select the project created above
- go to the **Time Entries** tab, verify desired time entries are shown
- use the **Project Client Invoice** dialog
  - optionally specify *Thru Date*, or defaults to now (includes all time entries up to that date/time)
  - select a *Grouping* option, try *Item Per Time Entry* for detailed invoice
#### Review Invoice
- **Marble ERP Dashboard** ==> **Receivable Invoices** (*marble/Accounting/Invoice/FindInvoice* with type *Receivable*)
- select the invoice just created
- review parties, total, due date & terms, items, etc
#### Finalize Invoice
- still on the Marble ERP > Accounting > Invoices > Invoice screen
- if all looks well, click on the **Finalize** button
- note the *GL Transactions* created

### Create first Invoice - Physical Good
#### Create first Product
##### New Product, Content
- **Marble ERP Dashboard** ==> **Products** (*marble/Catalog/Product/FindProduct*)
- use **New Product** dialog
  - specify a *Product Name* and leave *Product Type* as *Asset (Good)*
  - *Owned By Org* is for multi-organization systems to isolate Product and other data across organizations, leave as *N/A*
- on the **Marble ERP > Catalog > Products > Product** screen
  - update *ID* (Pseudo ID) if needed
  - change *Asset Type* to *Inventory*
  - change *Asset Class* to *Inventory - Finished Good*
  - add *Description* and other fields as needed
- go to **Content** tab and add text, image, and other content as needed (mainly for ecommerce, can be useful for internal use as well)
##### Pricing
- go to the **Prices** tab: **Marble ERP > Catalog > Products > Prices**
- use the **New Price** dialog
  - for *Type* use *Current Price* (default)
  - for *Purpose* use *Purchase/Initial* (default)
  - optionally select a *Vendor* and/or *Customer* for Vendor/Customer specific pricing, or leave empty for all Vendors and Customers
  - specify other fields as needed to constrain applicability of price
  - for quantity breaks use the *Min Quantity* field
  - specify a *Price*, and a different *Currency* from the default if needed
#### Create first Facility
- **Marble ERP Dashboard** ==> **Facilities** (*marble/Facility/FindFacility*)
- use the **New Facility** dialog
  - optionally specify *ID*, defaults to generated numeric ID
  - specify a *Facility Name*
  - leave *Facility Type* as Warehouse for use with Inventory for sale
  - optionally specify an *Owner*
#### Create first Product Store
- **Marble ERP Dashboard** ==> **Stores** (*marble/ProductStore/FindProductStore*)
- use **New Store** dialog
  - optionally specify *ID*, defaults to generated numeric ID
  - specify a *Name*
  - for *Organization Party* use the Company (Internal Org) created above
- on **Marble ERP > Stores > Product Store** screen
  - select the *Facility* created above
  - for *Auto Reservation* (of inventory) select *On Order Placed*
  - set *Default Currency* to USD (general default for demo, needs other config to consistently use different currency)
  - set other fields as needed
#### Receive or Record Inventory
- **Marble ERP Dashboard** ==> **Inventory** (next to **Assets**, *marble/Asset/Asset/FindSummary* with type *Inventory*)
- use **Receive Direct** dialog
  - note that this is a shortcut and for better bookkeeping a purchase order, incoming shipment, and payable invoice should be used
  - select the *Product* created above
  - leave *Status* as *Available*
  - specify a *Quantity*
  - select the *Facility* created above
  - for *Owner* select the Company (Internal Org) created above
  - for accounting purposes, and because a purchase order is not being used, specify an *Acquire Cost*
  - use other fields as needed
#### Create first Sales Order
- **Marble ERP Dashboard** ==> **Sales Orders & Quotes** (*marble/Order/FindOrder* with type *Sales*)
- use **Create Sales Order** dialog
  - select the *Store* created above
  - note that *Vendor Org* and *Facility* are selected automatically based on the *Store*
  - select the *Customer* created above (the Sales Account)
  - use other fields as needed
- on the **Marble ERP > Orders > Order Detail** screen
  - use the **Add Product Item** dialog
    - select the *Product* created above
    - leave *Price* empty to use configured price (shown under *Calc Price*)
    - leave other fields as-is unless there is a special circumstance
  - use the **Place Warnings** dialog to place the order
    - there are warnings for a few things important to consider for normal business circumstances, ignoring for now...
    - use the **Place Order Anyway** button
  - use the **Approve Warnings** dialog
    - similar to place warnings, important considerations for normal use
    - use the **Approve Order Anyway** button
  - use the **Create Shipment** button, see it disappear replaced by a **Shipment {ID}** button
  - use the **Shipment {ID}** button
#### Ship the Order
- on the **Marble ERP > Shipments > Shipment** screen (from the button on the **Order Detail** screen)
- in the **Shipment Items** section use the **Issue & Pack** button to submit that inline form with defaults
- verify the *Issuance* under **Shipment Items**
- verify the **Packages**, use **Update Package** as needed to specify box type, weight, etc
- use the **Set Packed** dialog
  - at this point an Invoice for the Shipment is created
- use the **Set Shipped** dialog to finalize the Shipment, send notice emails, etc
  - note the warnings there for real world use
  - if Shippo or other shipping integrations are in place there will be options here to generate and print labels, and that is done before using the **Set Shipped** dialog
- note the **Pack Screen** button which goes to a screen optimized for in warehouse use, in the **Shipping** area of Marble ERP
#### Review Invoice
- from the **Shipments > Shipment** screen use the **Invoice {ID}** button
- note that the Status defaults to *Finalized* when created from a Shipment with a Sales Order
- note and verify parties, total, due date & terms, items, etc

### Receive first Payment
- payments can be viewed or created directly on **Marble ERP Dashboard** ==> **Customer Payments**
- easier to create a Payment from an existing Invoice
  - **Marble ERP Dashboard** ==> **Receivable Invoices** (*marble/Accounting/Invoice/FindInvoice* with type *Receivable*)
  - select an unpaid (*Finalized*) Invoice
  - use **New Payment for Invoice** dialog
    - *Payment Status* defaults to *Promised*, if already received change to *Delivered*
    - verify or modify *Amount*
    - make sure to specify the *Effective Date* (will be used for GL posting, reconciliation, etc)
    - select a *Payment Instrument* and/or *From Payment Method* (must already exist on Customer's account through **Customers > Customer** screen)
    - add data for other fields as needed
  - after submit verify payment applied to Invoice in the **Payment Applications** section, and *Unpaid* amount as $0.00
  - note the new transaction under **GL Transactions**
  - note the Invoice status changed to *Payment Received*

## Accounting

### Review Accounting Reports
- **Marble ERP Dashboard** ==> **Reports** (right of **Accounting**, *marble/Accounting/Reports/ReportList*)
- if data is missing because *Per-Transaction GL Summary* was not set to **Y**
  - under the **Accounting** menu select **Time Period**
  - select any current time period, easiest is current year
  - go to the **Accounts** tab
  - click on **Recalc All**
  - go back to the Accounting Reports screen (Accounting menu ==> Reports)
- try the **Income Statement** dialog
  - make sure the *Organization* selected is the Company (internal org) created above
  - for *Time Periods* select the current year (and/or other relevant time periods)
  - for more report features select the *Detail* and *Percent of Revenue* options
  - these use print-specific CSS so try printing from your browser (ctrl-p or Print from menu)
- try the **Balance Sheet** dialog
  - same notes as Income Statement
