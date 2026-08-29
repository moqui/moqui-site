# Transfer Shipments

Transfer shipments are used to transfer inventory from one facility to another. They use pack and inventory issuance from the origin facility just like outgoing shipments as well as inventory receipt just like incoming shipments.

## Create, Pack and Ship a Transfer Shipment

- start on Find Shipment screen
- use the **New Transfer Shipment** dialog, specify from and to facilities
- while still in Input status add items (Product, Quantity) to transfer
- once all items added use *Set Scheduled* button to update status to allow pack/issue of inventory
- this shipment is not based on an order so there are no inventory reservations to pack against
- use the *Pack/Issue Item* dialog to select inventory to use and to pack and issue to the shipment
- once all items desired are packed use the *Set Packed* button to change status to Packed
- if a shipping label is needed
    - note that both origin and destination facilities must have an address set to create labels
    - assign quantities to packages as needed
    - use the *Update Package* dialog to set box type and weight
    - back at the top of the screen select the *Ship By* (carrier and service) to use and click on 'Update Shipment'
    - use **Get Labels** near the top of the screen or the **Get Label** button for each package to get labels
    - check label data per package to make sure it is what was expected
    - print labels with the *Print Labels* dialog for configured printers or use the *Download Label* button for each package to get a PDF to print locally
- once finished with all inventory packing and issuing use the 'Set Shipped' button to update status
- note that once in the Shipped status the Transfer Shipment goes into a mode where it is ready to Receive

## Receive a Transfer Shipment

- when the Shipment physically arrives at the destination Facility look up the Shipment by ID or other
- the Shipment should be in the Shipped status
- use **Receive Product** to receive into inventory in the destination Facility
- once all receipt is complete use the 'Set Delivered' button to update Shipment status
- note that once a Shipment is in the Delivered status no additional items may be received but existing receipts may be updated
