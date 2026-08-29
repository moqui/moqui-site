# Issue and Pull Request Guide

[TOC levels=2-3]

## Introduction

Issues and pull requests are the primary form of contribution for most users and are a vital part of making software better. The Moqui Ecosystem projects are operated using a moderator model to help maintain high quality code with consistent and reliable behavior.

Moderators have a number of concerns to consider for each issue and pull request:

### Quality

* quality is only meaningful within a context, the 'purpose' in the term 'fitness for a purpose'
* understanding the context is necessary for both writing code and for reviewing and testing code
* in an ecosystem of projects that covers a wide range of technical and business functionality context can vary a great deal and is necessary to communicate effectively and to ensure a solution is adequate for the context
* technical context must be very specific given the wide variety of deployment approaches, external systems and tools, custom code, and so on
* business context can be more difficult but describing it in terms of business activities or a series of business activities (business process) can be helpful; each activity should be described in terms of an actor and an action
* given a context a test scenario can be defined and run
* nothing should be committed or merged without a test defined and run
* automated tests are preferred but manual tests are still the practice for many things

### Backward Compatibility

* basically, don't break existing functionality
* in the Moqui Ecosystem there are various projects at the framework, business artifact, application, and integration levels and changes made need to respect other code (or artifacts) that use it
* in some cases to fix an issue or support new functionality backwards compatibility cannot be maintained
* if non-backward compatible changes are necessary they need to be mentioned in release notes and higher level code and artifacts (possibly in other repositories in the ecosystem) need to be updated for the change

### Intellectual Property

* IP clearance is required for all code and other artifacts so users can trust that their usage of the software will not be encumbered by legal issues
* Moqui Ecosystem projects use a combination of the CC0 copyright waiver and a patent waiver
* all code contributions must come from GitHub users who have signed the AUTHORS file by adding themselves to it in a git commit from their GitHub account
* if you work for an employer or client who has an IP claim on work you do it is your responsibility to get clearance from them; if you have signed an agreement assigning copyright or patent rights you should also sign an agreement that any works contributed are an exception to that
* third party libraries must use a non-encumbering open source license; requirements for open source modifications must be limited to only their own code and not any code that uses it (hence LGPL, MPL, EPL, etc. are okay when necessary, others like GPL and AGPL may not be used); preferred licenses include CC0, ASL2, MIT, and other similar liberal licenses

High quality issues contain adequate information to quickly and easily understand and reproduce. The same applies to pull requests. Issues that can't be reproduced won't be fixed. Pull requests that can't be tested won't be merged.

As with any open source project it is a volunteer (unpaid) effort to research and fix issues, and sometimes even more effort to research, test, and offer feedback on pull requests. The easier you make it to understand, reproduce, and test your issue or pull request the more likely it is to be resolved in a timely manner (or at all).

## Where to Submit

File issues and pull requests on GitHub in the repository that contains the relevant code. For the framework that is typically [github.com/moqui/moqui-framework/issues](https://github.com/moqui/moqui-framework/issues). Browse all repositories at [github.com/moqui](https://github.com/moqui). Documentation changes go to [moqui-site](https://github.com/moqui/moqui-site).

Do not file issues on moqui.org; it no longer hosts HiveMind, a wiki, or an issue tracker.

## Security Issues

To report security issues that should not be disclosed publicly before they are fixed, please use the private **[moqui-board@googlegroups.com](mailto:moqui-board@googlegroups.com)** mailing list. Anyone can send messages to it, but only members of the group can read the messages.

## Bugs and General Issues

All issues and pull requests should include this information. Please consider that collaborating remotely requires a lot more detail than in person and it is best to include detail up front rather than waiting for a clarifying question from a moderator.

Please stick to facts and avoid theories about what is happening or why. Software is generally deterministic so a given starting state and input will always result in a consistent ending state and/or output. If you are having trouble finding the cause of an issue or fixes aren't making a difference, the first step is to question theories, research code, and run tests as needed to prove or disprove theories.

### 1. Steps to Reproduce

* keep this as short as possible, and as easy to do as possible by reproducing your own issue with current code from a Moqui Ecosystem repository; even if small changes are needed to a screen, service, etc. this makes it easier to reproduce than trying to incorporate custom code with all sorts of dependencies
* the steps to reproduce that you include will often be different from how you originally found the issue because they should be written so that a moderator can easily follow them to reproduce the issue
* which Moqui components are you using and which versions (release number or date of last git pull)?
* which configuration changes are needed to reproduce the issue?
* which code (artifact) changes are needed to reproduce the issue?
* if applicable describe user interactions including:
  * specific URLs (with path and parameter, preferably from localhost as in a dev/test environment)
  * specific link, button, and other labels
  * specific data entered
* if applicable include full system interactions such as curl commands for REST requests

### 2. What Happened

* describe the current behavior you observed
* include all error message text (copy from browser or log and paste into the issue or pull request)
* attach a log file or section from the log if applicable
* use screenshots only if the text cannot be pasted into the issue, for example to show how something is displayed in a browser that cannot easily be expressed in plain text

### 3. What Should Have Happened

* describe the difference between what you observed and what should have happened
* describing the difference instead of what you expected makes it easier to understand and less likely that follow up questions will be needed
* as applicable include specific output, database values, etc.

It is okay to describe why you think this is happening and what you think could be done to fix it, but please understand that a moderator will never accept your explanation and act on it without reproducing the issue, doing whatever is needed to fix it, and testing the result.

## New Features

The information needed to implement new features varies a lot more from feature to feature than for bugs and general issues so what we need is more fluid. The key for new features is describing context. If you haven't yet read the Quality section near the top of this document please do so now.

Before suggesting a new feature please do research on existing and related functionality that already exists, and reference it in your request. This can be helpful to establish context and is an opportunity to describe what you need in terms of how it varies from what already exists. This is critical if the new feature is an enhancement to existing functionality, and is helpful even if it is entirely new.

If you want to contribute large and complex new features it is often best to first implement them in a separate component that can be deployed as an add-on, even if the intention is to add it to an existing component such as mantle-usl, SimpleScreens, MarbleERP, PopCommerce, etc. The framework picks up services in any component, and even screens can be mounted in the screen tree of existing applications using database records.
