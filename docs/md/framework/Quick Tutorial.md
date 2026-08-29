# Moqui Framework Quick Tutorial

This is a **sample page** so the static documentation viewer can be exercised (spaces in the path, fenced XML, in-app links). The full tutorial will be imported from the wiki later.

This tutorial is a step-by-step guide to creating and running your own Moqui component with a user interface, logic, and database interaction.

See the [Framework space home](/docs/framework) and [Running and Deployment](/docs/framework/Run+and+Deploy) (the latter is not imported yet — you should see the missing-page message).

## Overview

**Part 1**: Create your own component and a simple "Hello world!" screen.

**Part 2**: Define an entity and add forms to find and create records.

**Part 3**: Custom logic instead of default CrUD.

### Add a Screen

```xml
<?xml version="1.0" encoding="UTF-8"?>
<screen xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="http://moqui.org/xsd/xml-screen-2.1.xsd"
        require-authentication="anonymous-all">
    <widgets>
        <label type="h1" text="Hello world!"/>
    </widgets>
</screen>
```

Download the [latest framework release](https://github.com/moqui/moqui-framework/releases/latest) and read the [Framework overview](/framework.html) on this site.
