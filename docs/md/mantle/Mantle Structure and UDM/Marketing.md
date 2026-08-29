# Marketing
[TOC levels=2]

## Campaign (mantle.marketing.campaign)

A MarketingCampaign is used for general tracking of marketing efforts and may be used for efforts that tracked in the system, or may be used to group other things like ContactList, TrackingCode, and SalesOpportunity.

A campaign has various budget/cost fields including **budgetedCost**, **actualCost**, and **estimatedCost**. It is valid within an optional date range (**fromDate**, **thruDate**). For campaign results there are fields like **convertedLeads**, **expectedResponsePercent**, and **expectedRevenue**.

A campaign may have various parties like marketers, sales reps, managers, prospects, and leads associated with it using MarketingCampaignParty. Use the MarketingCampaignNote entity to track notes about the campaign, which are in addition to the **campaignName** and **campaignSummary** fields on the campaign itself.

## Contact (mantle.marketing.contact)

A ContactList is used to plan and track mass outgoing communication such as Marketing, Newsletter, and Announcement (**contactListTypeEnumId**). This can be by email, phone, postal mail, or any other means of contact (**contactMechTypeEnumId**). It may be associated with a MarketingCampaign (**marketingCampaignId**).

A contact list is generally owned/managed by a particular Party (**ownerPartyId**). Other parties are associated with it using ContactListParty. The main use for this is parties who will receive the outgoing communication and optionally how they should be contacted (**preferredContactMechId**). Most emailing lists are opt-in and this is often done with an outgoing email to verify the address and the opt-in with a code, which is tracked for verification with the **optInVerifyCode** field.

A ContactListParty has a status (**statusId**) which may be Pending Acceptance, Accepted, Rejected, In Use, Invalid, Unsubscribe Pending, or Unsubscribed.

To configure outgoing email for the list, including types (**emailTypeEnumId**) such as Subscribe Notification, Unsubscribe Verify, Unsubscribe Notification, and Outgoing Email use the ContactListEmail entity. This points to a Moqui EmailTemplate record (with **emailTemplateId**) to be used with the org.moqui.impl.EmailServices.**send\#EmailTemplate** service.

To track actual communication use a CommunicationEvent record associated with the contact list using ContactListCommStatus. Use this to track the Party (**partyId**) and actual ContactMech (**contactMechId**) used, though further details are on the CommunicationEvent record. See the **Communication Event (mantle.party.communication)** section for additional details.

## Segment (mantle.marketing.segment)

The MarketSegment and related entities are used to define a group (segment) of Party records by PartyClassification using MarketSegmentClassification, by Geo (geographic boundary) using MarketSegmentGeo, and by Organization parties using MarketSegmentParty for all parties in the organization.

A segment can be used for many purposes such as populating ContactListParty records based on all current Party records in the system that match the segment criteria or recording interest in a set of products in a ProductCategory using the MarketInterest entity.

## Tracking (mantle.marketing.tracking)

A TrackingCode can be used for internal path tracking for critical web pages or for AB or other multivariate testing. It can also be used to track incoming links from affiliates for particular orders to pay affiliate commissions.

Once a tracking code is in the system it can be associated with a Moqui web Visit using TrackingCodeVisit, with an order (for conversion tracking and affiliate commissions) using TrackingCodeOrder and with returns using TrackingCodeOrderReturn.

For affiliate commissions that follow browser cookie preservation rules the tracking code is generally put in a cookie and then pulled from the cookie when an order is placed as opposed to remembering it through more means. The tracking codes associated with a Visit are different, they are generally all tracking codes used during a Visit and orders can then be tied to these through the **visitId** field on OrderHeader.
