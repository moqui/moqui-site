# Single Sign-On

[TOC levels=2-3]

SSO in Moqui is the optional **moqui-sso** component. It uses [pac4j](https://www.pac4j.org/) 6 (Jakarta) to talk to an identity provider, then creates or updates a local `UserAccount` and calls `internalLoginUser`. Local username/password authentication stays on Apache Shiro 2; see [Security](/docs/framework/Security).

SSO is not MFA (they can be used together), not a WAF, and not a replacement for TLS at the reverse proxy. Shiro 2 has no CasRealm; this component is the path for SAML, OpenID Connect, and OAuth.

## Install

`moqui-sso` is listed in `addons.xml`. From the moqui-framework root:

```
$ ./gradlew getComponent -Pcomponent=moqui-sso
```

The component's `MoquiConf.xml` mounts `sso.xml` as a webroot subscreen named **sso**, so the URLs below are at the host root (same place as `/Login`).

## Protocols and client types

Each configured IdP is an **AuthFlow** (`moqui.security.sso.AuthFlow`) plus a type-specific record. `authFlowTypeEnumId`:

| Type | Enum | Detail entity | Typical use |
|---|---|---|---|
| OpenID Connect | **AftOidc** | `OidcFlow` | Keycloak, Azure AD, Google, Apple, generic OIDC |
| OAuth | **AftOauth** | `OauthFlow` | GitHub, Google (OAuth 2), Twitter, generic OAuth 1.0/2.0, others in seed data |
| SAML 2 | **AftSaml** | `SamlFlow` | Enterprise IdP metadata + SP keystore |

OIDC `OidcFlow.clientTypeEnumId` values built in `AuthenticationClientFactory`: **OctKeycloak** (needs `realm` and `baseUri`), **OctAzureAd**, **OctGoogle**, **OctApple**, **OctOther** (generic `OidcClient`). Common OIDC fields: `clientId`, `secret`, `discoveryUri`, `preferredJwsAlgorithmEnumId`, `useNonce`.

OAuth `OauthFlow.clientTypeEnumId` seed values include GitHub, Google, Facebook, LinkedIn, Twitter, Bitbucket, Dropbox, PayPal, WordPress, Yahoo, Foursquare, plus **OctOauth10** and **OctOauth20**.

SAML `SamlFlow` needs a keystore location (Resource Facade location), keystore and private-key passwords, `serviceProviderEntityId`, and `identityProviderMetadataLocation`. The factory copies keystore and metadata into `runtime/tmp` for pac4j.

Only flows with **disabled** not Y and **inbound** not Y appear on the Login screen and in `buildAll()` (the callback uses `buildAll()` so it can match whichever client returns).

## URLs

Callback URL the IdP must allow, built from the current webapp HTTPS root:

`{webappRootUrl}/sso/callback`

| Path | Role |
|---|---|
| **POST or GET `/sso/login`** | Start login. Parameters: `authFlowId` (required), `returnTo` (optional). |
| **`/sso/callback`** | pac4j callback; creates/updates the user, then `internalLoginUser`. |
| **`/sso/logout`** | Local logout, and IdP logout when the session has `moquiAuthFlowExternalLogout` (set after an SSO login). Optional `returnTo`. |

These transitions set `require-session-token="false"` because the browser is coming from the IdP.

The Login screen (`Login.ftl`, extended by moqui-sso) adds an **SSO** tab when any eligible AuthFlow exists. Each flow is a POST to `/sso/login` with that `authFlowId`. After SSO login, the Login screen's logout transition calls `org.moqui.sso.AuthServices.logout#User` instead of a local-only logout.

## User and group mapping

On a successful IdP callback, `MoquiSecurityGrantedAccessAdapter`:

1. Loads `AuthFlowFieldMap` rows for the flow and evaluates `dstFieldExpression` (or `srcFieldName`) against the pac4j profile attributes. Optional `mappingServiceRegisterId` can transform a value.
2. Finds `UserAccount` by **username** (the pac4j profile username). Updates it, or creates one, with `externalUserId` = profile id plus the mapped fields.
3. Reads IdP **roles** from the profile (`profile.roles` or a `roles` attribute). Each `AuthFlowRoleMap.roleName` maps to a `userGroupId`; memberships are created. Memberships that are no longer in the IdP role set are thru-dated, except `AuthFlow.defaultUserGroupId`.
4. If the user has no remaining group memberships, assigns **defaultUserGroupId**.

Set **defaultUserGroupId** on the AuthFlow so new users get a known artifact-authz set.

## Configuration outline

This is the shape of the records, not a tutorial for any one IdP. Use the IdP's docs for client/app registration.

1. Install `moqui-sso` and restart so `/sso/*` and the Login tab are present.
2. At the IdP, create a client/app. Redirect / ACS URL: `https://your-host/sso/callback`. Copy client id, secret, and discovery URI (OIDC) or metadata URL (SAML).
3. In Moqui (Auto Screens or entity XML), create:
   - `moqui.security.sso.AuthFlow` — `authFlowId`, `authFlowTypeEnumId`, `description` (Login button text), `defaultUserGroupId`, `iconName` optional, `sequenceNum` for button order.
   - Matching `OidcFlow`, `OauthFlow`, or `SamlFlow` with the same `authFlowId`.
   - Optional `AuthFlowFieldMap` rows (for example map IdP `email` to `emailAddress`).
   - Optional `AuthFlowRoleMap` rows (IdP role name → `userGroupId`).
4. Confirm `webapp_https_enabled` / host settings so `ec.web.getWebappRootUrl(true, false)` matches the URL registered at the IdP (Moqui behind a TLS proxy must generate `https://` callback URLs).
5. Open `/Login`, use the SSO tab, and confirm a `UserAccount` is created or updated and can open `/qapps`.

For production, keep client secrets in the database the same way you treat other secrets, and put the WAF/proxy in front of Moqui as described in [Run and Deploy](/docs/framework/Run+and+Deploy) and [Security](/docs/framework/Security).
