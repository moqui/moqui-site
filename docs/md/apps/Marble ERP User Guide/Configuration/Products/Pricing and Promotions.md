# Pricing and Promotions

[TOC levels=2,3]

## Overview and Definitions

Product prices are determined by looking up the relevant price for a given product and may be modified by a price modify service. The result is the price to be charged to the customer or paid to a supplier. In accounting terms this is the gross revenue per quantity for the sale of a given product to a customer. Different prices may be configured for different stores, vendors, customers, currencies, date/time ranges, and quantity breaks. These may then be modified by a rule or service that has logic such as calculating a discounted price for certain customer classifications like charging 50% of the List price (MSRP) when selling to distributors. Product price calculation can be done before adding an item to an order (or shopping cart) and is always done when a product item is added to an order unless a manual price is specified by a user allowed to do so (such as a Sales Person or Customer Service Rep).

Promotions are applied to sales orders after the price to charge has been looked up and calculated, and generally based on the price charged for the related product item. A single promotion may apply to multiple items in an order whereas pricing is per order item. Promotions are calculated for and applied to an entire order and promotion discounts will generally vary based on how much of different product items are in a given order. In accounting terms promotion discounts are subtracted from gross revenue to calculate net revenue. While humans can come up with a huge variety of promotions the most common form is buy X quantity get Y quantity at Z% discount. For example a buy 3 get 1 free (100% discount) promotion would have X = 3, Y = 1, Z = 100 for this type of promotion. When a promotion like this runs a Discount type order item is added automatically as a child item of the product item.

Price configuration is primarily associated with a Product and the most common prices to configure are the general List and Current prices (the price Purpose) to be used for Purchase/Initial pricing (the price Type). Promotion configuration is associated with a Store and is applied based on the Store selected for each Sales Order. A Sales Order with no Store will still have price lookup and optionally price modify, but will not have promotions applied.

## Product Price Configuration

TODO

## Price Modify Services

TODO

## Promotions

### How Promotions Work

Each time an Order is modified in a way that might affect promotions (add items, edit item quantities and prices, change shipping information, etc) the system removes promotion discount items from the order and re-runs promotions. When running promotions the system will:

1. find all promotions configured for the Store selected for the Order where the Order Placed date (or current date if order not yet placed) is after the From Date and before the Thru Date on the promotion
2. run each promotion in order based on the Sequence Number (sorted ascending, ie lower numbers run first)
3. if **Require Code** is set to 'Y' on the promotion see if a Promo Code associated with the promotion has been entered for the Order, if not skip the promotion; if the Promo Code used has a **Limit Per Code** or **Per Customer** then check those limits and if reached then skip the promotion
4. if promotion has limits (**Limit Per Order**, **Per Customer**, **Per Promotion**) look up how many times the promotion has been used and if any of limits are reached then skip the promotion
5. run the promotion **Service** using the configured parameters; each promotion service does different things so from here behavior varies by the Service selected for the promotion

If any promotion is applied that has **Free Ground Ship** set to 'Y' and the Shipment Method for the Order Part is set to Ground then any configured automatic shipping calculation will be skipped so shipping is not charged.

### Finding and Creating Promotions

Promotions are configured for a Product Store in the Promotions tab of the Store screen ([demo](https://demo.moqui.org/qapps/marble/ProductStore/Promotion/FindPromotion?productStoreId=POPC_DEFAULT)).

Each promotion has an **Item Description** that is used as the Order Item Description when the promotion is applied. Each promotion also has a **Service** which defines the behavior of the promotion. Each promotion Service has parameters you can use to adjust behavior. There are a few standard promotion services to choose from and your system may have additional custom promotion services available.

Another important concept for all promotions is the **Seq Num** (Sequence Number). This is used to configure the order that promotions are applied. Higher value promotions should generally have lower sequence numbers so they are run before lower value promotions. Unless configured otherwise most promotions are only applied to order item quantities that have not already been used by another promotion. If you configure a lower value promotion to run first (lower sequence number) it will use up order item quantities so they can't be used by higher value promotions.

To create a promotion use the **New Store Promotion** dialog on the Promotions tab. In that dialog specify a Item Description, Service and From Date then click on the Create button. To go to an existing promotion just click on the ID or Item Description in the list of promotions.

### Standard Promotion Services

#### Buy X Get Y at Z% Discount

This is the most common type of promotion and covers promos like buy 1 get 1 free, buy 2 get 1 for 50% off, and with a Buy Quantity of 0 (zero) promotions like get 1 for 50% (a quantity limited percent discount).

This promotion service can be applied to a limited set of Products by adding one or more Products to the configured promotion. If no Products are configured for the promotion it will apply to any Product.

| Parameter | Description |
| ----------- | ----------- |
| Buy Quantity | Required. Quantity to buy to qualify for the discount but that does not get the discount applied. |
| Get Quantity | Required. Quantity that will receive the discount (must have at least Buy + Get in cart to apply). |
| Discount Percent | Required. Discount percentage such as 50 for half off, 100 for free; applies to Get quantity only. |
| Items With Promo | If *true* apply to product item quantities that already have another promotion (defaults to *false*) |
| Include Non Consumer | If *true* apply when customer has a classification other than Consumer (defaults to *false*) |

#### New Customer Discount

This promotion service adds a percent discount child item to each qualifying Order Item if this is the first order for the customer. If the Sequence Num of the configured promotion is higher than other promotions such as Buy/Get (so it runs after them) this will give new customers a discount on item quantities that do not get other promotions.

| Parameter | Description |
| ----------- | ----------- |
| Discount Percent | Required. Discount percent for new customers as a plain number like 10 or 25. |
| Items With Promo | If *true* apply to product item quantities that already have another promotion (defaults to *false*) |
| Include Non Consumer | If *true* apply when customer has a classification other than Consumer (defaults to *false*) |
| Require Account For Web | If true (default) for Web orders only apply if the customer has a User Account |

#### Flat Discount per Quantity

This promotion applies a discount amount per quantity. It is best limited by applicable products and with one or more use limits.

This promotion service can be applied to a limited set of Products by adding one or more Products to the configured promotion. If no Products are configured for the promotion it will apply to any Product.

| Parameter | Description |
| ----------- | ----------- |
| Discount Amount | Required. Discount Amount applied per quantity. Set limits per order and/or customer on promo or code (if no limit specified defaults to 1). |
| Items With Promo | If *true* apply to product item quantities that already have another promotion (defaults to *false*) |
| Include Non Consumer | If *true* apply when customer has a classification other than Consumer (defaults to *false*) |
