# Inventory Mover does Stock Move

Trigger: Based on touch frequency or other report showing a non-optimal location, move inventory to match frequency or other criteria (Optimize Locations)

## Ideas to Incorporate

## Dependencies

## Story

*(Bulk-to-Pick)* Inventory Mover gets a list of inventory items by Product ID and facility location (generated according to pick location where quantity drops below configured threshold). Inventory Mover moves inventory from bulk location to pick location according to list. Inventory Mover records actions to represent actual inventory moves (not listed ones). If Inventory Mover finds that inventory in the bulk location is short of system record during a stock move, Inventory Mover records moves of available quantity and records a physical inventory adjustment with difference between requested move amount and actual move amount.

*(Optimize Locations)* TODO
