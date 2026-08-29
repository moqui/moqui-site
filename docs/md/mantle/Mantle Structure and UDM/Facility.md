# Facility

## Facility (mantle.facility)

A facility is a building, unit, room, land or even floor space. There are also more particular types of facility such as warehouse and office. The primary entity for a facility is what you would imagine (Facility) and it is identified by a single PK field (**facilityId**). As with many of the main (master) entities a facility has a type (**facilityTypeEnumId**), status (**statusId**), and name (**facilityName**). There are also fields for the owner, size, open/close dates, etc.

Facilities are hierarchical to model things like units within a building and rooms within a unit. The Facility.**parentFacilityId** field is used to specify the parent for each facility. In theory this could be used for things like warehouse inventory locations but to simplify and flatten that structure the FacilityLocation entity is just for inventory locations within a facility. These have a type (such as bulk or pick/primary), locator fields (**areaId**, **aisleId**, **sectionId**, **levelId**, and **positionId**), and even a **geoPointId** for GPS-driven automation.

A Product may be associated with a FacilityLocation using the ProductFacilityLocation entity to record which products go in which locations, and to set **minimumStock** and **moveQuantity** values to use for recommended stock moves (when replenishing pick/primary locations from bulk locations). If you need to track more data about a particular product in a particular location extend this entity.

Similarly a Product may be associated with a Facility using the ProductFacility entity to specify **minimumStock** and **reorderQuantity** values for use in simple automated (recommended) replenishment. Other fields related to a particular product in a particular facility can be added to this entity as needed.

The physical location of a facility can be recorded in two ways: through a GeoPoint record referenced by the Facility.**geoPointId** field, or in a PostalAddress type of ContactMech with the FacilityContactMech. FacilityContactMech can also be used for more general contact information for the facility including phone/fax/etc (telecom) numbers, email and web addresses, and even multiple postal addresses when there are different ones for things like receiving correspondence, receiving shipments, shipping return address, etc.

For more details about ContactMech see the **Contact Mechanism (mantle.party.contact)** section.

Use the FacilityParty to associate a party (**partyId**) with a facility (**facilityId**) in a particular role (**roleTypeId**) and within an effective date range (**fromDate**, **thruDate**). This can be used for any role and might be used to record who is an owner, tenant, occupant, manager, picker, packer, etc for a particular facility.

To associate Resource Facade content (with a **contentLocation**) with a facility use the FacilityContent entity. This has a content type (**facilityContentTypeEnumId**) such as internal content (documents, etc) and images, and the ever useful effective date range (**fromDate**, **thruDate**).

To organize facilities for pricing or management purposes, or more generally to keep better track of large numbers of facilities, use FacilityGroup. Facility groups have a **description**, are hierarchical (**parentGroupId**) and have a type (**facilityGroupTypeEnumId**) such as management structure or pricing group. To associate a Facility with a FacilityGroup use the FacilityGroupMember entity. You may also associate a party in a particular role with a facility group with the FacilityGroupParty entity.

![MantleDataModel-facility](/docs/attachment/100463/MantleDataModel-facility.svg)
