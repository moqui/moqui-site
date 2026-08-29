# Moqui Framework

This space contains documentation about Moqui Framework. It is more technical in nature, meant for developers and IT staff.

The full wiki corpus has not been imported yet. This page is a stub so the documentation viewer can be used and tested. When the wiki is migrated, files such as `Quick Tutorial.md` will be listed in `docs/manifest.json` and rendered here.

If you're just getting started with Moqui the recommended reading order (after import) is:

1. Introduction to Moqui Framework
2. Moqui Framework Features
3. Running and Deployment Instructions
4. Moqui Framework Quick Tutorial
5. Framework Tool and Configuration Overview

Useful links that already work on this static site:

- [Framework overview](/framework.html)
- [API Javadoc](/javadoc/)
- [Download](https://github.com/moqui/moqui-framework/releases/latest)

```groovy
def tutorial = ec.entity.makeValue("tutorial.Tutorial")
tutorial.setFields(context, true, null, null)
if (!tutorial.tutorialId) tutorial.setSequencedIdPrimary()
tutorial.create()
```
