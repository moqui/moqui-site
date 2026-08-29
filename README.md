# moqui-site

Static HTML site for [moqui.org](https://www.moqui.org). Replaces the older `moqui-org` Moqui component. Hosted as a GitHub Pages site and (after cutover) fronted by Cloudflare on the apex domain.

No build step. Pages are HTML at the repository root. Shared header and footer are injected by `/js/site.js`. Third-party libraries are loaded from [cdnjs](https://cdnjs.cloudflare.com), not vendored.

## Local preview

From the repository root (root-absolute URLs need a server, not `file://`):

```bash
python3 serve.py
```

Then open http://127.0.0.1:8080/ . `serve.py` mirrors GitHub Pages: missing extensionless paths are served from `404.html`, so `/docs/framework` loads the documentation viewer.

Plain `python3 -m http.server` also works for real files, but `/docs/{space}/{page}` will not.

## Layout

| Path | Role |
|---|---|
| `index.html`, `framework.html`, `mantle.html`, `applications.html`, `addons.html`, `service.html` | Marketing / directory pages |
| `css/site.css`, `js/site.js` | Theme and shared chrome |
| `docs/` | Markdown documentation viewer |
| `docs/manifest.json` | Space list and page tree (GitHub Pages cannot list directories) |
| `docs/md/{space}/` | Markdown files fetched and rendered in the browser |
| `javadoc/` | Drop generated Javadoc / Groovydoc here (`index.html` is a placeholder until then) |
| `xsd/` | XML schemas, same `/xsd/...` URLs as the previous site |
| `img/` | Logo and related images |
| `CNAME` | `moqui.org` |
| `.nojekyll` | Stop Jekyll from skipping files |

## Documentation viewer

`/docs/` is a client-side viewer (marked + DOMPurify + highlight.js). It is ready for the wiki import:

1. Put markdown at `docs/md/{space}/{Page Name}.md` (nested wiki paths become nested directories).
2. List each page in `docs/manifest.json`.
3. Existing wiki URLs such as `/docs/framework/Quick+Tutorial` map to `Quick Tutorial.md`.

This repository currently ships one stub page per wiki space plus a short Framework Quick Tutorial sample so the viewer can be exercised. The full wiki dump is a separate task.

## CDN pins

Loaded from cdnjs with Subresource Integrity:

- Font Awesome 7.3.1
- marked 18.0.10
- DOMPurify 3.4.14
- highlight.js 11.11.2 (github-dark theme, extra Groovy language)

## GitHub Pages and Cloudflare

Enable Pages from the `master` branch, site root. `CNAME` is already `moqui.org`.

At DNS cutover, point Cloudflare at this Pages origin and add:

- 301 `/m/docs/*` → `/docs/*`
- 301 `/m/alldocs` → `/docs/?view=all`
- Rewrite (not redirect) `/docs/{space}/*` to `/docs/index.html` when the request is not an existing file (`.md`, `.json`, `.js`). GitHub Pages already serves `404.html` for those paths; a Cloudflare rewrite can turn the status into 200.
- Keep `/xsd/*` as static files.

Do not flip the live domain until this site is reviewed.

## Not in this site

- Wiki corpus (import later)
- Full-text search (was Elasticsearch on the old site)
- HiveMind / issue tracking / login hosted on moqui.org (use GitHub and the Forum; demos remain on demo.moqui.org)

Directory listings (add-ons, service providers) are updated by pull request to this repository.
