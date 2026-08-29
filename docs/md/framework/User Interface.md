# User Interface

The main artifact for building user interfaces in Moqui Framework is the XML Screen.

XML Screens are designed to be used with multiple render modes using the same screen definition. This includes various types of text output for user and system interfaces, and code-driven user interfaces in client applications.

To accommodate this design goal most screen elements are render-mode agnostic. For elements that are specific to a particular render mode there is a `render-mode` element with subelements designed for specific render modes. To support multiple render-mode specific elements in the same screen, put a subelement under the `render-mode` element for each desired type.

In a web-based application an XML Screen is the main way to produce output for incoming requests. The structure of screens makes it easy to support any sort of URL to a screen.

The default webroot subscreen is **qapps** (Quasar + Vue). The same application screen tree under `apps.xml` is also available through two other wrappers:

- `/qapps` — default UI; client-rendered Quasar + Vue (`qvt` / `qjs` / `qvue`)
- `/vapps` — Vue + Bootstrap SPA (`vuet` / `js` / `vue`)
- `/apps` — server-rendered HTML

Local URLs in this section use `http://localhost:8080/qapps/...` unless the page is specifically about another render mode.

This section covers:

- [XML Screen](/docs/framework/User+Interface/XML+Screen)
- [XML Form](/docs/framework/User+Interface/XML+Form)
- [Client Rendered Vue Screen](/docs/framework/User+Interface/Client+Rendered+Vue+Screen)
- [Templates](/docs/framework/User+Interface/Templates)
- [Sending and Receiving Email](/docs/framework/User+Interface/Sending+and+Receiving+Email)
- [Notification and WebSocket](/docs/framework/User+Interface/Notification+and+WebSocket)
