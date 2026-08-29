# Manufacturing Screens

NOTE: Production run screens described here are implemented in SimpleScreens Manufacturing (`/qapps/marble/Manufacturing`). Quotes and Orders, Costing, and Planning and Reports tabs were planned and are not in the current screen tree.

### Production Runs

- Find Production Run
    - create run dialog
    - find run form-list (WorkEffort with purposeEnumId=WepProductionRun)
- Run tab
    - main edit form (WorkEffort)
    - notes section
    - equipment section
    - parties section
- Products tab
    - for planning products to produce and viewing bill of materials break down
    - add product dialog
    - products to produce list/edit form
    - BOM breakdown and product/quantity to consume comparison, add
    - multi-level BOM breakdown with option to consume sub-assemblies vs raw materials
    - products to consume list form
- Inventory Consumed tab
    - record consumed inventory dialog (AssetServices.issue#AssetToWorkEffort)
    - consumed inventory list with return to inventory button/form (cancel asset issuance)
- Inventory Produced tab
    - record produced inventory dialog (AssetServices.receive#Asset)
    - produced inventory list with adjust button/form (update or cancel asset receipt)
- Tasks (Routing) tab
    - find task screen
        - add task dialog
        - list/edit tasks form, with status update and link to task screen (WorkEffortAssoc)
    - edit task screen
        - edit form (WorkEffort)
- Quotes and Orders tab
    - For RFQs (order in pre-placed statuses) and POs for outsourced manufacturing
- Costing tab
    - dialog to manually add cost (labor est, shipping, contract fees, etc)
    - dialog to add cost from payable invoice
    - automatically show cost from inventory consumed
    - automatically show cost from purchase invoices related to run (through purchase orders)

### Planning and Reports
