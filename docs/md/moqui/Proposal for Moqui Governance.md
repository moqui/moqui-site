## Proposal for Moqui Governance

Moqui Ecosystem is a suite of community driven open source Projects including Moqui Framework, Mantle Business Artifacts (UDM and USL), the PopCommerce and HiveMind applications, various integration and tool components, and other components that may be added over time to the core Moqui source repositories.

Moqui is governed by a Board of Directors that oversees the community and legal affairs of all official Moqui Projects. The Board makes official decisions by voting on proposals from Members of the Board. A proposal is passed only with at least three positive (in favor) votes and fewer negative (opposed) votes than positive. A proposal is considered a positive vote by the Board Member who submits the proposal and requests a vote. All votes will be open for at least 5 business days unless all Board Members have voted before. Official decisions by the Board include: inviting and appointing Project Moderators, approving releases, establishing new projects, changing policies, and all other community and legal affairs that require an official decision or position.

Proposals and voting should be done on a public mailing list (generally moqui@googlegroups.com) for most matters but more sensitive matters such as inviting new Project Moderators or addressing sensitive public concerns should be handled on the Board's private mailing list (moqui-board@googlegroups.com). Anyone may vote on public proposals but only votes by Board members are binding. The official record of each proposal and vote will be the thread in the mailing list archives. Members of the Board may not act independently as a representative of Moqui without an official decision by the Board.

Each Project is managed by Moderators who are responsible for establishing scope and maintaining quality. Moderators are responsible for designs and technical decisions. Moderators operate by controlling what gets committed or merged into the official source code repository for the Project. Moderators are responsible for enforcing the Contribution Policy. Moderators are appointed by the Board and operate under the direction of the Board. An official decision by the Board supersedes a decision by a Moderator. Disputes among Moderators for a Project may be resolved by the board with an official decision.

Informal roles in Moqui include Users and Contributors. People in these roles are vital to the health and growth of Moqui but do not operate in any official position. Any person or organization may Use open source software from Moqui under the terms of the software license. Any person may Contribute to a Moqui Project under the terms of the Contribution Policy.

## Addendum 1: Contribution Policy

All contributions (source code, documentation, binaries, etc.) must be covered by a release of intellectual property (copyright and patent). Each Project source repository contains a LICENSE file detailing terms of the software license and an AUTHORS file with signatures of all contributors.

Source code for all Moqui Projects is stored and distributed on GitHub under the 'moqui' organization. Contributions from any person who is not a Moderator must be submitted by pull request on GitHub. Moderators should not accept contributions from patches or full text communicated by other means (email, issue attachment, etc).

Before a contribution can be merged into the source repository the contributor must 'sign' the Copyright Waiver and Grant of Patent License sections of the AUTHORS file with a git commit from their personal account on GitHub. The signature consists of text including the effective year(s), the contributor's GitHub username (matching the username of the commit where it is added) and full legal name. By the agreement detailed in the AUTHORS file Contributors are responsible for ensuring that contributions are their works they hold copyright for (original work or purchased) and that the work is not encumbered by an employer or any other person or organization.

Moderators should directly commit only original works and Moderators must sign the AUTHORS file just like any other Contributor.

Works (source code and other) from third parties (not original works by a Contributor or Moderator) are permitted only if covered by a permissive or 'weak copyleft' open source licenses. This includes both code (Java, Groovy, FTL, XML, JavaScript, CSS, etc) and binaries (JAR files, etc) copied in a Project repository OR referred to by code in the repository. Examples of permitted licenses include CC0, Apache (ASL), MIT, BSD, EPL, MPL, and LGPL. Examples of prohibited 'strong copyleft' open source licenses include GPL and AGPL. While users of Moqui may choose to build and use software based on Moqui along with software with a strong copyleft license it is not allowed in Moqui Projects in order to permit proprietary derivative works (whether sold or used by a single organization).

## Addendum 2: Release Process

The first step for a Project release or release series (multiple Projects) is for a Board member to send a proposal to the Board mailing list and then it is reviewed and voted on by other Board members. The Board is ultimately responsible for legal issues so part of the review done by at least one board member is to verify that the Contribution Policy has been followed. The main thing to verify is that the AUTHORS file contains an entry for each Contributor and Moderator (on GitHub click on the 'contributors' link under the 'Code' tab for each repository). At least one Board member should also review the intended version number(s) to use and the Release Notes for each Project to release.

Moqui uses semantic versioning (see semver.org), but a loose version of it. Because the current community is small we don't have the resources to maintain and support past releases using a release branch for all major and minor releases. Because of this every release tends to contain at least minor new features along with bug fixes so if semantic version was used strictly there would be no 'patch' level releases (increment 3rd number). Backward incompatible changes should always result in a major (1st number) version increment. Because Moqui projects have a large amount of functionality and there is no specification for ERP/etc systems to implement to there may be exceptions to this for backward incompatible changes to minor and generally unused features. This may change over time and become more strict as the community matures and multiple branches are maintained for bug fixes on past releases (namely we would start using the patch level version increments as intended).

Release Notes are the responsibility of Moderators for each Project. Release Notes should describe ALL non backward compatible changes along with migration notes for updating. Release Notes should also list significant new features and bug fixes.

Once a release is approved by the Board the following is needed to publish the release:

1. notify the community (with an email to moqui@googlegroups.com) that a release is a about to be done to help avoid conflicting or unintended commits during the release process
2. update the version number(s) for each Project repository included in the release in the 'addons.xml' file in the moqui-framework repository
    * commit this just before doing the release tags if moqui-framework will be released so that the addons.xml file in the release will have the correct version numbers
3. tag each GitHub repository included in the release with 'v' plus the version number (for example 'v2.1.1')
    * include the summary from Release Notes for the Project in the release description as well as a summary of the additional downloads in the release (if applicable)
    * on GitHub this automatically makes a source archive available and this is the source distribution for the release
    * for major and minor releases (first or second version number incremented) also create a release branch named 'release' plus the major and minor versions (for example 'release2.1')
4. create source, binary, and docker builds for the demo/ecosystem under the moqui-framework repository, and application builds (PopCommerce and HiveMind) under their repositories using predefined repository sets in the moqui-framework/addons.xml file
5. announce the release on the moqui@googlegroups.com mailing list, the Moqui Ecosystem group on LinkedIn, and other places for marketing decided on over time
