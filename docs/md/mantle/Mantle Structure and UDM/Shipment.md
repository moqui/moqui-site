# Shipment
[TOC levels=2]

## Shipment (mantle.shipment)

The Shipment and related entities may be used for both Incoming and Outgoing shipments (**shipmentTypeEnumId**), and more specifically for Sales Return, Sales Shipment, Purchase Shipment, Purchase Return, Drop Shipment, and Transfer shipments. A Shipment is generally from one Party (**fromPartyId**) and to another (**toPartyId**). If needed put special instructions in the **handlingInstructions** field.

For planning purposes a shipment may have **estimatedReadyDate**, **estimatedShipDate**, **estimatedArrivalDate**, and **latestCancelDate** values. For further detail or to get the shipment in a calendar as an event use the **shipWorkEffortId** and **receiveWorkEffortId** fields to point to WorkEffort records. There is typically some sort of estimated cost for the shipment, track that in **estimatedShipCost** with its currency in **costUomId**. If the cost is adjusted use the **addtlShippingCharge** field along with a description of the additional charge in **addtlShippingChargeDesc**.

For the entire Shipment there is a **statusId** that may be Input, Scheduled, Picked, Packed, Shipped, Delivered, Rejected, and Cancelled. This field is audit logged for a status history. The **Packed** status is one of the more important as it is the point where the shipment is generally considered fulfilled for billing purposes. The change to the Packed status is used to trigger Invoice creation for the order(s) on the shipment, and if applicable automated payment processing.

Each shipment has ShipmentItem records with a **quantity** for each Product (**productId**) in the shipment.

A Shipment always has one or more packages (ShipmentPackage) and the **quantity** of **productId** in each package is recorded with ShipmentPackageContent. Each package may have the box used (**shipmentBoxTypeId** pointing to a ShipmentBoxType record), and the total shipping **weight** of the package along with the unit for the weight (**weightUomId**).

A Shipment also always has one or more route segments (ShipmentRouteSegment). Consumer fulfillment and most simple shipments involve a single route segment with a carrier (**carrierPartyId**) and shipment method (**shipmentMethodEnumId**) going from a certain origin (**originPostalContactMechId**, **originTelecomContactMechId**) to a destination (**destPostalContactMechId**, **destTelecomContactMechId**). A shipment may also have other contact information associated with it using the ShipmentContactMech entity.

For consumer fulfillment the origin will usually be a warehouse Facility and specified with **originFacilityId**. For consumer returns or inventory purchase shipments they will generally go to a Facility, recorded in **destinationFacilityId**. There are various dates associated with a route segment including **estimatedStartDate**, **estimatedArrivalDate**, **actualStartDate** and **actualArrivalDate**.

Each package will have certain details for each route segment (ShipmentPackageRouteSeg) including **trackingCode**, **boxNumber** (within the shipment, if applicable), and labels/documents including **labelImage**, **labelIntlSignImage**, **labelHtml**, **labelPrinted**, and **internationalInvoice**.

For billing purposes each package in a route segment (ShipmentPackageRouteSeg) has an **estimatedAmount** for the estimate before getting a quote or actuals from the carrier, plus **packageTransportAmount**, **packageServiceAmount**, and **packageOtherAmount** for actuals from the carrier, along with **codAmount** and **insuredAmount** for those special situations. All of these use the currency specified in **amountUomId**.

For all packages in a route segment (i.e., on ShipmentRouteSegment) there are fields for the totals in **actualTransportCost**, **actualServiceCost**, **actualOtherCost**, and **actualCost** with the currency in **costUomId**. The route segment also has a total **billingWeight** with **billingWeightUomId** that includes the billing weight used from all packages for the route segment. A route segment also has a status (**statusId**) that is mostly used for keeping track of communication (usually by integration) with the carrier, including: Not Started, Confirmed, Accepted, and Voided.

A Shipment is generally based on one or more orders or returns, and generally results in one or more invoices being produced. The ShipmentItemSource entity is used to keep track of these, and there may be more than one ShipmentItemSource for each ShipmentItem record. More specifically a shipment item may be associated with multiple order items (**orderId**, **orderItemSeqId**) or return items (**returnId**, **returnItemSeqId**) and is generally associated with one or more invoice items (**invoiceId**, **invoiceItemSeqId**).

There is a ShipmentItemSource.**quantity** field to specify how much of the ShipmentItem.**quantity** comes from the specified order or return item. There is also a quantityNotHandled field on the source to specify how much of the quantity should have been shipped but was not.

Shipment has **binLocationNumber** (and **shipWorkEffortId** for the picklist WorkEffort), and ShipmentItemSource has **binLocationNumber** and **statusId** fields to use for picking and packing in a warehouse. See the **Picklist (mantle.shipment.picklist)** section below for details.

### Picklist

A Picklist is used to organize pending Shipment records for a pick/pack process. There is no separate picklist bin structure, instead Shipment itself is used. Similarly there is no picklist item, the ShipmentItemSource is used to track items in a pick "bin" and details about the order, return, and invoice that the particular quantity of the item are associated with.

For a Shipment in the Input or Scheduled statuses the Shipment.**shipWorkEffortId** points to the Picklist (or Ship Load) WorkEffort it is on. A picklist is always associated with a Facility (**facilityId**) and may be associated with a particular shipment method (**shipmentMethodEnumId**) for planning and processing fulfillment by shipment method. For management and historical tracking purposes Picklist WorkEffort has various date/time fields. Parties in a particular role such as Picker, Packer, Manager, etc may be associated with the picklist using WorkEffortParty.

In a typical picking process multiple shipments are picked at the same time, with the contents put into a bin. This is tracked with the Shipment.**binLocationNumber** field unless the shipment is split into multiple bins (like one bin per order on the shipment) and then the ShipmentItemSource.**binLocationNumber** field is used to override the one on the Shipment record.

The ShipmentItemSource entity has the OrderItem details (**orderId**, **orderItemSeqId**) to lookup related AssetReservation records that have the **quantity** (or **quantityNotIssued** if used) to pick and the corresponding Asset to find the FacilityLocation that the asset is stored in for picking.

ShipmentItemSource has a status (**statusId**) for picking and packing purposes that can be Pending, Picked, Packed, Received, or Cancelled. Note that the Received status goes beyond the typical pick/pack process to track receipt of items when that data is available and needed.

A typical pick sheet will have a list of all facility locations to pick from listed in order of their location for easy walking of the floor to pick all shipments on the list. For each location the product and quantity to pick are listed along with the pick bin number and the quantity for that bin to get the right number of items in the bin for the right shipment (or order). The series of entities above is used to get all of those details.

![MantleDataModel-shipment](/docs/attachment/100471/MantleDataModel-shipment.svg)

## Carrier (mantle.shipment.carrier)

A carrier is typically a company like UPS or FedEx. Use CarrierShipmentMethod to configure which carriers (**carrierPartyId**) support which shipment methods (**shipmentMethodEnumId**) and the carrier’s service code (**carrierServiceCode**) and Standard Carrier Alpha code (**scaCode**) for the method.

Similarly CarrierShipmentBoxType is used to configure the ShipmentBoxType (by **shipmentBoxTypeId**) records for a carrier and their corresponding **packagingTypeCode** and if applicable **oversizeCode**. The method and box codes are all typically used for carrier integrations to specify the service level and boxes using codes that the carrier supports.

If a Party has an account with a carrier track that using the PartyCarrierAccount entity.

The ShippingGatewayConfig entity is used to specify details for an integration with a carrier for purposes of shipping estimates, rate quotes, getting labels, voiding labels, tracking packages, and even validating addresses. To implement a shipping gateway (carrier integration) implement services for each of these and create a record that points to them, then associate that with a ProductStore using the ProductStoreShippingGateway entity.
