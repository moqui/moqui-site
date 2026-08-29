(function () {
  var MANIFEST_URL = "/docs/manifest.json";
  var MD_ROOT = "/docs/md/";
  var cache = {};
  var manifest = null;
  var rootEl = null;

  function pathName() {
    return location.pathname || "/";
  }

  function isDocsAssetPath(path) {
    return (
      path.indexOf("/docs/js/") === 0 ||
      path.indexOf("/docs/md/") === 0 ||
      path.indexOf("/docs/manifest.json") === 0
    );
  }

  function isDocsRoute() {
    var path = pathName();
    if (isDocsAssetPath(path)) return false;
    if (path === "/docs" || path === "/docs/" || path === "/docs/index.html") return true;
    if (path.indexOf("/docs/") === 0) return true;
    if (path.indexOf("/m/docs") === 0 || path.indexOf("/m/alldocs") === 0) return true;
    if ((path === "/docs" || path.indexOf("/docs") === 0) && location.hash.indexOf("#/") === 0) return true;
    return false;
  }

  function decodeSegment(seg) {
    try { seg = decodeURIComponent(seg); } catch (e) { /* keep */ }
    return String(seg).replace(/\+/g, " ");
  }

  function encodeSegment(seg) {
    return encodeURIComponent(seg).replace(/%20/g, "+");
  }

  function parseRoute() {
    var params = new URLSearchParams(location.search);
    var viewAll = params.get("view") === "all";
    var rest = "";
    var path = pathName().replace(/\/+$/, "") || "/";

    if (location.hash.indexOf("#/") === 0) {
      rest = location.hash.slice(2);
    } else if (params.get("p")) {
      rest = params.get("p");
    } else if (path === "/m/alldocs" || path.indexOf("/m/alldocs/") === 0) {
      rest = path.replace(/^\/m\/alldocs\/?/, "");
      viewAll = true;
    } else if (path.indexOf("/m/docs/") === 0) {
      rest = path.slice("/m/docs/".length);
    } else if (path === "/m/docs") {
      rest = "";
    } else if (path === "/docs" || path === "/docs/index.html") {
      rest = "";
    } else if (path.indexOf("/docs/") === 0) {
      rest = path.slice("/docs/".length);
      if (rest === "index.html") rest = "";
    }

    var parts = rest.split("/").filter(Boolean).map(decodeSegment);
    return {
      space: parts[0] || null,
      pagePath: parts.slice(1).join("/"),
      viewAll: viewAll
    };
  }

  function routeHref(space, pagePath, viewAll) {
    if (!space) return viewAll ? "/docs/?view=all" : "/docs/";
    var slug = encodeSegment(space);
    if (pagePath) {
      slug += "/" + pagePath.split("/").map(encodeSegment).join("/");
    }
    return "/docs/" + slug + (viewAll ? "?view=all" : "");
  }

  function navigate(href, replace) {
    if (replace) history.replaceState(null, "", href);
    else history.pushState(null, "", href);
    render();
  }

  function mdUrl(space, pagePath) {
    var file = pagePath ? pagePath + ".md" : "index.md";
    return MD_ROOT + encodeURI(space + "/" + file);
  }

  function fetchText(url) {
    if (cache[url]) return Promise.resolve(cache[url]);
    return fetch(url).then(function (res) {
      if (!res.ok) throw new Error("Not found");
      return res.text();
    }).then(function (text) {
      cache[url] = text;
      return text;
    });
  }

  function spaceTitle(id) {
    if (!manifest) return id;
    for (var i = 0; i < manifest.spaces.length; i++) {
      if (manifest.spaces[i].id === id) return manifest.spaces[i].title;
    }
    return id;
  }

  function pageTitle(space, pagePath) {
    var pages = (manifest.pages && manifest.pages[space]) || [];
    for (var i = 0; i < pages.length; i++) {
      if (pages[i].path === pagePath) return pages[i].title;
    }
    if (!pagePath) return spaceTitle(space);
    var bits = pagePath.split("/");
    return bits[bits.length - 1];
  }

  function renderSpaces(route) {
    var html = "<h2>Wiki Spaces</h2><ul class='space-list'>";
    (manifest.spaces || []).forEach(function (space) {
      var active = space.id === route.space ? " is-active" : "";
      html += "<li><a class='" + active.trim() + "' href='" + routeHref(space.id, "", false) + "' data-docs-link>" + space.title + "</a></li>";
    });
    html += "</ul>";
    html += "<p><a class='docs-all-link' href='" + routeHref(route.space, route.pagePath, true) + "' data-docs-link>All pages</a></p>";
    return html;
  }

  function renderTree(route) {
    if (!route.space) return "";
    var pages = (manifest.pages && manifest.pages[route.space]) || [];
    var html = "<h2>Page Tree</h2><ul class='page-tree'>";
    pages.forEach(function (page) {
      var active = page.path === route.pagePath ? " is-active" : "";
      var indent = page.path ? page.path.split("/").length - 1 : 0;
      var style = indent > 0 ? " style='padding-left:" + (10 + indent * 14) + "px'" : "";
      html += "<li><a class='" + active.trim() + "' href='" + routeHref(route.space, page.path, false) + "' data-docs-link" + style + ">" + page.title + "</a></li>";
    });
    html += "</ul>";
    return html;
  }

  function renderAllPages(route) {
    if (!route.space) {
      return "<div class='docs-empty'><h1>Select a documentation space</h1><p>Choose a space on the left to see its pages.</p></div>";
    }
    var pages = (manifest.pages && manifest.pages[route.space]) || [];
    var html = "<h1>All pages — " + spaceTitle(route.space) + "</h1><ul class='feature-list'>";
    pages.forEach(function (page) {
      var label = page.path ? page.path.replace(/\//g, " / ") : spaceTitle(route.space);
      html += "<li><a href='" + routeHref(route.space, page.path, false) + "' data-docs-link>" + label + "</a></li>";
    });
    html += "</ul>";
    return html;
  }

  function rewriteLinks(container, route) {
    container.querySelectorAll("a[href]").forEach(function (a) {
      var href = a.getAttribute("href") || "";
      if (/^https?:\/\//i.test(href) || href.indexOf("mailto:") === 0) {
        a.setAttribute("target", "_blank");
        a.setAttribute("rel", "noopener noreferrer");
        return;
      }
      var docsMatch = href.match(/^\/(?:m\/)?docs\/?(.*)$/);
      if (docsMatch) {
        var parts = docsMatch[1].split("/").filter(Boolean).map(decodeSegment);
        a.setAttribute("href", routeHref(parts[0] || route.space, parts.slice(1).join("/"), false));
        a.setAttribute("data-docs-link", "");
        return;
      }
      if (href.indexOf("://") === -1 && href.charAt(0) !== "#" && href.charAt(0) !== "/") {
        var resolved = (route.pagePath ? route.pagePath.split("/").slice(0, -1).join("/") : "");
        var combined = (resolved ? resolved + "/" : "") + href.replace(/\.md$/, "");
        a.setAttribute("href", routeHref(route.space, combined, false));
        a.setAttribute("data-docs-link", "");
      }
    });
  }

  function renderMarkdown(md, container, route) {
    var html = window.marked.parse(md, { gfm: true, breaks: false });
    html = window.DOMPurify.sanitize(html, { USE_PROFILES: { html: true } });
    container.innerHTML = html;
    container.querySelectorAll("pre code").forEach(function (block) {
      if (window.hljs) window.hljs.highlightElement(block);
    });
    rewriteLinks(container, route);
  }

  function crumb(route) {
    var parts = ['<a href="/docs/" data-docs-link>Documentation</a>'];
    if (route.space) {
      parts.push('<a href="' + routeHref(route.space, "", false) + '" data-docs-link">' + spaceTitle(route.space) + "</a>");
      if (route.pagePath) {
        var segs = route.pagePath.split("/");
        var acc = [];
        segs.forEach(function (seg, i) {
          acc.push(seg);
          var path = acc.join("/");
          if (i === segs.length - 1) parts.push(pageTitle(route.space, path));
          else parts.push('<a href="' + routeHref(route.space, path, false) + '" data-docs-link">' + seg + "</a>");
        });
      }
    }
    return parts.join(" / ");
  }

  function bindLinks(el) {
    el.addEventListener("click", function (event) {
      var a = event.target.closest("a[data-docs-link]");
      if (!a) return;
      var href = a.getAttribute("href");
      if (!href || a.target === "_blank") return;
      event.preventDefault();
      navigate(href);
    });
  }

  function shellHtml() {
    return (
      '<div class="docs-layout">' +
        '<aside class="docs-sidebar" id="docs-sidebar"></aside>' +
        '<div class="docs-main">' +
          '<div class="docs-toolbar"><nav class="docs-crumb" id="docs-crumb"></nav>' +
          '<button type="button" class="btn btn-secondary docs-mobile-toggle" id="docs-mobile-toggle">Spaces</button></div>' +
          '<article class="md-body" id="docs-article"></article>' +
        "</div>" +
      "</div>"
    );
  }

  function render() {
    if (!rootEl || !manifest) return;
    var route = parseRoute();
    var sidebar = document.getElementById("docs-sidebar");
    var article = document.getElementById("docs-article");
    var crumbEl = document.getElementById("docs-crumb");
    sidebar.innerHTML = renderSpaces(route) + renderTree(route);
    crumbEl.innerHTML = crumb(route);
    document.title = (route.space ? pageTitle(route.space, route.pagePath) + " · " : "") + "Moqui Documentation";

    if (route.viewAll) {
      article.innerHTML = renderAllPages(route);
      return;
    }
    if (!route.space) {
      article.innerHTML = "<div class='docs-empty'><h1>Select a documentation space</h1><p>Choose a space from the list to browse its pages. Wiki content will be added in a later import; the viewer is ready for markdown files under <code>docs/md/</code>.</p></div>";
      return;
    }

    article.innerHTML = "<p class='muted'>Loading…</p>";
    fetchText(mdUrl(route.space, route.pagePath)).then(function (md) {
      renderMarkdown(md, article, route);
    }).catch(function () {
      article.innerHTML = "<div class='docs-error'><h1>Sorry, we couldn't find that page</h1><p>No markdown file at <code>" + mdUrl(route.space, route.pagePath) + "</code>.</p></div>";
    });
  }

  function initViewer() {
    var mount = document.getElementById("docs-root");
    var notFound = document.getElementById("not-found");
    if (!mount) return;
    if (notFound) notFound.hidden = true;
    mount.hidden = false;
    mount.innerHTML = shellHtml();
    rootEl = mount;
    bindLinks(mount);
    var toggle = document.getElementById("docs-mobile-toggle");
    if (toggle) {
      toggle.addEventListener("click", function () {
        document.getElementById("docs-sidebar").classList.toggle("is-open");
      });
    }
    window.addEventListener("popstate", render);
    window.addEventListener("hashchange", render);
    fetch(MANIFEST_URL).then(function (res) {
      if (!res.ok) throw new Error("manifest");
      return res.json();
    }).then(function (data) {
      manifest = data;
      render();
    }).catch(function () {
      document.getElementById("docs-article").innerHTML = "<div class='docs-error'><h1>Could not load documentation index</h1><p>Missing <code>/docs/manifest.json</code>.</p></div>";
    });
  }

  function init() {
    if (!isDocsRoute()) return;
    document.body.setAttribute("data-page", "docs");
    if (typeof window.marked === "undefined" || typeof window.DOMPurify === "undefined") {
      var mount = document.getElementById("docs-root");
      if (mount) mount.innerHTML = "<div class='docs-error'><p>Markdown libraries failed to load from cdnjs.</p></div>";
      return;
    }
    window.marked.setOptions({ gfm: true });
    initViewer();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
