# Accounting
[TOC levels=2]

## Account - Billing (mantle.account.billing)

A BillingAccount is used to group Invoice and Payment records for the purposes of tracking how much a customer (**billToPartyId**) owes to a vendor (**billFromPartyId**). The balance owed on the account is the unpaid invoice total minus the associated payment total. The payment total may be larger than the invoice total, in which case there is a positive balance in the account owed to the customer (**billToPartyId**). The BillingAccount may have a credit limit in the accountLimit field and its associated currency in **accountLimitUomId**.

A BillingAccount itself is fairly simple as the "transaction" details in the account are in Invoice and Payment records. It can have other parties associated with it using BillingAccountParty. For terms on the account use BillingAccountTerm.

## Account - Financial (mantle.account.financial)

A FinancialAccount is a singe-entry balance account like a bank account. There are various types of financial account defined with the FinancialAccountType entity with settings like **isRefundable**, **requirePinCode**, automatic replenishment settings, and others. OOTB types include Gift Certificate, Store Credit Account, Service Credit Account, Loan Account, and Bank Account.

A FinancialAccount is owned by a Party (**ownerPartyId**) and an internal organization (**organizationPartyId**) is liable for the balance on the account. Other parties may be associated with it using FinancialAccountParty. It has a name (**finAccountName**), code (**finAccountCode**), and may have a PIN number (**finAccountPin**). It may be valid only within a date range (**fromDate**, **thruDate**). It has a status (**statusId**) that may be Active, Negative Pending Replenishment, Manually Frozen, or Cancelled.

The **actualBalance** of a FinancialAccount is the sum of the transactions (FinancialAccountTrans) associated with the account. The **availableBalance** of an account is the **actualBalance** **minus** the total of authorizations (FinancialAccountAuth) on the account.

A transaction (FinancialAccountTrans) for a given **amount** may be a for Deposit, Withdraw, or Adjustment (**finAccountTransTypeEnumId**). Transactions requiring approval or for other reasons may have a **statusId** of Created, Approved, or Cancelled. They will generally have a reason (**reasonEnumId**) such as Purchase, Initial Deposit, Replenishment, or Refund.

A transaction happens at a certain date/time (**transactionDate**) and may be entered at a different time (**entryDate**). It is generally performed or initiated by a party (**performedByPartyId**) and may have **comments** about it. A transaction will also often have a Payment (**paymentId**) and/or OrderItem (**orderId**, **orderItemSeqId**) associated with it.

An authorization (FinancialAccountAuth) is used to reserve an **amount** in advance of a Withdraw transaction. The auth is done on **authorizationDate** and expires on **expireDate**.

## Account - Invoice (mantle.account.invoice)

An Invoice or bill is used to request Payment with details about why and is sent from the Party that is owed (**fromPartyId**) to the Party that owes (**toPartyId**). There are a few types of invoices (**invoiceTypeEnumId**) including Sales, Return, Payroll, Commission, and Template. The direction of the invoice is determined by the from and to parties so there is no separate type for purchase versus sales, they are both Sales type invoices with parties going one way or the other.

Depending on the direction and which Party is the internal organization there is a different set of statuses (**statusId**). For incoming invoices the statuses are Incoming, Received, Approved, Payment Sent, Billed Through, and Cancelled. For outgoing invoices the statuses are In-Process, Finalized, Sent, Payment Received, Write Off, and Cancelled.

The invoice may be associated with a BillingAccount (**billingAccountId**), see the **Account - Billing (mantle.account.billing)** section for details. Amounts on an invoice are for a single currency specified with the **currencyUomId** field. Each invoice is initiated on a certain date (**invoiceDate**), has a due date (**dueDate**) and for historical reference date when it was paid (**paidDate**). The due date is generally determined by a SettlementTerm record specified with the **settlementTermId** field. Other terms may be associated with the invoice or with invoice items using InvoiceTerm.

Contact details for an invoice are associated with it using InvoiceContactMech. In addition to the from and to parties other parties such as sales reps or accountants may be associated with an invoice using InvoiceParty.

The details of goods, services, shipping, tax, discounts, and so on for an invoice are recorded with InvoiceItem records. Invoice items use the same set of types as other items including mantle.order.OrderItem and mantle.order.return.ReturnItem. These shared item types are defined in the ItemTypeData.xml file. There are a wide variety of types for things like sales, purchase, expenses, commissions, and payroll. For sales orders the most common types are product, time entry, shipping charges, sales taxes, and discounts.

Just like order items, invoice items may have a hierarchical structure using the **parentInvoiceId** and **parentInvoiceItemSeqId** fields. This is used for things like tax items that are for a particular good or service item.

Each item has a **description** and will generally have a **productId** and possibly an **assetId** for more detail about goods and services. Each item has a **quantity** and unit for the quantity (**quantityUomId**) and an **amount** per quantity. The sub-total for an invoice item is: **quantity \* amount**.

Invoice items may be associated with other items using InvoiceItemAssoc. One example of when this is useful is when receiving an invoice with expense items from a service provider and billing those items through to a client.

An Invoice is a record with financial impact and triggers GL posting when the status changes to Finalized for outgoing invoices and Approved for incoming ones. Note that if both from and to parties on an invoice are internal organizations with accounting settings the invoice will be posted for both. If the **overrideOrgPartyId** field is populated that Organization will be used instead of the **fromPartyId** or **toPartyId** when posting depending on which is an internal org (this is not generally used if both are internal orgs).

The accounting transaction (AcctgTrans) generated for automated posting of an invoice will have one entry for each invoice item posted to the GL account (GlAccount) configured for the item type, and a balancing transaction entry with the total of the invoice posted to an accounts payable account for incoming invoices and an accounts receivable account for outgoing invoices.

![MantleDataModel-account.invoice](/docs/attachment/100462/MantleDataModel-account.invoice.svg)

## Account - Method (mantle.account.method)

A PaymentMethod is an instrument used for payment and each type has a separate entity with details including BitcoinWallet, CreditCard, EftAccount, GiftCard, and PayPalAccount. A PaymentMethod may be for a FinancialAccount and that is specified with the **finAccountId** field. Some payment method types such as cash, checks, and money orders are used directly on payments, orders, and so on with no PaymentMethod record because the Payment is not processed through a payment method.

A payment method is owned by a Party (**ownerPartyId**), has a **description**, and generally has a **postalContactMechId**, **telecomContactMechId**, and possibly a **emailContactMechId**.

A PaymentMethod is valid in a date range (**fromDate**, **thruDate**). Generally the **thruDate** field is null until the payment method is no longer used, or has been changes. PaymentMethod and related records are considered immutable, so when changed the original record has the **thruDate** set and a new record is created with the modified details. The new record points to the original with the **originalPaymentMethodId** field.

Where fraud is a concern the PaymentMethod should have a **trustLevelEnumId** set. OOTB options include New Data, Valid/Clean (through 3rd party service), Verified (with outbound contact or authorization), Greylisted, and Blacklisted. If the trust level is Greylisted or Blacklisted there should be a **paymentFraudEvidenceId** pointing to a PaymentFraudEvidence record with details about why.

For GiftCard payment methods they are usually purchased from or issue by the organization and details about that are tracked with the GiftCardFulfillment entity.

Certain types of payment method, especially credit cards, commonly have automated payment processing through a payment gateway such as Authorize.net and Cybersource. The integration with the payment processor consists of services for authorize, capture, release, and refund. These services are configured with the PaymentGatewayConfig which is typically associated with a ProductStore using the ProductStorePaymentGateway entity.

Any time a payment gateway is used the details of the response should be stored with the PaymentGatewayResponse entity. There are generally associated with a Payment (**paymentId**) and have various fields for codes and results from the payment processor.

![MantleDataModel-account.method](/docs/attachment/100462/MantleDataModel-account.method.svg)

## Account - Payment (mantle.account.payment)

A Payment is generally issued in response to an Invoice and like an invoice goes from one Party (**fromPartyId**) to another (**toPartyId**). The parties on a Payment will be reversed from the parties on an Invoice. Types of payments (**paymentTypeEnumId**) include Invoice Payment, Disbursement, and Refund. A payment always has an **amount** and the currency for it in **amountUomId**.

A Payment should always have a payment method type (**paymentMethodTypeEnumId**) such as cash, check, or credit card and if applicable for the payment method type should also have a payment method (**paymentMethodId**).

If the payment is processed automatically through a payment gateway the gateway used for auth should be recorded in **paymentGatewayConfigId** so that it can be used for subsequent operations like capture or void. For convenience (since these are also on the PaymentGatewayResponse) for automated payments there are **paymentAuthCode** and **paymentRefNum** fields for authorization results and the reference number to use for subsequent operations. Other fields for details when processing credit card and similar payments through a gateway include **presentFlag**, **swipedFlag**, **processAttempt**, and **needsNsfRetry**.

A payment has various statuses (**statusId**) including Proposed, Promised, Authorized, Delivered, Confirmed Paid, Cancelled, Void, Declined and Refunded.

Payments to not have items like an invoice, but may have deductions for special cases and these are recorded using the Deduction entity.

A Payment record may be created very early in an ordering process to specify payment details for an entire order or for a particular order part. There may be multiple Payment records for a given OrderHeader or OrderPart, so they are referred to using the **orderId** and if applicable **orderPartSeqId** fields on the Payment record. Payment details are looked up for an order or part using these fields on the Payment entity.

Payments may be associated with a financial account (**finAccountId**), and more particularly an authorization and/or transaction on a financial account (**finAccountAuthId**, **finAccountTransId**).

For fraud sensitive organizations and applications when processing online transactions it is important to associated the Payment with a Visit using the **visitId** field. This tracks the client IP address and other HTTP client and session information. When a fraudulent transaction is identified the evidence should be recorded in a PaymentFraudEvidence and this is usually used to change the trust level on the associated payment method (PaymentMethod.**trustLevelEnumId**) and contact mechs (ContactMech.**trustLevelEnumId**).

For organizations that deal with multiple currencies the payment may be converted to an internal currency for the organization, or to match the currency on the associated invoice(s). In this case the original amount and currency should be recorded in the **originalCurrencyAmount** and **originalCurrencyUomId** fields for bank and other reconciliation.

A Payment is a record with financial impact and triggers GL posting when the status changes to Delivered. Note that if both from and to parties on a payment are internal organizations with accounting settings the payment will be posted for both. If the **overrideOrgPartyId** field is populated that Organization will be used instead of the **fromPartyId** or **toPartyId** when posting depending on which is an internal org (this is not generally used if both are internal orgs).

The accounting transaction (AcctgTrans) generated for automated posting of a payment will have one entry posted to the GL account (GlAccount) configured for the cash account for payment method type (unless overrideGlAccountId is populated, then that is used), and a balancing transaction entry posted to an accounts payable account for outgoing payments and an accounts receivable account for incoming payments.

To make things a little more complex payments are explicitly applied to an Invoice using the PaymentApplication entity so that a single payment can apply to multiple invoices, and an invoice can have multiple payments applied to it. A payment may also be applied to another Payment for situations where incoming and outgoing payments between parties cancel one another.

For GL posting purposes a Payment can be received without being applied to an invoice, or being partially applied and the unapplied amount will be posted to an unapplied payment account instead of a cash account. When the payment is applied another accounting transaction will be triggered with entries in the unapplied payments account and the cash account to balance things out.

When a Payment is part of a budgeted expenditure it can be associated with one or more BudgetItem records using PaymentBudgetAllocation.

![MantleDataModel-account.payment](/docs/attachment/100462/MantleDataModel-account.payment.svg)

## Ledger - Account (mantle.ledger.account)

General ledger accounts (GlAccount) make up the chart of accounts for an internal Organization. Each account has a class (**glAccountClassEnumId**) to determine if the account balance is add or subtracted to a transaction total and for reporting purposes (especially: Balance Sheet with Asset on one side and Contra Asset, Liability and Equity on the other; and Income Statement with Revenue, Contra Revenue, Cost of Sales, Income and Expense accounts). Here is the structure of the OOTB GL account classes (this can be changed with different Enumeration records of type GlAccountClass):

TODO: update for latest defaults account classes

-   Debit
    -   Asset
        -   Current Asset
            -   Cash and Equivalent
            -   Inventory Asset
            -   Accounts Receivable
            -   Prepaid Expense and Other
        -   Long Term Asset
            -   Land and Building
            -   Equipment
        -   Other Asset
    -   Expense
        -   Cash Expense
        -   Interest Expense
        -   Sales, General, and Administrative Expense
        -   Non-Cash Expense
            -   Depreciation
            -   Amortization
    -   Cost of Sales
        -   Cost of Goods Sold
            -   Inventory Adjustment
        -   Cost of Services Sold
    -   Contra Revenue
    -   Equity Distribution
        -   Return of Capital
        -   Dividends
    -   Non-Posting
-   Credit
    -   Income
        -   Cash Income
        -   Non-Cash Income
    -   Revenue
        -   Goods Revenue
        -   Services Revenue
    -   Equity
        -   Owners Equity
        -   Retained Earnings
    -   Liability
        -   Current Liability
            -   Accounts Payable
            -   Accrued Expenses
        -   Long Term Liability
    -   Contra Asset
        -   Accumulated Depreciation
        -   Accumulated Amortization

GlAccount records also have a type (**glAccountTypeEnumId**) that is used for automated posting configuration. The available GL account types are in Enumeration records of type GlAccountType. There are quite a few defined OOTB such as AR, AP, Fixed Asset, Current Liability, Inventory, Finished Good Inventory, Tax, Profit Loss, Cost of Goods Sold, Expense, Customer Deposits, and Commission Expense (plus many others). There is some overlap in GL account classes and types, but they are separate fields because they are used for different things.

GL accounts are hierarchical with the **parentGlAccountId** field specifying the parent account. Each account has a code (**accountCode**) that is separate from the glAccountId so that it can be changed, a name (**accountName**) and a **description**. There is a **postedBalance** field that is maintained with each posting and derived from AcctgTransEntry records associated with the GlAccount.

For more general accounting use outside a typical general ledger GlAccount has a resource type (**glResourceTypeEnumId**) that is generally Money and can be other things such as Raw Material, Labor, and Finished Good. It also has a **glXbrlClassEnumId** field to specify the reporting (XBRL) class such as US GAAP and IAP.

To support multi-organization accounting there is a shared chart of accounts in GlAccount records and each internal Organization that needs it has a subset of the accounts assigned to it using the GlAccountOrganization entity. This has a **postedBalance** field that is updated with the balance of that account for just that Organization. Getting more specific there is a record in GlAccountOrgTimePeriod for each GlAccount, Organization, and TimePeriod (a fiscal month, quarter or year period). It has more detailed information about totals: **postedDebits**, **postedCredits**, **beginningBalance**, and **endingBalance**. These are all maintained by the GL posting service.

Other parties may be associated with a GL account using the GlAccountParty entity. A GlAccount may be associated with a budget through a budget item type using the GlBudgetXref.

In addition to the inherent hierarchy of GL accounts they may be organized with two other structures: categories and groups. GlAccountCategory is used for an arbitrary grouping of GL accounts and has a many-to-many relationship with them through the GlAccountCategoryMember. This is used for special tracking and reporting purposes such as cost centers.

A GlAccountGroup is a more restricted grouping of GlAccount records for purposes of reporting and populating forms such as tax forms. For example a US IRS Form 1120 (U.S. Corporation Income Tax Return) would be a group type, and groups within the type would be "1a Gross receipts or sales", "1b Returns and allowances", and "4 Dividends". Each GL account can be associated with at most one group of each type (i.e. for each form, etc) through GlAccountGroupMember. This is intentional to avoid applying a GL account more than once and duplicating its value.

## Ledger - Config (mantle.ledger.config)

The main entity of accounting preferences for an internal Organization is PartyAcctgPreference. It has fields for the tax filing form to use (**taxFormEnumId**), COGS method (**cogsMethodEnumId**), base currency for accounting (**baseCurrencyUomId**), fields to manage invoice ID sequencing (**invoiceSequenceEnumId**, **invoiceIdPrefix**, **invoiceLastNumber**, **invoiceLastRestartDate**, and **useInvoiceIdForReturns**), order ID sequencing (**orderSequenceEnumId**, **orderIdPrefix**, **orderLastNumber**) and the default PaymentMethod to use for refunds (**refundPaymentMethodId**).

One of the more important fields is **errorGlJournalId**. This is the GlJournal to put transactions (AcctgTrans) in when there is a problem with automatic posting. Transactions in this journal should be reviewed periodically, and most importantly before closing a period, to resolve issues and post the transaction. The most common issue is not finding the configuration for the GlAccount for a particular entry (AcctgTransEntry). Another possible issue is that the debits and credits don’t match.

The other entities in this package are for configuration the GlAccount to use for automated posting of various types of records that have a financial impact. The most general are GlAccountTypeDefault and GlAccountTypePartyDefault which are used to configure the default account for different GL account types if no more specific mapping is found.

For **Invoice** **posting** the various items are mapped by their ItemType (the same item type that is shared among OrderItem, ReturnItem, and InvoiceItem) using ItemTypeGlAccount. If a more specific mapping is found for an InvoiceItem it will be used. This may be for specific products with ProductGlAccount or ProductCategoryGlAccount or for tax items for a specific TaxAuthority with TaxAuthorityGlAccount. The balancing entry for an invoice is generally a debit to the default accounts receivable type account, or a credit to the default accounts payable type account.

For **Payment** **posting** the PaymentTypeGlAccount entity is used to find the balancing liability or asset (AR, AP, etc) GL account for the payment for an Organization by **paymentTypeEnumId**, **isApplied**, and **isPayable** (i.e., payable versus receivable). The cash account to post to is found for the payment method using PaymentMethodTypeGlAccount unless a more specific mapping is found for the credit card type in CreditCardTypeGlAccount or for a financial account type in FinancialAccountTypeGlAccount.

For inventory postings the GL account is determined generally with AssetTypeGlAccount, but for physical inventory variances the gain or loss is posted according to the variance reason configured with the VarianceReasonGlAccount entity.

## Ledger - Reconciliation (mantle.ledger.reconciliation)

GlReconciliation is used to record results of reconciliation with external sources such as a bank statement. Each GlReconciliation record is associated with a GlAccount (**glAccountId**), and generally for a specific Organization (**organizationPartyId**) for reconciliation on a certain date (**reconciledDate**). It tracks the **openingBalance** and **reconciledBalance**. The actual records to reconcile are AcctgTransEntry and the **reconciledAmount** for each is tracked with the GlReconciliationEntry entity.

## Ledger - Transaction (mantle.ledger.transaction)

An accounting transaction (AcctgTrans) is triggered by various things, and is associated with what triggered it or adds detail to what triggered it including asset issuance (**assetIssuanceId**), asset receipt (**assetReceiptId**), physical inventory (**physicalInventoryId**), invoice (**invoiceId**), payment (**paymentId**), payment application (**paymentApplicationId**) financial account transaction (**finAccountTransId**), shipment (**shipmentId**), and work effort (**workEffortId**). Transactions may also be created manually, i.e., not just through automated posting.

There are many types of accounting transaction (**acctgTransTypeEnumId**). The most common ones are Sales Invoice (from Org to Customer), Purchase Invoice (from Vendor to Org), Asset Receipt, Sales Inventory, Incoming Payment (Receipt), and Outgoing Payment (Disbursement). More exotic types include Amortization, Capitalization, Period Closing, and Credit Memo.

An AcctgTrans happens in the context of an internal Organization (**organizationPartyId**), happens at a certain date/time (**transactionDate**), knows if it is posted yet (**isPosted**), and if so the date/time when (**postedDate**). It may be in a single journal, such as the organization’s error journal, with the **glJournalId** field. The currency it is posted in is tracked in the **amountUomId** field, and if that is different from the currency of whatever the transaction is based on (such as an order) that currency goes in **origCurrencyAmountUomId**.

Each transaction entry (AcctgTransEntry) may be a debit or credit (**debitCreditFlag** of ‘D’ or ‘C’), has an **amount** and if the posting currency is different from the currency of what the transaction is based on the amount in the original currency goes in **origCurrencyAmount**. Each is associated with a specific GL account type (**glAccountTypeEnumId**), and in order to post successfully must be associated with a GL account (**glAccountId**).

An entry may be a summary of transactions from an external system and if so **isSummary** is set to **Y**. For invoice items the **invoiceId** is on the AcctgTrans record and the **invoiceItemSeqId** is on the AcctgTransEntry. The entry may also be associated with a product (**productId**) and/or asset (**assetId**).

Journals (GlJournal) may be used to keep track of specific accounting transactions, usually for transactions with errors or manual transactions and are in progress (**glJournalTypeEnumId**). They are for a particular organization (**organizationPartyId**) and single-use journals may be posted all at once, tracked with **isPosted** and **postedDate**. Transactions are associated with journals using the AcctgTrans.**glJournalId** field.

## Other - Budget (mantle.other.budget)

A Budget is generally associated with a TimePeriod (**timePeriodId**) and may be of various types (**budgetTypeEnumId**) such as Capital or Operating. Each BudgetItem has an amount and may have text descriptions of purpose and justification. The item type (**budgetItemTypeEnumId**) is generally something like Required or Discretionary. Parties may be associated with a budget using BudgetParty.

Various other entities point to BudgetItem records to provide detail for them, including: Payment through PaymentBudgetAllocation, EmplPosition, OrderItem, and Requirement through RequirementBudgetAllocation.

When a budget is reviewed by a particular party the results of the review are recorded with the BudgetReview entity. To keep a history of budget revisions use the BudgetRevision and BudgetRevisionImpact entities.

During a budget planning process various scenarios may be discussed and modeled. These can be recorded with the BudgetScenario and details for specific items in BudgetScenarioApplication and more generally for budget item types in BudgetScenarioRule.

## Other - Tax (mantle.other.tax)

A TaxAuthority is a government entity (**taxAuthPartyId**) that collects taxes within a geographic boundary (**taxAuthGeoId**). For VAT tax authorities set **includeTaxInPrice** to Y. If a tax ID is required for exemption set **requireTaxIdForExemption** to Y.

Many tax authorities have different tax rates for different types of products. To configure this create a ProductCategory for each type and use TaxAuthorityCategory to associate it with the tax authority. Tax authorities may be associated with other tax authorities using TaxAuthorityAssoc for Exemption Inheritance or as a Collection Agent (**assocTypeEnumId**). For example a US state tax authority may collect taxes on behalf of a city or county tax authority within that state, and exemption at the state level may exempt at the city or county level.

Parties may be associated with a TaxAuthority using TaxAuthorityParty. This is useful to represent that an internal organization has a nexus (**isNexus**=Y) or that a customer is tax exempt (**isExempt**=Y) and in either case the Party may have an ID issued by that tax authority and that is recored in the **partyTaxId** field.

Tax may be calculated using an external system or internal services configured using TaxGatewayConfig that in either case points to the service (**calculateServiceName**) that calculates the taxes or calls out to the external system. There used to be a TaxAuthorityRate entity for configuring local tax calculation, but that has been replaced with a Drools decision table which is more flexible. The TaxGatewayConfig is associated with a ProductStore using the ProductStore.**taxGatewayConfigId** field.
