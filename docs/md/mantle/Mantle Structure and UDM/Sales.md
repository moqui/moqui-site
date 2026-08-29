# Sales
[TOC levels=2]

## Opportunity (mantle.sales.opportunity)

As part of sales force automation (SFA) use the SalesOpportunity to keep track of opportunities. An opportunity is typically associated with a certain sales stage (SalesOpportunityStage), and you can define any series of stages desired.

There may be many parties associated with an opportunity including the customer/prospect, sales representative, manager, etc. Record these with the SalesOpportunityParty entity. You could use this for competitors as well, but generally there is additional information for competitors so use the SalesOpportunityCompetitor entity for them.

An opportunity will often be associated with a quote, which may turn into an order. Use SalesOpportunityQuote to keep track of these. There may be meetings, other calendar events, or tasks associated with an opportunity and use SalesOpportunityWorkEffort to associate it with those.

There are a couple of touch points to marketing records. One is to a MarketingCampaign using SalesOpportunity.**marketingCampaignId**. Another is marketing TrackingCode records which are associated using the SalesOpportunityTracking entity. See the **Marketing** section for more details about these.

## Forecast (mantle.sales.forecast)

A SalesForecast may be for an entire internal organization (**organizationPartyId**) or a specific Party within that Organization (**internalPartyId**). It is associated with a TimePeriod and has amount fields including **quotaAmount**, **forecastAmount**, **bestCaseAmount**, and **closedAmount** for the final result.

Details about actual Product sold are recorded in SalesForecastDetail with a record with the sales **amount** and **quantity** sold for each Product and/or ProductCategory.

## Need (mantle.sales.need)

To record when a customer or other Party needs product (could be internal or external) use the PartyNeed entity. It can be for a Product and/or ProductCategory for needs that may be met by a variety or products, or when the exact product needed is not yet known. It often comes from a CommunicationEvent or through a web app with a Visit so there are fields for both.
