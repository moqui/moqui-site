# Security

[TOC levels=2-3]

Moqui Framework handles **application** security: authentication, optional MFA, optional SSO, artifact-aware authorization, CSRF tokens, input allow-lists, and per-artifact velocity limits. It is designed to run **behind** a web application firewall and reverse proxy. It is not a WAF and is not the right place in the stack for WAF functionality.

See also [Single Sign-On](/docs/framework/Single+Sign-On) for the optional `moqui-sso` component, [Run and Deploy](/docs/framework/Run+and+Deploy) for production deployment practice, and [Web Service](/docs/framework/System+Interfaces/Web+Service) for REST authentication.

## Layers

A typical production request path is:

**Browser or API client → WAF / reverse proxy / TLS → Moqui (authn, MFA, SSO, artifact authz, tarpit, CSRF, headers, HTML allow-lists) → database and OpenSearch**

The edge (WAF, load balancer, reverse proxy) is where TLS termination, volumetric and protocol attacks, bot scoring, geo/IP reputation, HTTP normalization, and similar concerns belong. Moqui's overlapping knobs (tarpit, login lockout, CSRF tokens, default response headers, `allow-html`) are for **application and business-risk mitigation** inside the app. They are not a substitute for a WAF.

The `webapp_https_enabled`, `webapp_https_port`, and `webapp_http_host` settings are for **URL generation** when Moqui sits behind that edge. They do not make Moqui a TLS terminator or a WAF. Docker compose files under `moqui/docker/` (nginx-proxy, ACME/Let's Encrypt) are examples of TLS at the proxy.

## Authentication

The main code path for user authentication starts with a call to the UserFacade.**loginUser**() method. This calls into Apache Shiro 2 for the actual authentication. ExecutionContextFactoryImpl loads Shiro from the classpath `shiro.ini` file using `org.apache.shiro.env.BasicIniEnvironment` (not the Shiro 1 INI factory):

```
BasicIniEnvironment env = new BasicIniEnvironment("classpath:shiro.ini");
internalSecurityManager = env.getSecurityManager()
```

UserFacade.**loginUser**() then builds a `UsernamePasswordToken` and logs in a Shiro `Subject`. This is basically what the code looks like:

```
UsernamePasswordToken token = new UsernamePasswordToken(username, password, true)
Subject loginSubject = eci.getEcfi().getSecurityManager().createSubject(new DefaultSubjectContext())
loginSubject.login(token)
```

Shiro is configured by default to use the MoquiShiroRealm so this ends up in a call to the MoquiShiroRealm.**getAuthenticationInfo**() method, which authenticates using the moqui.security.UserAccount entity and handles things like disabled accounts, keeping track of failed login attempts, etc. Here are the lines from the shiro.ini file where this is configured:

```
moquiRealm = org.moqui.impl.util.MoquiShiroRealm
securityManager.realms = $moquiRealm
```

Shiro can be configured to use other authentication realms that still ship in Shiro 2, such as `JdbcRealm`, `DefaultLdapRealm` (LDAP; `JndiLdapRealm` remains as a deprecated subclass), or `ActiveDirectoryRealm`. You can also implement your own, or even modify the MoquiShiroRealm class to better suit your needs. See the Shiro [Realms](https://shiro.apache.org/realm.html) documentation for writing your own realm and for configuration of these classes.

The older Shiro 1 *CasRealm* is not part of Shiro 2. For CAS, SAML, or OpenID Connect, use the optional **moqui-sso** component (pac4j) rather than a Shiro CAS realm. See [Single Sign-On](/docs/framework/Single+Sign-On).

Back to the MoquiShiroRealm that is used by default, here is its default configuration from the MoquiDefaultConf.xml file that can be overridden in your runtime Moqui Conf XML file:

```
 <user-facade>
        <password encrypt-hash-type="SHA-256" min-length="8" min-digits="1" min-others="1"  history-limit="5" change-weeks="104" email-require-change="false" email-expire-hours="48"/>
        <login-key encrypt-hash-type="SHA-256" expire-hours="144"/><!-- default expire 6 days, 144 hours -->
        <login max-failures="3" disable-minutes="5" history-store="true" history-incorrect-password="false"/>
 </user-facade>
```

The **login** element configures the max number of login failures to allow before disabling a UserAccount (**max-failures**), how long to disable the account when the max failures is reached (**disable-minutes**), whether to store a history of login attempts in the UserLoginHistory entity (**history-store**) and whether to persist incorrect passwords in the history (**history-incorrect-password**). This lockout is an application control on a user account. It is not a WAF.

The **login-key** element is used to configure login/API keys. **encrypt-hash-type** tells which hash algorithm to use and **expire-hours** tells how long it takes to expire. A key for the current user is created with *ec.user*.**getLoginKey**() and presented as the `api_key` or `login_key` HTTP header (or request-body parameter). See [Web Service](/docs/framework/System+Interfaces/Web+Service) for REST authentication.

The **password** element is used to configure the password constraints that are checked when creating an account (org.moqui.impl.UserServices.**create#UserAccount**) or updating a password (org.moqui.impl.UserServices.**update#Password**).

Settings include the hash algorithm to use for passwords before persisting them and before comparing an entered password (**encrypt-hash-type**; MD5, SHA, SHA-256, SHA-384, SHA-512), the minimum password length (**min-length**), the minimum number of digit characters in the password (**min-digits**), the minimum number of characters other than digits or letters (**min-others**), how many old passwords to remember on password change to avoid use of the same password (**history-limit**), and how many weeks before forcing a password change (**change-weeks**).

The main way to reset a forgotten password is by an email that includes a randomly generated password. The **email-require-change** attribute specifies whether to require a change on the first login with the password from the email, making it a temporary password. The **email-expire-hours** attribute specifies how many hours before the password in the email expires.

## Second Factor (MFA)

After a correct password, a second authentication factor may be required. MFA is built into the framework. It is not SSO, not a WAF, and not a substitute for TLS at the edge.

### When a second factor is required

The service `org.moqui.impl.UserServices.get#UserAuthcFactorRequired` (used from MoquiShiroRealm during login) decides as follows:

1. If the user has **any** active `UserAuthcFactor` records (date-filtered), a second factor is required.
2. Otherwise, a second factor is required if the user is a member of any `UserGroup` with **requireAuthcFactor**=Y.

So: enabling a factor on a user turns MFA on for that user. Requiring MFA for a group of users is a group flag, and those users must have at least one factor set up or they cannot complete login.

### Factor types

Factors are `moqui.security.UserAuthcFactor` records. **factorOption** is encrypted and its meaning depends on type:

| Type enum | Description | factorOption | How the user proves it |
|---|---|---|---|
| **UafTotp** | Authenticator app (TOTP) | Shared secret | Six-digit code from the app |
| **UafEmail** | Email code | Email address | One-time code sent to that address |
| **UafSms** | SMS code | Phone number | One-time code sent by SMS |
| **UafSingleUse** | Backup / single-use code | Hashed code | One of the printed backup codes; the factor is thru-dated after use |

There is a special seed factor `factorId=UserAccountEmail` (`userId=_NA_`) so a user with **no** other factors can receive an email code at `UserAccount.emailAddress`. If the user already has any active factors, that fallback is not used.

TOTP verification uses the `dev.samstevens.totp` library. Email and SMS send a single-use code (see `send#AuthcCodeEmail` and `send#AuthcCodeSms`) and need working email / SMS configuration. TOTP does not.

### Admin setup

Configure users, groups, and factors in the System app: `http://localhost:8080/qapps/system/Security`.

- **User Group**: set **requireAuthcFactor** so every member must use a second factor.
- **User Account** detail: add factors. TOTP, email, and SMS factors start with **needsValidation**=Y until the user completes the matching verify screen (`VerifyTotp`, `VerifyEmail`, `VerifySms` under the account).
- Backup codes: `create#SingleUseAuthcCodes` (default 6 codes, max 21; 8-digit codes, hashed at rest). Show the plaintext codes once, then store them offline.

### Interactive login

1. User submits username and password on the Login screen (`/Login`).
2. If a second factor is required, Shiro pre-authenticates (password is correct) and the session keeps `moquiPreAuthcUsername` / `moquiAuthcFactorRequired`. The user is **not** fully logged in yet.
3. The `SecondFactor` screen (`/SecondFactor`) lists the user's factor types. For email/SMS the user picks a factor and **sendOtp** (`send#ExternalAuthcCode`). For TOTP they enter the app code. Backup codes are entered the same way as TOTP (no send).
4. **verifyUserAuthcFactor** calls `validate#ExternalUserAuthcCode` and, if valid, `ec.user.internalLoginUser(username)`.

The default Quasar UI (`/qapps`) also has a re-login MFA prompt on the Vue root when a session needs a code.

If a group requires MFA but the user has no factors, SecondFactor tells them to contact an administrator.

### REST

POST `/rest/login` with `username` and `password` (and `code` if you already have one). If a second factor is required and no valid code is sent, the JSON response is the user's factor info (`get#ExternalUserAuthcFactorInfo`) and the session remembers the pre-authenticated user. Then:

- POST `/rest/sendOtp` with `factorId` to send an email/SMS code
- POST `/rest/verifyOtp` with `code` to complete login

`factorId` may be `UserAccountEmail` only if the user has no other active factors. Details and the other REST auth methods (`api_key`, Basic, body credentials) are on [Web Service](/docs/framework/System+Interfaces/Web+Service).

## CSRF (session token)

State-changing screen transitions (anything other than GET, unless the transition sets `require-session-token="false"`) must present the session CSRF token. Get it from *ec.web*.**getSessionToken**() / the session attribute `moqui.session.token`. Send it as:

- form field **moquiSessionToken**, or
- request header **moquiSessionToken** or **X-CSRF-Token**

XML Forms and the `/qapps` / `/vapps` shells include this automatically. Custom JavaScript POSTs must send the header.

There is no `/rest/moquiSessionToken` transition. It was removed because it was a CSRF vector (anyone could fetch a token). REST login uses `require-session-token="false"` on `/rest/login` specifically; other `/rest` transitions follow the same token rules as screens unless marked otherwise.

This is application CSRF protection for Moqui forms and the SPA. It is not a WAF.

## Default response headers

`MoquiDefaultConf.xml` sets default `webapp.response-header` values. Override them in a runtime or component conf file. Defaults include:

- **Content-Security-Policy** on screen-render: `frame-ancestors 'none'; form-action 'self';` (a stricter `default-src` example is commented in that file for internal apps)
- **X-Frame-Options**: `sameorigin`
- **X-Content-Type-Options**: `nosniff`
- **X-XSS-Protection**: `1; mode=block` (kept because some scanners look for it)
- **Strict-Transport-Security** on `screen-secure` (when the request is treated as HTTPS)
- CORS headers when `webapp.@handle-cors` is on; **Access-Control-Allow-Origin** is set only if the request `Origin` is in `webapp.@allow-origins` (`webapp_allow_origins`)

Session cookies are `http-only` with SameSite Lax (`web.xml` `cookie-config`).

These headers are browser/app hardening. They are not a WAF.

HTML submitted to services is constrained by `parameter.@allow-html` (`none` by default, or `safe` / `any`). Safe HTML uses the OWASP AntiSamy / ESAPI configuration. See [Tool and Config Overview](/docs/framework/Tool+and+Config+Overview).

## Simple Permissions

The most basic form of authorization (authz) is a permission explicitly checked by code. Artifact-aware authz (covered in the next section) is generally more flexible as it is configured external to the artifact (screen, service, etc) and is inheritable to avoid issues when artifacts (especially services) are reused.

The API method to check permissions is the ec.user.**hasPermission**(String userPermissionId) method. A user has a permission if the user is a member (UserGroupMember) of a group (UserGroup) that has the permission (UserGroupPermission). The **userPermissionId** may point to a UserPermission record, but it may also be any arbitrary text value as the UserGroupPermission has no foreign key to UserPermission.

## Artifact-Aware Authorization

The artifact-aware authorization in Moqui enables external configuration of access to artifacts such as screens, screen transitions, services, and even entities. With this approach there is no need to add code or configuration to each artifact to check permissions or otherwise see if the current user has access to the artifact.

### Artifact Execution Stack and History

The ArtifactExecutionFacade is used by all parts of the framework to keep track of each artifact as it executes. It keeps a stack of the currently executing artifacts, each one pushed on the stack as it begins (with one of the **push**() methods) and popped from the stack as it ends (with the **pop**() method). As each artifact is pushed onto the stack it is also added to a history of all artifacts used in the current ExecutionContext (i.e., for a single web request, remote service call, etc).

Use the ArtifactExecutionInfo **peek**() method to get info about the artifact at the top of the stack, Deque&lt;ArtifactExecutionInfo&gt; **getStack**() to get the entire current stack, and List&lt;ArtifactExecutionInfo&gt; **getHistory**() to get a history of all artifacts executed.

This is important for artifact-aware authorization because authz records are inheritable. If an artifact authz is configured inheritable then not only is that artifact authorized but any artifact it uses is also authorized.

Imagine a system with hundreds of screens and transitions, thousands of services, and hundreds of entities. Configuring authorization for every one of them would require a massive effort to both set up initially and to maintain over time. It would also be very prone to error, both incorrectly allowing and denying access to artifacts and resulting in exposure of sensitive data or functionality, or runtime errors for users trying to perform critical operations that are a valid part of their job.

The solution is inheritable authorization. With this you can set up access to an entire application or part of an application with authz configuration for a single screen that all sub-screens, transitions, services, and entities will inherit. To limit the scope, sensitive services and entities can have a deny authz that overrides the inheritable authz, requiring special authorization to those artifacts. With this approach you have a combination of flexibility, simplicity, and granular control of sensitive resources.

This is also used to track performance metrics for each artifact. See [Performance](/docs/framework/Performance) for artifact execution runtime profiling.

### Artifact Authz

The first step to configure artifact authorization is to create a group of artifacts. This involves an ArtifactGroup record and an ArtifactGroupMember record for each artifact, or artifact name pattern, in the group.

For example here is the artifact group for the Example app with the root screen (ExampleApp.xml) as a member of the group:

```
   <moqui.security.ArtifactGroup artifactGroupId="EXAMPLE_APP" description="Example App (via root screen)"/>
   <moqui.security.ArtifactGroupMember artifactGroupId="EXAMPLE_APP" artifactTypeEnumId="AT_XML_SCREEN" inheritAuthz="Y" artifactName="component://example/screen/ExampleApp.xml"/>
```

In this case the **artifactName** attribute has the literal value for the location of the screen. It can also be a pattern for the artifact name (with **nameIsPattern**="Y"), which is especially useful for authz for all services or entities in a package. Here is an example of that for all services in the moqui.example package, or more specifically all services whose full name matches the regular expression "moqui\.example\..*":

```
<moqui.security.ArtifactGroupMember artifactGroupId="EXAMPLE_APP" artifactName="moqui.example..*" nameIsPattern="Y" artifactTypeEnumId="AT_SERVICE" inheritAuthz="Y"/>
```

The next step is to configure authorization for the artifact group with an ArtifactAuthz record. Below is an example of a record that gives the ADMIN group always (AUTHZT_ALWAYS) access for all actions (AUTHZA_ALL) to the artifacts in the EXAMPLE\_APP artifact group set up above.

```
<moqui.security.ArtifactAuthz artifactAuthzId="EXAMPLE_AUTHZ_ALL" userGroupId="ADMIN" artifactGroupId="EXAMPLE_APP" authzTypeEnumId="AUTHZT_ALWAYS" authzActionEnumId="AUTHZA_ALL"/>
```

The always type (**authzTypeEnumId**) of authorization overrides deny (AUTHZT_DENY) authorizations, unlike the allow authz (AUTHZT_ALLOW) which is overridden by deny. The other options for the authz action (**authzActionEnumId**) include view (AUTHZA_VIEW), create (AUTHZA_CREATE), update (AUTHZA_UPDATE), and delete (AUTHZA_DELETE) in addition to all (AUTHZA_ALL).

For example here is a record that grants only view authz with the type allow (so can be denied) of the same artifact group to the EXAMPLE_VIEWER group:

```
<moqui.security.ArtifactAuthz artifactAuthzId="EXAMPLE_AUTHZ_VW" userGroupId="EXAMPLE_VIEWER" artifactGroupId="EXAMPLE_APP" authzTypeEnumId="AUTHZT_ALLOW" authzActionEnumId="AUTHZA_VIEW"/>
```

Entity artifact authorization can also be restricted to particular records using the *ArtifactAuthzRecord* entity. This is used with a view entity (**viewEntityName**) that joins between the **userId** of the currently logged in user and the desired record. If the name of the field with the **userId** is anything other than **userId** specify its name with the **userIdField** field. The record level authz is checked by doing a query on the view entity with the current **userId** and the PK fields of the entity the operation is being done on. To add constraints to this query you can add them to the view-entity definition, use the **filterByDate** attribute, or use ArtifactAuthzRecordCond records to specify conditions.

If authorization fails when an artifact is used the framework creates an ArtifactAuthzFailure record with relevant details.

### Entity Filter Sets and Authorization

Automatic query augmentation (adding conditions to find/select queries) can be used to filter records by configuration using the *ArtifactAuthzFilter* entity. This ties record-level authorization to application (screen/etc) authorization. Each filter set associated with an ArtifactAuthz has various condition expressions stored using the *EntityFilterSet* entity.

Each record has an Entity Name for the entity that should be filtered when queried on (either directly or through a view-entity, i.e. joined into a query). Each record also has a Filter Map which is a Groovy expression that should evaluate to a Map. While filtering can be done on view entities it is not a good practice as data leakage is easy through direct entity finds or other view entities so filters are generally defined only on plain entities and not view entities.

For view entities and dynamic view entities, which includes DataDocument based dynamic view entities, in order for a filter to apply to a query the fields used in each filter must be included in the definition. This means that entities with a filter must also be included in the view. For example any view entity or report on OrderItem should also include the customerPartyId and vendorPartyId fields on the OrderPart entity for active or user organization based filtering.

The Groovy expressions can be somewhat complex. The main OOTB example in Moqui is in the Mantle USL component for organization based record filtering. The expressions use two variables that are always available (populated in always-actions in the root screen of any application that should support organization based filters): ‘activeOrgId’ for the ID of the user selected active organization and ‘filterOrgIds’ which is a set of IDs that should be used to filter the results, either just the activeOrgId or if no active org then all partyIds of organizations the current user is a member of.

## Artifact Tarpit

An artifact tarpit limits the **velocity of access to artifacts** for a user. It is per-user and per-artifact (or artifact type). That is **business-risk mitigation** inside the application (slowing a scripted or confused client that is hammering a screen or service). It is **not** a WAF: it does not see unauthenticated floods, protocol abuse, or traffic that never reaches Moqui.

Here is an example of an artifact group for all screens and an ArtifactTarpit to restrict access for all users to each screen for 60 seconds (**tarpitDuration**) if there are more than 120 hits (**maxHitsCount**) within 60 seconds (**maxHitsDuration**).

```
<moqui.security.ArtifactGroup artifactGroupId="ALL_SCREENS" description="All Screens"/>
<moqui.security.ArtifactGroupMember artifactGroupId="ALL_SCREENS" artifactName=".*" nameIsPattern="Y" artifactTypeEnumId="AT_XML_SCREEN"/>
<moqui.security.ArtifactTarpit userGroupId="ALL_USERS" artifactGroupId="ALL_SCREENS" maxHitsCount="120" maxHitsDuration="60" tarpitDuration="60"/>
```

When a particular user (**userId**) exceeds the configured velocity limit for a particular artifact (**artifactName**) or a particular type (**artifactTypeEnumId**) the framework creates an ArtifactTarpitLock record to restrict access to that artifact by the user until a certain date/time (**releaseDateTime**).

Tarpit can be enabled or disabled per artifact type on `artifact-execution-facade.artifact-execution.@tarpit-enabled` in the Moqui Conf XML file (screens, transitions, and services are enabled by default).

## Reporting vulnerabilities

To report security issues that should not be disclosed publicly before they are fixed, use the private **[moqui-board@googlegroups.com](mailto:moqui-board@googlegroups.com)** mailing list. Anyone can send messages to it; only Board members can read them. See the [Community Guide](/docs/moqui/Community+Guide).
