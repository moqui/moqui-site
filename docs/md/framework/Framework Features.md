# Moqui Framework Features

Moqui Framework gives you flexible tools to quickly create functional and secure applications.

Moqui Framework helps you build applications quickly and scale complex applications to hundreds of thousands of lines of efficient, well organized code instead of millions of lines of mess. Along the way you work on only what you care about, and let the framework take care of the rest.

[TOC]

## Big Ideas

**Comprehensive:** Moqui Framework is designed to provide comprehensive infrastructure for enterprise applications and handle common things so you can focus your efforts on the business requirements, whether it be for a multi-organizational ERP system, an interactive community web site, or even a bit of simple content with a few forms thrown into the mix.

**Automatic Functionality:** By using the tools and practices recommended for the framework you can easily build complex applications with most security and performance concerns taken care of for you.

**No Code Generation:** Moqui relies on dynamic runtime functionality to avoid the need for code generation. This keeps your development artifacts small and easy to maintain, not just easy to create.

**True 3-Tier Architecture:** Many modern frameworks have tools for database interaction and user interaction but you have to roll your own logic layer. Moqui has a strongly defined and feature rich logic layer built around service-oriented principles. This makes it easy to build a service library for internal application use, and automatically expose services externally as needed.

## Deployment and Runtime

- Java 21 on Windows, macOS, Linux, and other JVM platforms
- Executable WAR file for command-line data loading and an embedded Jetty 12 servlet container (Jakarta EE)
- The same WAR file can be dropped in a servlet container such as Tomcat or Jetty
- Runtime directory separate from the framework: your applications, add-ons, and configuration
- Runtime Moqui Conf XML is merged over `MoquiDefaultConf.xml`; sample conf for development, staging, and production
- Default webroot with login, menus, and three UI wrappers (see User Interface below)
- Embedded H2 database by default; configuration included for PostgreSQL, MySQL/MariaDB, Oracle, DB2, and SQL Server (other databases usually with configuration only)
- JTA transactions and connection pooling with the [Bitronix](https://github.com/moqui/bitronix) fork; plug in another transaction manager, or use the application server's through JNDI
- Build, test, and deploy with Gradle
- Multi-instance: one container or VM and one database per instance, with Docker automation
- Clustering through the optional `moqui-hazelcast` component: distributed entity cache invalidation, background service executor, notification topic, JCache, and servlet session replication

See [Run and Deploy](/docs/framework/Run+and+Deploy) and [Multi-instance with Docker](/docs/framework/Multi-instance+with+Docker).

## Components

A component is the unit of an application or add-on. Convention over configuration: put artifacts in the expected directories and the framework loads them.

- Directories: `entity`, `service`, `screen`, `data`, `script`, `lib`, `classes` (plus optional `screen-extend`)
- Optional `component.xml` (name, version, dependencies), `MoquiConf.xml` (merged at startup), and `build.gradle`
- Install by dropping the directory in `runtime/component`, or with `./gradlew getComponent -Pcomponent=...`
- Mount screens as subscreens of an existing screen (in the screen XML, in `MoquiConf.xml`, or with a `SubscreensItem` record)
- `extend-entity` adds fields and relationships to an entity defined in another component
- `screen-extend` adds transitions, actions, and widgets to an existing screen by matching path, without forking the original file

See [Tool and Config Overview](/docs/framework/Tool+and+Config+Overview#extensions-and-add-ons) and [XML Screen](/docs/framework/User+Interface/XML+Screen#screen-extend).

## API

The **ExecutionContext** (`ec`) is created for each web request, service call, or other execution. It holds the context (variable space) as a stack of maps, and is the handle to every framework facade:

- WebFacade — servlet objects, parameters, JSON request/response helpers (null when not in a web request)
- UserFacade — current user, login/logout, preferences, locale/time zone/currency
- MessageFacade — general and error messages, validation errors
- ArtifactExecutionFacade — artifact stack and history; authorization and hit tracking
- L10nFacade — localize text; parse and format numbers and dates
- ResourceFacade — resources by location (`classpath://`, `component://`, `http(s)`, `file`, `content://`, and others); run scripts and render templates
- LoggerFacade — logging for non-class code
- CacheFacade — `javax.cache` (JSR-107); default implementation is MCache
- TransactionFacade — JTA-style begin/commit/rollback and transaction tracking
- EntityFacade — relational (and pluggable) data access
- ElasticFacade (`ec.elastic`) — OpenSearch / ElasticSearch 7.x HTTP client
- ServiceFacade — local and remote services
- ScreenFacade — render screens through ScreenRender

Also: `ec.getTool()` for configured ToolFactory instances, `ec.makeNotificationMessage()` for notifications, and `ec.runAsync()` for a lightweight ExecutionContext-aware executor.

See [Tool and Config Overview](/docs/framework/Tool+and+Config+Overview) and the [API Javadoc](/javadoc/).

## Data

- Define entities in XML and use them; no generated persistence code
- Java API (`EntityValue`, `EntityFind`) and XML Actions for create, update, delete, find, count, and related operations
- Entity cache with automatic clearing; optional write-through per-transaction cache to cut database round-trips
- Automatic schema work at runtime: create missing tables, columns, indexes, and foreign keys
- Import and export XML, CSV, and JSON (API, Tools screens, and `java -jar moqui.war load`); data snapshots for full-database move
- Entity ECA rules on data changes
- View entities (including database-driven views); `extend-entity` from other components
- Field audit logging and field encryption
- Primary and secondary sequenced IDs
- Data Documents: nested Map/JSON documents from database data, configured in records
- Data Feed: generate documents on change and send them to services (search indexing, notifications, and so on)
- Data Search through ElasticFacade and OpenSearch (ElasticSearch 7.x compatible)
- Time-based Entity Sync between Moqui systems
- Framework seed structures (not Mantle): enumerations and statuses with transitions, units of measure with conversion (including currency), geographic boundaries and points, time periods
- Plug in other datasources; OrientDB is the optional `moqui-orientdb` component

See [Data and Resources](/docs/framework/Data+and+Resources).

## Logic

- XML service definitions: typed parameters, conversion, validation; HTML allow-list per parameter (`none` / `safe` / `any`)
- Call services synchronously, asynchronously, scheduled (`ServiceJob` with cron), or on transaction commit/rollback
- Implicit entity-auto services for create, update, delete, and store (create or update)
- Service ECA rules before/after validation, auth, run, commit, or rollback
- Implementations in XML Actions, Groovy, Java methods, or a runner you plug in
- XML Actions compile to Groovy for runtime performance; embeddable in service and screen definitions
- Email: send from an EmailTemplate; receive with Email ECA rules against an EmailServer

See [Logic and Services](/docs/framework/Logic+and+Services).

## User Interface

- XML Screens: hierarchical subscreens (directory, XML, conf, or database), automatic menus, virtual hosts by hostname
- Transitions for input processing and conditional response (another screen, URL, or none); restriction by HTTP method
- Standalone screens (no parent decoration) for dialogs, CSV/PDF, and similar
- form-single and form-list; automatic fields from entity and service definitions, with client and server validation from the service
- Database form extensions (DbForm) for all users or a user group
- Three web wrappers over the same application screen tree:
  - `/qapps` — default; Quasar + Vue (`qvt` / `qjs` / `qvue`)
  - `/vapps` — Vue + Bootstrap (`vuet` / `js` / `vue`)
  - `/apps` — server-rendered HTML
- Hybrid XML widgets rendered as Vue templates; optional 100% client-rendered `.qvue` / `.vue` screens
- Other render modes: CSV, XML, plain text, XSL-FO (PDF and related through the optional `moqui-fop` component)
- Notifications: user- and topic-based publish/subscribe, optional persist and email, WebSocket at `/notws`
- Localization of labels, titles, messages, and entity fields (base-language text is the lookup key)
- WebFacade for parameters and JSON; webapp events (first-hit-in-visit, before/after request, login/logout, startup/shutdown)

See [User Interface](/docs/framework/User+Interface).

## Security

Moqui handles **application** security. It is designed to run **behind** a WAF and reverse proxy; it is not a WAF.

- Apache Shiro 2 with MoquiShiroRealm (UserAccount); other realms such as LDAP or Active Directory in `shiro.ini`
- Password constraints and hashing, login failure lockout, password-reset email
- Built-in second-factor authentication (TOTP, email, SMS, backup codes)
- Optional SSO through the `moqui-sso` component (OIDC, OAuth, SAML)
- Login/API keys (`api_key` / `login_key` header or body) for API clients
- CSRF: `moquiSessionToken` form field or `X-CSRF-Token` header (XML Forms and the SPA shells send this automatically)
- Default response headers (CSP `frame-ancestors`, X-Frame-Options, HSTS on secure screens, and others)
- XSS protection: input canonicalization, JSoup cleaning, `allow-html` on service parameters
- Simple permissions (`ec.user.hasPermission`) and UserGroup (including automatic ALL_USERS)
- Artifact-aware authorization in the database: inheritable allow/deny on screens, transitions, services, and entities
- Record-level authorization and entity filter sets (automatic query conditions)
- Artifact tarpit: per-user, per-artifact velocity limits (business-risk mitigation, not a WAF)
- Screens can require authentication and/or HTTPS

See [Security](/docs/framework/Security), [Single Sign-On](/docs/framework/Single+Sign-On), and [Run and Deploy](/docs/framework/Run+and+Deploy) (Production security).

## Integration

- Service REST API: `*.rest.xml` resource trees at `/rest/s1/...`; generated Swagger
- Entity REST API at `/rest/e1/...` and master-definition REST at `/rest/m1/...` (authc and authz still apply)
- JSON-RPC 2.0 at `/rpc/json` for services with `allow-remote=true`; remote-json-rpc and remote-rest service runners for outgoing calls
- HTTP-method-sensitive screen transitions as REST wrappers around internal services
- System Messages: incoming and outgoing message queue with retry, history, HTTP receive, and configurable produce/send/process services
- Optional transport and integration components: Camel, SFTP, AWS (see below)

See [System Interfaces](/docs/framework/System+Interfaces) and [Web Service](/docs/framework/System+Interfaces/Web+Service).

## Operations

- ArtifactHit and ArtifactHitBin for screens, transitions, services, and entities
- Built-in profiler: call tree for an ExecutionContext, consolidated counts, hot spots
- Lightweight `/status` to see if the server is running
- **Tools** (`/qapps/tools`): developer and data tools — entity data, import/export/snapshots, SQL runner, auto screens, service runner, Groovy shell, in-memory artifact stats
- **System** (`/qapps/system`): administration — users and groups, artifact authz, jobs, cache, localization, data documents, visits, instance management, system messages, entity sync
- Spock and JUnit for unit and integration tests (service call and screen render)

See [Performance](/docs/framework/Performance) and [The Tools Application](/docs/framework/The+Tools+Application).

## Optional Tool Components

These are not in the framework JAR. Install with `./gradlew getComponent -Pcomponent=...` (see `addons.xml`).

- **moqui-hazelcast** — clustering and distributed cache, executor, notifications, sessions
- **moqui-fop** — PDF, PS, SVG, and related output from XSL-FO and HTML
- **moqui-poi** — spreadsheet and document files
- **moqui-sftp** — SFTP client and server
- **moqui-aws** — Amazon Web Services integrations (S3, SNS, SMS)
- **moqui-image** — image format conversion and processing
- **moqui-camel** — Apache Camel endpoint to and from Moqui services
- **moqui-sso** — OpenID Connect, OAuth, and SAML
- **moqui-orientdb** — OrientDB through the Entity Facade
- **moqui-kie** — Drools rules and jBPM workflows
- **moqui-cups** — printing through CUPS
- **moqui-wikitext** — wiki markup rendering (Confluence, MediaWiki, and others)

The [example](https://github.com/moqui/example) component is a small application (entities, services, screens, security, localization) used by the [Quick Tutorial](/docs/framework/Quick+Tutorial).
