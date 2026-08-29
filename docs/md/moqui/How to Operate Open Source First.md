# How to Operate Open Source First

[TOC levels=2]

## Audience and Scope

* Target Audience
    * End-user Organizations with operational and strategic requirements
    * Proprietary software providers filling customer requirements
    * Service providers working on client requirements
    * Open source project maintainers
* Scope
    * Business and infrastructure software
    * Granular system and tool selection
    * Customization and enhancements
    * Maintenance, training, and support
* References
    * Open Source Definition: [https://opensource.org/docs/osd](https://opensource.org/docs/osd)
    * Dell EMC Strategy: [https://blog.dellemc.com/en-us/open-source-first-strategy/](https://blog.dellemc.com/en-us/open-source-first-strategy/)
    * Linux Foundation: [https://www.linuxfoundation.org/resources/open-source-guides/setting-an-open-source-strategy/](https://www.linuxfoundation.org/resources/open-source-guides/setting-an-open-source-strategy/)

## What is Open Source First?

* Default open source, justify proprietary
* Comedy of the Commons
    * Tragedy of the Commons
    * Enlightened Self-Interest
    * Limited vs easily reproduced resources (software!)
    * Consumed as-is vs Used with maintenance and improvement over time
* Collaborate directly (participate in community) over indirectly (purchase from vendor)
* Share your code, own your data (configuration, transactional, etc)
* Does not mean 100% open source

## Why Operate Open Source First?

* Collaboration opportunity
    * effectively equivalent requirements
    * similar (but different!) requirements
    * collaboration via communication and via code
    * use code, documentation, archives for read-only collaboration
* Avoid 'stuck in time' syndrome
    * proprietary modifications tend to build up over time
    * difficult and expensive to merge upstream changes
    * end up with general higher cost of maintenance
    * security risks unless carefully monitored and fixes manually back-ported
* Stand on the Shoulders of Giants! (well, peers really)
    * no crystal towers isolated from the world, it's all open
    * discover important requirements not yet considered
    * avoid over-fitting requirements
    * configure and use instead of build and maintain
* Money, time (money), and resources (money)
    * design risk: single greatest factor in overall cost
    * meet more requirements with less implementation cost
    * shared maintenance, community support
    * generic documentation, customize and reference

## Perceived and Actual Conflicts of Interest

* From experience actual conflicts extremely rare
* Cui Bono? Me! And You. And Future Me. And Future You.
    * Enlightened Self-Interest and Comedy of the Commons
    * Bigger picture: don't miss the forest for the trees
    * Different frame of thought required
* Conflicting requirements vs designs
    * Can almost always design around conflicting requirements
    * Design conflict is often a sign of poor quality design
* Effective, Quality Design
    * Consider current and potential future requirements
    * Predicting the future and identifying unknowns is HARD
    * Other organizations can be a proxy for your own future
    * Broaden your vision with requirements and designs from others

## Proprietary Justifications

* Even if Open Source First from top management down there are reasons for proprietary
* Based on confidential information
    * valid business concern, sometimes misguided application
    * actual NDA criteria, not attempts to include common practice or prior art
    * many seemingly great ideas end up being common practice or bad ideas, worth researching
* No potential for collaboration
    * target organizations unable to participate due to internal skill set and budget for external services
    * target market too small for likely third party participation
* Competitive differentiation
    * cost of design, implementation, maintenance, etc far less that differentiating market value
    * easy to overuse as a justification
    * balance against risk of opportunity cost as others choose to do the same as open source, often better with more collaboration

## Development Process

* Start with business requirements
    * from a system perspective: processes and actor/action based activities to support
    * from a business perspective: SOPs, a business 'design' based on objectives
* Gap/overlap analysis against requirements
    * the only way to achieve reuse and designs that satisfy a wide variety of requirements
    * gap/overlap based on designs will inherently result in mostly gaps
* Design based on existing artifacts
    * changes to existing system and user interfaces instead of clean slate designs
    * leverage and modify or extend existing logic and data structures
* Begin community collaboration with requirements and designs, don't wait for implementation
* Implement with intent to release as open source
    * consider structure of code and other artifacts
    * use repositories to help manage code (see Code Management below)
    * consider backward compatibility, use configuration options for different behavior
    * keep code clean and follow established practices to facilitate collaboration and maintenance

## Code Management

* Change only for contribution, keep customization separate
    * use open source repo directly (immediate contribution)
    * fork for stabilization and/or deferred contribution
* Fork repositories for proprietary changes
    * in some cases easier to maintain and update than separate repo
    * risk and complexity from mixed proprietary and intended open source
* Proprietary repositories
    * for overrides, extensions, independent functionality, etc
    * good place to house common configuration data (files and DB records)
    * kept clearly separate
* Which is best?
    * depends on objectives
        * open source vs proprietary
        * immediate vs deferred contribution
        * similar (small change) vs very different or new
    * testing and deployment considerations
    * nice to decide first but can always refactor
    * for Open Source First default to top of list, justify

## Transitioning to Open Source First

* Establish an Open Source First policy
* Review existing code
    * what can be open sourced?
    * which repositories can be brought back in-line with the upstream open source repo?
    * what can we move from modified open source repos to private repos?
* For current and future projects and tasks
    * ask the open source question starting in the requirements phase
    * encourage developers to interact frequently with open source communities
    * use open source project resources (mailing lists, etc) to replace internal collaboration
