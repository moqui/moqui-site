
# Product Store Screens

- Find Store (default screen, not in menu/tabs; FindProductStore)
    - create dialog with simple form (productStoreId, storeName, organizationPartyId; leave rest for edit form)
    - store list with ID, name, org
- Store tab (EditProductStore)
    - Edit ProductStore form
    - Shipping Options section with add and list forms (ProductStoreShipOption; in right column)
    - Shipping Gateways section with add and list forms (ProductStoreShippingGateway; in right column)
    - Payment Gateways section with add and list forms (ProductStorePaymentGateway; in right column)
- Promotions (tab with sub-tabs)
    - Find Promotion screen (default, not in menu/tabs)
        - create dialog with basic create form
        - list form to find
    - Promotion (EditPromotion)
        - edit form (for ProductStorePromotion)
        - parameters section
            - list/edit parameters form
            - use Moqui API to get ScreenDefinition object to get in-parameters, pretty print names, show descriptions
            - have in-parameters list be the list for the form-list, ie show all and fill in stored values if there is one
            - create/update values on submit in ProductStorePromoParameter entity
    - Promo Codes (tab with sub-tabs)
        - Find Promo Code
            - create dialog with basic create form
            - list form to find
        - Promo Code (single screen, no tabs)
            - edit form (ProductStorePromoCode)
            - parties section, list with add form (ProductStorePromoCodeParty)
    - Promotion Stats (based on OrderItem records, for orders Approved or later)
- Emails
    - Find/Edit form-list (ProductStoreEmail)
- Categories
    - Find/Edit form-list like on Product/EditCategories.xml (ProductStoreCategory)
- Parties
    - Find/Edit form-list (ProductStoreParty)

### Gateways

(basic crud screens, link to from Find Store; details edited here to keep gateway selection on Store screen simple)

- Find Payment Gateway
- Edit Payment Gateway
    - general edit form (mantle.account.method.PaymentGatewayConfig)
    - depending on type, options form for Authorize.NET, Braintree (the 2 currently implemented)
- Find Shipping Gateway
- Edit Shipping Gateway
    - general edit form (mantle.shipment.carrier.ShippingGatewayConfig)
    - form for Shippo options
