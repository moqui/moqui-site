# Product
[TOC levels=2]

## Definition - Product (mantle.product)

A product is a person, place, or thing. Actually, that’s a noun, but products are similar. A Product is a description of a service, facility use, asset use, or a digital or physical good for sale. For manufacturing a product can represent raw materials, subassemblies, finished goods, and so on. These product types are specified with the **productTypeEnumId** and the options available are Enumeration records with the type ProductType.

An instance of a Product is tracked in different places depending on what type of product it is. Physical goods are tracked as inventory using the Asset and related entities. Asset use products are tracked as Asset records and have corresponding WorkEffort records for their schedule. Facility use products are tracked with Facility records, and also use WorkEffort for scheduling. Service products are tracked through a variety of WorkEffort records for projects, tasks, etc and may also have corresponding Request and Requirement records. The services will generally have one or more Party records associated with them for the people and/or organizations that will perform or have performed the service.

The Product entity has a **statusId**, but this is mostly there for special cases and is not used for certain things that might seem like statuses but are modeled as dates, including **salesIntroductionDate**, **salesDiscontinuationDate**, and **supportDiscontinuationDate**. If you want to know whether a product is available for sale, you check the current date/time against the sales date fields instead of looking at an indicator or status.

For content about the product it has **productName** and **description** fields, and the everything else such as more localized name/description, detailed descriptions, images, instructions, warnings, button/link labels, etc are all recorded with the ProductContent entity. The **contentLocation** points to a Resource Facade location so the content can be in a database (with the DbResource/File entities), a JCR (Java Content Repository, such as Apache JackRabbit), in the local filesystem, or any other location configured OOTB or that you add. See the **Resource Locations** section for more details.

Product has inventory (**requireInventory**, **requirementMethodEnumId**), shipping (**chargeShipping**, **inShippingBox**, **defaultShipmentBoxTypeId**, **returnable**), and tax (**taxable**, **taxCode**) settings. Some products have an amount associated with them, such as a number of cans in a case, or allow the user to enter an amount when purchasing it. Use the **amountUomId**, **amountFixed**, and **amountRequire** fields for this.

The various possible dimensions for a product are recorded with the ProductDimension entity. This would include weight, lengths dimensions, shipping dimensions, quantity and pieces included, and any other dimension you might want to define. To add other dimension types add Enumeration records of type ProductDimensionType. There is a similar structure for identifiers such as UPC, ISBN, EAN, etc: ProductIdentification.

Product has an **originGeoId** field to specify where the product comes from for import/export restrictions or for pure curiosity. For more specific Geo details like shipping and purchase restrictions use the ProductGeo entity.

A product can be associated with other products using ProductAssoc. This is useful for cross/up sell, size/color/etc variants, accessories, and for manufacturing purposes even BOM breakdowns. To associate a Product with a Party use the ProductParty entity. The ProductReview entity is used to record user/customer reviews and ratings.

The ProductPrice entity is used for a wide variety of prices, including: prices from suppliers and prices for customers (via **vendorPartyId** and **customerPartyId**); list, current, max/min, promotional, competitive, etc prices (**priceTypeEnumId**); purchase, recurring, and use prices (**pricePurposeEnumId**). For quantity breaks there is a **minQuantity** field (for any quantity greater than or equal to this, and less than the next highest matching record’s **minQuantity**).

Prices are valid in an effective date range (**fromDate**, **thruDate**) and can be restricted to a particular ProductStore (**productStoreId**). For jurisdictions with VAT taxes the price can have tax included (**taxInPrice**=true), and use the other tax fields to specify details (**taxAmount**, **taxPercentage**, **taxAuthPartyId**, **taxAuthGeoId**). See the **mantle.other.tax** section for more details about tax calculation.

The actual price goes in the **price** field, and its currency in the **priceUomId** field. See the **Units of Measure** section in the **Data and Resources** chapter for more details on UOMs. For recurring prices the recurrence term goes in **termUomId** and the price is the price per unit (like time, data size, etc).

![MantleDataModel-product](/docs/attachment/100468/MantleDataModel-product.svg)

## Definition - Category (mantle.product.category)

The obvious use for a ProductCategory is a way to structure products within a catalog, but that is only one of various types (**productCategoryTypeEnumId**). More generally a category is a way to specify a set of products. Other common types include tax, cross sell, industry, search, and best selling.

Products are associated with a category using ProductCategoryMember, which is the join entity that supports a many-to-many relationship (products can be in many categories, categories can have many products). Categories are associated with parent/child categories using ProductCategoryRollup, which is also a many-to-many relationship so a category can have multiple parent and child categories. Both of these have effective dates (**fromDate**, **thruDate**) and a **sequenceNum** field for sorting products within categories, and subcategories of categories.

ProductCategoryMember also has a **quantity** field which can be used when a category represents a set of products that come in a sort of ad-hoc or recommended package.

Content from the Resource Facade can be associated with a category using ProductCategoryContent. Similarly, parties can be associated with a category using ProductCategoryParty.

![MantleDataModel-product.category](/docs/attachment/100468/MantleDataModel-product.category.svg)

## Definition - Config (mantle.product.config)

Product configuration entities are used to specify configuration options for products of type Configurable Good (Product.**productTypeEnumId**=PtConfigurableGood). Configuration items are specified with the ProductConfigItem entity, and applied to the Configurable Good product using ProductConfigItemAppl. The options for a config item are specified with ProductConfigOption, and for options that are associated with another Product (which has its own inventory, pricing, supplier details, etc) use the ProductConfigOptionProduct entity.

To help clarify here is the path between the **configurable** product and the **component** product: Product ==&gt; ProductConfigItemAppl ==&gt; ProductConfigItem ==&gt; ProductConfigOption ==&gt; ProductConfigOptionProduct ==&gt; Product.

The ProductConfigOption entity has a **description** field, and for localized description and other content associated with an option use the ProductConfigItemContent entity to reference Resource Facade content locations.

When a configurable product is configured, usually when added to an order, we need a place to save the configuration and that starts with the ProductConfigSaved entity. This is referenced on an order item using the OrderItem**.productConfigSavedId** field. Within the saved configuration the option selected for each item is recorded with the ProductConfigSavedOption entity.

## Definition - Cost (mantle.product.cost)

CostComponent records are used to break down the cost of a Product, especially manufactured products. Products purchased from suppliers have a much simpler cost, the price paid to the supplier. Cost components include things like estimated and actual material, supply, equipment usage, and other costs. The various cost components added together for a particular product within a date range make up the cost of a product.

The CostComponentCalc entity, and the ProductCostComponentCalc to apply it to a Product, are used to specify how a CostComponent is to be calculated, or what the cost of a product should be based on.

The ProductAverageCost entity is used to keep track of the average cost of a Product over time (with a from/thru effective date range) optionally for a particular Facility and a particular Organization. This is mostly to be used for the purpose of COGS calculations that require an average cost history as opposed to being based on actual cost of an item sold.

## Definition - Feature (mantle.product.feature)

A ProductFeature describes a Product in a structured way. There are quite a few feature types (**productFeatureTypeEnumId**) defined OOTB, like Brand, Color, Fabric, License, and Size. It is common to add customer feature types using Enumeration records of type ProductFeatureType.

A feature is applied to a product using the ProductFeatureAppl with a **applTypeEnumId** to specify what the feature is to the product (Selectable for optional features, Standard for inherent aspects of a product, or Distinguishing to describe variants or a virtual product), and within an effective date range (**fromDate**, **thruDate**).

Sometimes it is necessary to model features that are incompatible or dependent, use the ProductFeatureIactn entity for this.

Features are naturally organized by type, but it is often useful to define sets of features that are used for a particular purpose such as facets for search of certain products or that are used to describe certain types of products (mostly for administrative purposes). The ProductFeatureGroup entity does just that. Use ProductFeatureGroupAppl to specify which features belong in which groups. For feature groups that are associated with a ProductCategory use ProductCategoryFeatGrpAppl to tie them together.

![MantleDataModel-product.feature](/docs/attachment/100468/MantleDataModel-product.feature.svg)

## Definition - Subscription (mantle.product.subscription)

A Subscription is used to record a party’s (**subscriberPartyId**) access to a SubscriptionResource for a specific date range (**fromDate**, **thruDate**). It is typically associated with the OrderItem used to purchase the subscription and for convenience the Product that was purchased to create the subscription. In addition to, or as an alternative to, the date range the subscription can be limited by actual use time as opposed to calendar time (**useTime**) and/or by use count (**useCountLimit**).

To configure a SubscriptionResource to be accessible for a **availableTime**, **useTime**, and/or **useCountLimit** when a Product is purchased use the ProductSubscriptionResource entity.

Use the SubscriptionDelivery entity to keep track of CommunicationEvent instances that are related to the subscription, especially for delivery of digital subscription resources.

## Asset - Asset (mantle.product.asset)

The Asset entity is used for inventory, equipment, and anything to be financially tracked as a fixed asset (**assetTypeEnumId**). Assets are identified by an **assetId**. An asset also has a class (**classEnumId**) such as forklift, tractor, laptop computer, or even software that can be used to categorize assets especially for manufacturing purposes to find the equipment needed for specific routes (manufacturing tasks). Add your own asset classes with Enumeration records of type AssetClass.

An Asset commonly represents an instance of a Product, or in other words the physical item that the Product record describes. The **productId** field specified which. An asset will also generally have an **assetName** and has a **comments** field to track general comments/notes.

Assets have a status (**statusId**) with various OOTB statuses for serialized inventory and equipment. A serialized inventory asset represents a single physical item and commonly has a **serialNumber**, hence the name.

Non-serialized inventory assets (**hasQuantity**=Y) represent more than a single quantity to handle simpler inventory needs where the items are all the same and don’t need to be individually tracked. The current physical quantity on hand is maintained in the **quantityOnHandTotal** field, and the quantity that can be reserved or promised in the **availableToPromiseTotal**. Inventory of a product will usually consist of multiple Asset records such that all items represented by the record have the same **receivedDate**, **lotId**, **facilityId** and **locationSeqId** (for the FacilityLocation where the asset is stored), **ownerPartyId** (the Party, usually internal org for inventory, that owns it), and where applicable **statusId**. Typically as each batch of inventory is received and put away a new Asset record is created for it.

The quantity fields have the Total suffix because they are derived from the **quantityOnHandDiff** and **availableToPromiseDiff** fields on the AssetDetail entity. Each AssetDetail record represents some change to an Asset such as a reservation for a placed order (**assetReservationId**), issuance on outgoing shipment (**assetIssuanceId**), receipt on incoming shipment (**assetReceiptId**), variance from physical inventory count (**physicalInventoryId**, **varianceReasonEnumId**), and production or consumption in a work effort such as a manufacturing route (**workEffortId**). If a Shipment is involved that is recorded in **shipmentId**, and all details should have their **effectiveDate** recorded.

When a physical inventory count is done it is tracked with a PhysicalInventory record, and the details for each inventory variance are recorded in AssetDetail records as described above.

An asset may have a number of dates recorded as applicable for the type of asset: **receivedDate**, **acquiredDate**, **manufacturedDate**, **expectedEndOfLife**, and **actualEndOfLife**. To track purchased assets and actual cost data Asset has **acquireOrderId**, **acquireOrderItemSeqId**, **acquireCost**, and **acquireCostUomId** fields. For fixed asset depreciation tracking, in adding to the corresponding AcctgTrans records, it has **depreciation**, **depreciationTypeEnumId**, and **salvageValue** fields.

Use AssetGeoPoint to record where an asset is, and a history of where it has been (with from/thru date fields). Use AssetIdentification to ID values for an asset such as a tracking label number, manufacturer serial number, VIN, etc. An Asset can be assigned to a Party using AssetPartyAssignment in a particular role and with an effective date range (**fromDate**, **thruDate**) for purposes such as use, management, maintenance, etc.

While an Asset is an instance of a Product, additional products may be associated with the asset to represent things such as rental or sale of the asset. Use the AssetProduct entity to keep track of these associated products.

While an inventory Asset, and sometimes other types of asset, are generally located in a FacilityLocation with the **facilityId** and **locationSeqId** fields it can also be located in a Container to more easily track movement of a set of assets that are in the container. In this case the **facilityId** and **locationSeqId** fields will be null and the Asset.**containerId** field will be populated. In that case the actual location will be found using the **facilityId**, **locationSeqId**, and **geoPointId** fields as applicable. These fields are audit logged to keep a history of their changes as a container moves.

![MantleDataModel-product.asset](/docs/attachment/100468/MantleDataModel-product.asset.svg)

## Asset - Issuance (mantle.product.issuance)

Because competition for specific inventory items is common, such as when sales orders are placed for products with limited inventory, it is necessary to track reservations with AssetReservation records that are created when an item is promised. Later on when the physical item is fulfilled a AssetIssuance is created and the AssetReservation is deleted as it is no longer valid.

A reservation is associated with the Asset (**assetId**), Product (**productId**) for convenience, and OrderItem (**orderId**, **orderItemSeqId**). It has the **quantity** reserved, and for when the reservation goes beyond on hand inventory the quantity reserved that was not available to promise is tracked with the **quantityNotAvailable** field.

An issuance is associated with the Asset (**assetId**), the AssetReservation (**assetReservationId**) if applicable, Product (**productId**) for convenience, and OrderItem (**orderId**, **orderItemSeqId**), and the Shipment (**shipmentId**) or AssetMaintenance (**assetMaintenanceId**) the asset is issued to. The issuance has a **issuedDate**, the **quantity** issued, and when applicable the **quantityCancelled** from the issuance.

The issuance may have parties associated with it in particular roles using AssetIssuanceParty.

When an AssetIssuance is created it triggers a general ledger accounting transaction to deduct it from the value of inventory on hand. This is part of the standard set of accounting transactions for inventory sales.

![MantleDataModel-issuance-receipt](/docs/attachment/100468/MantleDataModel-issuance-receipt.svg)

## Asset - Receipt (mantle.product.receipt)

When an Asset is received, especially an inventory asset, that receipt is tracked with the AssetReceipt. For convenience the **productId** of the asset and an itemDescription are recorded on this. The receipt may be associated with an OrderItem (**orderId**, **orderItemSeqId**), ShipmentPackage (**shipmentId**, **shipmentPackageSeqId**), ShipmentItem (**shipmentId**, **productId**), and ReturnItem (**returnId**, **returnItemSeqId**).

There are fields to track the user who received the asset (**receivedByUserId**), the date it was received (**receivedDate**), the **quantityAccepted** and **quantityRejected**, and if there is a rejected quantity the reason for it (**rejectionReasonEnumId**).

When an AssetReceipt is created it triggers a general ledger accounting transaction to add it to the value of inventory on hand. This is part of the standard set of accounting transactions for inventory purchasing.

## Asset - Maintenance (mantle.product.maintenance)

Following the pattern of Asset being an instance of a Product, the product describes the asset including the maintenance schedule associated with the product in the form of the ProductMaintenance entity. There are many types of maintenance, specified with the **maintenanceTypeEnumId** field, such as oil change and cleaning. You can add more by creating Enumeration records of type MaintenanceType.

The maintenance is to be done each **intervalQuantity** with the unit **intervalUomId**. The interval may be measured by a meter on the asset of ProductMeterType identified by **intervalMeterTypeId**. The meter should also be associated directly with the Product using ProductMeter. If a **repeatCount** is specified on the ProductMaintenance record the maintenance would be done only that many times.

The maintenance may be tracked with a WorkEffort and to simplify this a predefined work effort can be used as a template and copied from the maintenance schedule (ProductMaintenance.**templateWorkEffortId**) to the actual maintenance record (AssetMaintenance.**taskWorkEffortId**) where it would be assigned, the status updated, and so on.

For an actual maintenance effort for a particular Asset the AssetMaintenance entity has similar fields like the **intervalQuantity** value and related fields when the maintenance is actually performed. This has a status (**statusId**) to track planning and completion of the maintenance. It also has a **purchaseOrderId** for when the work is hired out to track the corresponding order. The maintenance may be purchased or sold and the relevant order item or items are tracked with AssetMaintenanceOrderItem.

It is typical to read meters on the asset when maintenance is done, and the meter values for each meter associated with the product (ProductMeter) are recorded with AssetMeter. Other meter readings may be done outside the context of maintenance and also recorded with AssetMeter. This may be done when fueling, at route waypoints, before/after production tasks, etc (**readingReasonEnumId**) and these records are often very important for financial management and tax liability.

Use AssetRegistration to record details when an Asset is registered with a government authority (**govAgencyPartyId**). These may include a **licenseNumber** and **registrationNumber**. The registration will happen on a certain date (**registrationDate**) and be valid within a date range (**fromDate**, **thruDate**).

![MantleDataModel-product.maintenance](/docs/attachment/100468/MantleDataModel-product.maintenance.svg)

## Store (mantle.product.store)

For sales order processing on an eCommerce site or in a POS (point of sale) system we need a way to keep track of all of the relevant settings. The ProductStore and related entities are used for this.

A store has a name (**storeName**) and is owned/run by an internal organization (**organizationPartyId**). While a store may support various languages and currencies each store is typically best focused on a single country/area with a single language (**defaultLocale**) and currency (**defaultCurrencyUomId**).

 including:

-   **Products available**: The ProductStoreCategory entity associates ProductCategory records with a store for browse root, default search, purchase allow, etc and the products in those categories or their sub-categories make up the products available in the store.
-   **Notification emails**: Use ProductStoreEmail to associated Moqui EmailTemplate records with the store for notification emails such as registration, order confirmation, order change, return completion, password update, and so on.
-   **Inventory reservation**: The most common case is to have a single inventory Facility for a store, and this is specified in the ProductStore.**inventoryFacilityId** field. When more than one is needed use the ProductStoreFacility entity. Inventory is reserved in the order specified with the ProductStore.**reservationOrderEnumId**, such as FIFO or LIFO by received date or expiration date. For automatic replenishment requirements set the ProductStore.**requirementMethodEnumId** field.
-   **Payment processing**: Use ProductStorePaymentGateway to configure the PaymentGatewayConfig to use for each **paymentMethodTypeEnumId**.
-   **Shipping options and rate calculation**: The ProductStoreShippingGateway entity is used to configure the ShippingGatewayConfig to use for each **carrierPartyId**.
-   **Tax calculation**: The ProductStore.**taxGatewayConfigId** points to the TaxGatewayConfig record to use for this store for sales/VAT tax calculation.

The ProductStoreParty entity is used for general needs to associate parties in a particular role with a store. One of many uses for this is if ProductStore.**requireCustomerRole** is set to Y then only parties associated with the store in the Customer role can access the store.

When managing a large number of stores or to automate based on specific sets of stores use the ProductStoreGroup entity to represent a group of stores, and ProductStoreGroupMember entity to associate stores with the group. A store can be associated with multiple groups. Use the ProductStoreGroupParty entity to associate parties with the group.
