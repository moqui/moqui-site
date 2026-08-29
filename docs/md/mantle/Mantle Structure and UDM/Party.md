# Party
[TOC levels=2]

## Party (mantle.party)

The term party in this case has a meaning like the legal term of a party to a lawsuit as in an individual or group, not the fun kind of party. There are two types of party and each has its own entity to add applicable detail to the Party entity: Person representing an individual and Organization which is a group and each member of the group may be a person or organization. These entities have the same primary key field as the Party entity (**partyId**) so that they have a one-to-one relationship.

The name of a Party comes from different fields depending on its type. For organizations it comes from the Organization.**organizationName** field. For persons (people) it comes from multiple fields on the Person entity: **salutation**, **firstName**, **middleName**, **lastName**, **personalTitle**, **suffix**, and **nickname**. Usually at least first and last names are used, and the others less commonly. There are various other fields on Party, Person, and Organization to specify details about parties, and just like any other entities you can extend these to add any others you might need.

Each party may have zero to many roles that are used to define how a party relates to other structures in the system such as orders, work efforts (tasks, etc), agreements, and even other parties. The available roles are defined using the RoleType entity and there is a fairly comprehensive set of them defined OOTB in Mantle. Some examples of roles include: carrier, bill-to customer, ship-from vendor, employee, affiliate, and spouse.

A role can be associated with a party using the PartyRole entity. Entities that have a **partyId** and a **roleTypeId** intentionally have foreign keys just to Party and RoleType and not to PartyRole so that PartyRole records are optional. In some cases it is useful to see if a party is in a certain role, and PartyRole is the entity you would use for that.

Relationships between parties are recorded with the PartyRelationship entity. These include members of a group, employees of an organization, organization hierarchies (rollup), contacts, friends, and so on. There are various OOTB relationship types for the **relationshipTypeEnumId** field, and you can add more by adding Enumeration records with **enumTypeId**=PartyRelationshipType. In addition to the relationship type there are from and to party and role type fields that detail the nature relationship. When needed there are also effective date (**fromDate**, **thruDate**) fields and a **statusId** field (which like most statuses is has **enable-audit-log**=true for a status history).

A party may have multiple identifiers such as a driver license number, employee number, and external system identifiers for correlation. These are stored with the PartyIdentification entity. This entity has an **idValue**, a **partyIdTypeEnumId** for the type of ID, and an optional **expireDate** for identifiers that expire.

Party classifications are used to classify parties by industry/SIC/NAICS, size, revenue, minority/EEOC, etc. Each PartyClassification (such as the NAICS industry classification 541511 - Custom Computer Programming Services) has a **classificationTypeEnumId** (such as PctNaicsCode) and optional **parentClassificationId** to organize them. Use the PartyClassificationAppl entity to associate a party with a classification in a date range (**fromDate**, **thruDate**).

A party can be have associated Resource Facade content with PartyContent, geographic points with PartyGeoPoint, and notes with PartyNote. A party may be associated with a Moqui Framework UserAccount with the UserAccount.**partyId** field that Mantle adds to it using extend-entity.

![MantleDataModel-party](/docs/attachment/100467/MantleDataModel-party.svg)

## Agreement (mantle.party.agreement)

Agreement is used to track sales, employment, commission, and other types (**agreementTypeEnumId**) of agreements. An agreement is typically between two parties (**fromPartyId**, **toPartyId**) and those parties may be in specific roles (**fromRoleTypeId**, **toRoleTypeId**). Additional parties may be associated with it using the AgreementParty entity. Parties may also be associated with a specific item on the agreement using the AgreementItemParty entity.

An agreement is made on a certain date (**agreementDate**) and is valid within a date range (**fromDate**, **thruDate**). You can record a **description** for the agreement and the full text in **textData** if available.

An agreement is detailed with one or more AgreementItem records that have most of the structure around an agreement. An item may have its own detail text (**itemText**) and its own effective date range (**fromDate**, **thruDate**). An item will typically have a type (**agreementItemTypeEnumId**) such as Sub-Agreement, Pricing, Section, or Commission Rate. When relevant the currency for an item is tracked with the **currencyUomId** field.

If an agreement is changed it should be tracked with an addendum using the AgreementAddendum entity, which can be applied to a particular item or the entire agreement.

An item or the entire agreement may also have terms, recorded with the AgreementTerm entity, such as Payment, Fee, Penalty, Incentive, Termination, Indemnification, Commission, and Purchasing terms. There are various others defined and you can define more by adding Enumeration records with the type TermType. These are also used for BillingAccount and for Invoice through the SettlementTerm entity.

Use AgreementItemGeo to associated an item with a specific geographic boundary (Geo), and AgreementItemWorkEffort for a WorkEffort such as a project. When an agreement (item) is for employment, associated the item with the Employment record using AgreementItemEmployment.

For product pricing agreement items the ProductPrice has **agreementId** and **agreementItemSeqId** fields to point to an AgreementItem. This provides structured detail about the pricing, and can be used for automated price calculation for a particular order.

## Communication Event (mantle.party.communication)

Use CommunicationEvent to keep track of communication between parties (**fromPartyId**, **toPartyId**), optionally in particular roles (**fromRoleTypeId**, **toRoleTypeId**), and also optionally with specific contact mechanisms (**fromContactMechId**, **toContactMechId**; see the next section for ContactMech details). Even if there are not specific contact mechs associated with the communication event the type (**contactMechTypeEnumId**) such as phone/telecom number or email address can be.

In addition to the from and to parties other parties, along with a role and contact mech, can be associated with the CommunicationEvent using the CommunicationEventParty entity. This is especially useful for events like meetings and conference calls.

Communication event types are specified with the **communicationEventTypeId** field on the CommunicationEvent entity which points to a CommunicationEventType record. These types correlate to contact mech types. For example the phone comm event type is associated with the telecom number contact mech type using the **contactMechTypeEnumId** attribute on the CommunicationEventType entity.

CommunicationEvent has a status (**statusId**) for both incoming and outgoing events including In Progress, Ready, Sent, Received, Viewed, Resolved, Referred, Bounced, Unknown Party, and Cancelled. These statuses should handle most situations, including inbound email queues that need to be viewed and acted on (resolved). For status history this field use the Entity Facade audit log. The time of special events are tracked on the **entryDate**, **datetimeStarted**, and **datetimeEnded** fields.

Communication events are hierarchical to handle threaded discussions with a **parentCommEventId** to track the previous or parent comm event, and the **rootCommEventId** to tie all comm events to the comm event that initiated the thread.

If available the content of the comm event can be stored with the **subject**, **contentType** (MIME type), and **body** fields with any notes about it in the **note** field. For records from email messages the **Message-ID** header that identifies the email can be recorded with the **emailMessageId** field. Additional content can be saved in a Resource Facade location and associated with the comm event using the CommunicationEventContent entity.

One or more purposes, such as Customer Service and Sales Inquiry, for the comm event can be tracked with the CommunicationEventPurpose entity (separate entity so that multiple purposes can be associated with the comm event). The purpose is specified with the **purposeEnumId** field which points to Enumeration records of type CommunicationPurpose, so use the enum type to add more available purposes.

When relevant products may be associated with a comm event using the CommunicationEventProduct entity.

## Contact Mechanism (mantle.party.contact)

A contact mechanism is a means of contacting a party. The primary entity is ContactMech and while there are various types only two have entities with additional fields: PostalAddress and TelecomNumber. The remaining types (such as email address) use the ContactMech.**infoString** field.

The primary key field of ContactMech is contactMechId. Like the pattern with Party, Person, and Organization the ContactMech, PostalAddress, and TelecomNumber entities share the same primary key field so they have a one-to-one relationship.

The PartyContactMech entity is used to associate a ContactMech with a Party. A purpose (**contactMechPurposeId**) describes what the ContactMech is for the Party such as destination shipping address or billing phone (telecom) number. The purposes are defined as records in the ContactMechPurpose entity. There is a comprehensive set available OOTB and you can add records to define more.

PartyContactMech has effective date (**fromDate**, **thruDate**) fields to define the date range where the ContactMech is valid for the Party. ContactMech records are immutable (they should never be changed) so that they can be referenced in other places without a change unintentionally effecting other places (and to keep a history of contact information). When one needs to be updated a new record is created and associated with the Party and the **thruDate** is set on the old PartyContactMech record to expire it. See the mantle.party.ContactServices.**update\#PartyContactOther** service for details of how this is done (and there are similar services for postal addresses and telecom numbers to handle the additional fields and separate entities).

Where fraud is a concern the ContactMech should have a **trustLevelEnumId** set. OOTB options include New Data, Valid/Clean (through 3rd party service), Verified (with outbound contact or authorization), Greylisted, and Blacklisted. If the trust level is Greylisted or Blacklisted there should be a **paymentFraudEvidenceId** pointing to a PaymentFraudEvidence record with details about why.

Another entity that uses ContactMech similar to Party is mantle.facility.Facility. A facility has contact information just like a party and is a long-lasting record with multiple contact mechs that may change over time. Just like for Party there are services to update contact mechs for a facility (see the mantle.facility.ContactServices services) that expire the old record and create a new one.

There are many entities which refer to contact mechs, and some which use a join entity to associate multiple contact mechs with different purposes. These include InvoiceContactMech, OrderContactMech, ReturnContactMech, ShipmentContactMech, and WorkEffortContactMech. These entities do not have effective date (**fromDate**, **thruDate**) fields as they are short-lived and if contact information changes the **contactMechId** is simply updated to point to a different record.

![MantleDataModel-party.contact](/docs/attachment/100467/MantleDataModel-party.contact.svg)

## Time Period (mantle.party.time)

The TimePeriod entity is for custom time periods, as opposed to calendar time periods, such as fiscal years/quarters/months and sales quarters (**timePeriodTypeId**, references the TimePeriodType entity). They may match calendar time periods, i.e. **fromDate** is the beginning of a calendar period and **thruDate** is the actual end of the calendar period, but are referenced anyway for any functionality that allows the time period to be something other than a calendar period.

A time period can be linked to its parent (**parentPeriodId**) and previous (**previousPeriodId**) time periods. It can also be associated with a Party (**partyId**) for things such as fiscal time periods that are specific to an organization for accounting purposes. When a TimePeriod is used for the general ledger the **isClosed** field specifies when the period is closed and transactions can no longer be posted to it.
