# UBPL Introduction

## Why a Universal Business Process Library?

UBPL documents business processes that are commonly used. It is to business processes what the Universal Data Model is to data structures.

There are very few standards or projects for business processes. Some of the closest are some semi-helpful books about business best practices and documents created as a part of a number of business related specifications. Here is a page with some references:

[Resources with Information about General Business Processes](Business Process Library/Resources with Information about General Business Processes)

These are not adequate for designing and building ERP systems, and even if they were we want something that the community can participate in to maintain and expand, and also to tie these artifacts to actual things that exist in the Moqui Ecosystem.

This isn't meant to include everything that every business might do, but to be a library of general business activities that make up common processes that are shared by a wide variety of businesses. Some may be less commonly used, but the general intent will be similar to that of the rest of Mantle: things that can be customized and reused or used as-is for a wide variety of businesses to help with business process automation efforts.

Here is the index for the Universal Business Process Library:

[UBPL Index](Business Process Library/UBPL Index)

## What is in this Library?

This library will consist of Business Process Stories. These stories are basically a series of sentences, each one consisting of an actor and an action. Just keep that in mind, it's _always_ actor and action, actor and action, actor and action. Hopefully that's clear! All sentences need both, and may have conditions on them and other things as well, but always need an actor and an action. One basic rule based on that is no actions without actors.

The top level document has 3 main parts:

1. Actor Definitions
2. General Business Process Stories
3. Stories for Specific Types of Organizations

In part #2 we'll create the library of smaller stories that make up parts of the higher level stories that are in #3. For example, look at the [Story of Online Retail Company](Business Process Library/Story of Online Retail Company).

There are a lot of high level steps in that story that describe general business activities. These are assembled in a way that makes sense for a retail company, but many of the individual activities are just as applicable in different parts of the high level stories for other types of organizations.

Part #2 has smaller scoped processes that can be reused in many different types of companies, and based on writing stories for specific types of organizations we'll flesh that out to include a wide variety of business activities organized according to yet higher level business concepts, like the Marketing, Sales, Warehouse Management, etc. that are currently in there.

In part #2 each of these process names should also include both actor and action, and for higher level things like this the actor should be the "primary" actor for the story; there will certainly be other actors involved in most of them.

## Concepts Behind This, and "HEMP"

The idea of using stories (aka "narratives") like this is a common one. Part of the reason for writing them specifically in the way described here is to make them a good starting point for further UI and system design efforts. These stories are based on the concepts and story structure details in "HEMP: An agile approach to analysis and design". HEMP stands for "Holistic Enterprise Mechanization Process". The author notes that a better word for "mechanization" is "automation", but thought HEMP would make a more colorful and interesting title than HEAP.

The book and other details are available at: [https://coarchy.com/HempExcerpts](https://coarchy.com/HempExcerpts?utm_source=moqui&utm_medium=business_process_library&utm_campaign=moqui_community)

## A Special Note on Testing

The requirements and designs that come out of this effort will also help drive automated and manual testing efforts. Sometimes a problem with testing is we don't know what to test, or what the business activities the software is trying to support. This will help with the problem. Along with these business process stories we may want test scenarios based on them, that are linked to from the stories.
