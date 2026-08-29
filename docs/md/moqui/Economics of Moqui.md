# The Economics of Open Source Business Software
[TOC levels=2-4]

## Market Price of Software Trends Toward Zero

Much of this applies to all software but the focus is on open source business software like Moqui.

The price of software (code) trends toward zero due to **collaboration** and **negligible cost to copy**. These break the supply & demand factors of pricing as software is not a naturally limited resource.

- *increased supply* (alternative software, not copy of software) reduces price via competition
- *increased demand* reduces price via collaboration (direct involvement or shared cost of improvement and maintenance)

While the price of software may trend toward zero the cost of creating and maintaining software is based primarily on the price of labor. Labor is a limited resource and the price of labor is driven by market supply and demand (decreasing with increased supply, increasing with increasing demand).

While the price of labor in software may vary it is bound:

- on the lower side by cost of living and operating for labor providers
- also on the lower side by the cost to labor providers (individuals and organizations) to acquire the knowledge and experience necessary to perform work
- on the upper side by the funding available to create and maintain software

With those natural economic constraints a given software package is only viable if the upper bound of funding available is higher than the lower bound of the cost of applicable labor.

The lack of a price signal to balance supply and demand of software causes two primary issues:

1. there is no price signal to represent the value of software (popularity reduces the price per user of software instead of increasing it)
    - with increased demand the most popular software will trend toward lower prices, not higher (opposite of market forces for limited resources)
    - choice among alternatives based on functionality and reduction of non-software (intellectual property) costs
2. with price trending toward zero there is less revenue from increased demand to fund improvement and maintenance of software

With these market forces at play commercial software (just the software) is not a viable long-term model. Software companies use various strategies to protect prices:

- increase cost to copy with intellectual property protection (limited by policy and enforcement available per jurisdiction, ROI on prosecution, etc)
- eliminate copy option by only leasing access, ie software only available as a hosted service (SaaS; software never leaves infrastructure of owner, plus IP protection)
- increase cost to switch away and decrease cost to switch to (PaaS; data policies and access, custom code and configuration with anti-WORA, inherent technical dependency)
- allow collaboration only via shared cost (don't allow direct involvement)

Software and platforms available only as a service (no copy option) are a viable model but still face price pressure from competitors, eventually leading to prices reduced toward the costs other than software that are naturally limited and will never go to zero.

## What Will Never Go to Zero

For business software, including Moqui, assuming adequate software exists to attract end users, what prices will never go to zero?

### Hosting

Software execution, data storage, and communication have a lower bound on price by cost of:

- server physical hardware (compute, storage, network, etc)
    - equipment cost: cost to acquire, naturally depreciates due to wear and obsolescence
    - labor cost: cost to monitor and maintain/repair
- internet bandwidth usage (nearly always shared: leased and/or metered)
    - natural equipment and labor costs like server hardware
- configuration, monitoring, software deployment (initial and updates)
    - labor cost: human effort required (beyond automation, software not counted as trends toward zero)

Hosting providers can increase profit by avoiding pricing models that are based only on a margin above cost. For internal applications (back office, ie ERP, CRM, etc) one example is a price per user. For public web sites and APIs one example is price per page view or transaction. With this sort of pricing, hosting providers have an incentive to make software more efficient (less hardware resources, bandwidth, etc) which becomes a natural channel for contribution to the software they host.

### Support

End user and technical support have a lower bound on price by cost of:

- support personnel
    - labor cost: cost of time to manage, review, and communicate with customers and upstream support
    - education cost: cost of time and external resources to acquire knowledge and experience
        - *in advance* or *on the fly* the cost must be passed on to customers to be profitable
        - resolution time and quality of service are competitive, depend largely on education
- upstream support cost - external support services
    - for on the fly education and issue categories that cannot, or by decision will not, be handled internally
    - ultimate backstop tends to be the analysts, designers, and developers who create the software
    - lower cost bounds similar to general support but higher education cost (leads to inherently lower supply)
- infrastructure and communication
    - equipment cost: per-person hardware
    - hosted systems cost: work management and communication
    - office space with furniture, internet service, etc; or subsidize home offices for remote workers

Support providers can increase profit by avoiding pricing models based on a margin above cost such as hourly billing. Hourly billing rates are often easiest to sell but are bad for customers as it tends to lead to insufficient education and therefore slow response times and poor service results. There is also little incentive to improve the underlying software to make it easier to support, and easier for customers to use so they need less support. Billing based on number of customer contacts and/or software users can be more profitable for providers, easier to plan/budget for customers, and gives an incentive to improve the software they support.

### Software Improvement

While software itself may trend toward zero price the price of improving and maintaining software will always be bound by costs.

The costs involved are mostly the same as the **Support** costs listed above for labor, education, upstream support, and infrastructure.

Software improvement skill sets often overlap with support services, both end user and technical support. Support services can be a good place to start for selling improvement services. The activities are very different, supporting the use of software that already exists and creating new software. The skill sets that overlap most are in analysis and design, understanding business context (processes, activities) and how the software is designed to be used in the business context. In theory an individual must know much more to document business context and design for it than to know how to use it, but in reality most analysts and designers learn as they go when creating new things. The overlap for developers is with technical support.

The overlap is stronger in the other direction where those who are involved with analyzing business context and designing software have already acquired the knowledge and experience necessary to support the software. This is why people who have done that can act as a backstop for support and not need upstream support themselves. A support organization could also build that knowledge and experience without having designed and built the software. In other words designing and building software is not a prerequisite for offering backstop support, but it is generally adequate to educate those who can then offer support services.

Software improvement naturally benefits the system software. That system software may be used by a single organization or shared among many. To the extent it is shared among many, the cost of specific functionality or systems in general may also be shared.

### System Usage

Using a system is generally an internal cost (mostly operating expense) and has no external price. One exception to this is the use of a business process outsourcing company that charges for services such as customer service, accounts receivable, fulfillment, or pretty much any business activity.

Every business activity that involves system interaction (viewing or changing data) requires human time so there is always a labor expense. The primary value proposition of business systems is to reduce human labor so that organizations can operate at higher scale with lower expenses. Some business activities like accounting and reporting benefit more from data automation than others.

One way to think of this is by comparing computer systems to paper systems. Paper processes often involved large banks of filing cabinets with information, duplicated across departments, and with a single taxonomy for indexing and retrieval (like customer files sorted alphabetically by name). Being able to look up a customer by name, phone number, email address, postal address, etc and have the records immediately available makes a huge difference in the time required to perform all sorts of business activities. In accounting there is even greater business benefit for things like automated posting. In paper accounting ledgers, information would be manually copied from invoice, payment, and other documents to account ledgers, and ledger balances had to be maintained manually. If ledger entries were ever changed it was a nightmare to recalculate; errors were often not corrected and instead additional adjusting records were added. Paper reports had to be compiled manually from the paper account ledgers. Auditing and analyzing accounting records was a great deal of work, manually comparing and reconciling paper records.

This may seem to be a focus on bottom-line operational expenses, leaving out investment in software for the purpose of increasing revenue. Increasing revenue generally involves business activities that are part of marketing and sales processes. Those are still just business activities and just like operating expenses can be done with any sort of system, even paper or spreadsheets, so the focus for software systems is still on increasing efficiency.

Another common topic is increasing efficacy or quality of work and information. Software systems can enforce (by hard errors) or encourage (by defaults, warnings, etc) certain types of business policies. Ultimately those business policies are also just business activities that could be done manually (and in the past with paper processes were done manually, helped by form designs). Being able to enforce, encourage, and audit policies without having to do it all manually is much more efficient with software systems, another value add in terms of increasing efficiency.

That is more than is needed for an analysis of costs related to system usage. The important point is every business activity has a cost to perform. In paper systems the cost was designing and printing forms, filing systems, etc. In computer systems the costs are the software, hosting, support, etc. Factoring those out to make it easier to compare costs, the primary cost to consider is human labor.

More generally the costs are essentially the same as the **Support** costs listed above for labor, education, upstream support, and infrastructure.

Every organization that uses a system has a natural incentive to improve the system to enable scale and reduce operating expenses. In computer-based systems this is a natural incentive to improve software, mostly to reduce the human time (labor cost) required for each business activity. The priorities for improving software are based mostly on the frequency of each business activity but may also be based on general business objectives and strategy. The cost of software improvements is justified mostly by an increase in operational efficiency so the price of software improvements is inherently limited by how much may be saved by an end user organization.

A smaller end user organization or business process outsourcing company may not have the resources or the potential reduction in expenses to pay the price of software improvement. There are two main ways of getting around this:

1. find and pay for commercial software that already meets your very specific needs (generally requires a great deal of analysis, is usually not done so only starting after using a system do mismatches surface); this is the collaboration via funding approach, there may be some influence requesting features
2. pool funds from other users, directly or indirectly, to fund improvements that can be shared

## Useful Links

[The Marginal Cost of Software by Basab Pradhan](https://www.enterpriseirregulars.com/31274/the-marginal-cost-of-software/)

[Software Has Marginal Cost by Bob Warfield](https://www.enterpriseirregulars.com/31273/software-has-marginal-cost/)

[Digital Economics: The Zero Marginal Cost Economy by Nathan Taylor](https://praxtime.com/2013/01/06/digital-economics-the-zero-marginal-cost-economy/)
