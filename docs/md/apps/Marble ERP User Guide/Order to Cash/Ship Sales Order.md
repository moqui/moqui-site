# Ship Sales Order

[TOC levels=2]

## Introduction and Definitions

This document covers shipping a single Sales Order through the *Order Detail* and *Shipment Detail* screens. These screens have all options related to orders and shipments. For higher volume shipping with picklist management and a streamlined but limited packing screen see the [Shipping Management with Picklists](/docs/apps/POPC+ERP+User+Guide/Order+to+Cash/Shipping+Management+with+Picklists) document.

A Sales Order is ready for fulfillment (shipping) once it reaches the **Approved** status. Shipping is tracked through **Shipment** records. A Shipment may be created from an Order Part and other Order Parts may be added to an existing Shipment in the **Input** or **Scheduled** statuses with the same destination address, shipment method (ground, next day, etc), and ship from Party (the Vendor on the Sales Order). Partial order shipping is done by creating a Shipment from the Order Part and then reducing the Shipment Item quantities, leaving the remaining Order Item quantities available for adding to another Shipment.

## Create Shipments from Approved Sales Orders

1. the Order **Approved** status is the hand off between Sales (or Customer Service) and Shipping
1. start on the POPC ERP main Dashboard, click on the **Sales Orders** icon or link
1. now on the Find Order screen search for Approved Sales Orders
    - click on **Find Options** to open dialog
    - make sure Order Type is Sales
    - in Status clear out all except Approved
    - click on **Find**
1. click on an Order ID to view the Order
1. make sure the Order has adequate Payment and Shipping information
1. create one or more Shipments
    - an Order may have multiple parts
    - starting with the first Part click on **Create Shipment**
    - for other parts either Create Shipment or Add to Shipment
1. click on the **Shipment {ID}** button to view the Shipment

## Prepare Shipments for Pick

1. starting with a Shipment freshly created from an Order Part
1. click on **Set Scheduled**
1. review Order Notes if there are any relevant
1. review and optionally edit Shipping Instructions
1. review the Payments section to make sure order Credit Card payments are Authorized, if not refer back to customer service
1. review each Shipment Item and look at the asset reservation the system came up with
1. if needed use the **Reserve** button to select a different asset to reserve
1. once all reservations look good print the Pick PDF (general pick sheet) and/or Package PDF (for pick directly to packages)

## Pick Shipments

1. pick items from the shelf, and as I understand it put directly into boxes
1. optionally set the status to Picked (usually after picking, or skip this status altogether)

## Pack Shipments

1. with the boxes and printed Pick PDF and/or Package PDF in hand go to the POPC ERP Dashboard screen
1. enter the Shipment ID in the **Lookup By ID** field and hit enter (or scan the barcode on the Pick or Package PDF if you have a barcode scanner)
1. click on the **Shipment** button in the Shipment section
1. for each item click on the **Issue & Pack** button after verifying the quantity and optionally specifying the package it should go in
1. click on the **Set Packed** (now green) button at the top
1. if the order for the shipment was paid by credit card make sure the credit card payment capture was successful
  - look at the payment status which will be Delivered if capture was successful, or will remain as Authorized if it was not
  - if credit card capture was not successful set the package(s) aside and refer back to customer service to contact customer and arrange for payment

## Get Labels and Ship

1. review the Payments section to verify that Credit Card payments are captured, ie in the Delivered status
1. verify package info including which items are in which package by quantity, and the box type and weight on each package
1. unless a real Shipment Method has already been selected (ie a UPS, USPS, or FedEX one) select a real shipment method
    - Shipments are created with the Shipment Method from the Order Part and may have no carrier, such as the plain 'Ground Parcel' shipment method so a shipment method such as USPS First Class or Priority Mail needs to be selected
    - note that USPS First Class is limited to less than one pound (ie 15.99999oz max), a clue that this is the case is that no rate will come back from Shippo for USPS First Class
    - click on **Update Shipment** to save the selection
1. click on **Get Labels** at the top to get a label from Shippo for each Package
1. if there were any errors (shows 'ERROR' for Gateway in the Package header, and you'll get messages showing growl style)
1. click on **Print Labels** at the top to send the labels to the network label printer
1. if all looks well and you're ready to verify that it has shipped, and have the system send an email to the customer, click on **Set Shipped** at the top
