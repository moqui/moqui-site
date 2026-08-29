(function () {
  var NAV = [
    { id: "home", label: "Home", href: "/" },
    {
      id: "ecosystem",
      label: "Ecosystem",
      href: "/framework.html",
      children: [
        { id: "framework", label: "Framework", href: "/framework.html" },
        { id: "mantle", label: "Business Artifacts", href: "/mantle.html" },
        { id: "applications", label: "Applications", href: "/applications.html" },
        { id: "addons", label: "Add-ons", href: "/addons.html" }
      ]
    },
    {
      id: "docs",
      label: "Documentation",
      href: "/docs/",
      children: [
        { id: "docs-moqui", label: "Moqui Community", href: "/docs/moqui" },
        { id: "docs-framework", label: "Moqui Framework", href: "/docs/framework" },
        { id: "docs-mantle", label: "Business Artifacts", href: "/docs/mantle" },
        { id: "docs-apps", label: "Applications", href: "/docs/apps" },
        { id: "docs-javadoc", label: "API Javadoc", href: "/javadoc/" }
      ]
    },
    { id: "service", label: "Service Providers", href: "/service.html" },
    { id: "forum", label: "Forum", href: "https://forum.moqui.org/?utm_source=moqui.org", external: true },
    { id: "github", label: "GitHub", href: "https://github.com/moqui", external: true }
  ];

  var CHILD_PARENT = {
    framework: "ecosystem",
    mantle: "ecosystem",
    applications: "ecosystem",
    addons: "ecosystem"
  };

  function currentPageId() {
    var path = location.pathname || "/";
    if (path.indexOf("/docs") === 0 || path.indexOf("/m/docs") === 0 || path.indexOf("/m/alldocs") === 0) {
      return "docs";
    }
    return document.body.getAttribute("data-page") || "home";
  }

  function isActive(item, pageId) {
    if (item.id === pageId) return true;
    if (CHILD_PARENT[pageId] === item.id) return true;
    if (item.children) {
      for (var i = 0; i < item.children.length; i++) {
        if (item.children[i].id === pageId) return true;
      }
    }
    return false;
  }

  function linkAttrs(item, pageId) {
    var attrs = 'href="' + item.href + '"';
    if (item.external) attrs += ' target="_blank" rel="noopener noreferrer"';
    if (item.id === pageId || (item.children && item.children.some(function (c) { return c.id === pageId; }))) {
      attrs += ' aria-current="page"';
    }
    return attrs;
  }

  function renderNav(pageId) {
    return NAV.map(function (item) {
      var active = isActive(item, pageId) ? " is-active" : "";
      if (item.children) {
        var kids = item.children.map(function (child) {
          return '<li><a ' + linkAttrs(child, pageId) + ">" + child.label + "</a></li>";
        }).join("");
        return (
          '<li class="has-children' + active + '">' +
            '<a class="nav-parent" ' + linkAttrs(item, pageId) + '>' +
              item.label + ' <i class="fa-solid fa-chevron-down" aria-hidden="true"></i>' +
            "</a>" +
            '<ul class="dropdown">' + kids + "</ul>" +
          "</li>"
        );
      }
      return '<li class="' + active.trim() + '"><a ' + linkAttrs(item, pageId) + ">" + item.label + "</a></li>";
    }).join("");
  }

  function renderHeader(pageId) {
    return (
      '<a class="skip-link" href="#main">Skip to content</a>' +
      '<div class="util-bar"><div class="util-bar-inner">' +
        '<span><a href="https://demo.moqui.org/qapps" target="_blank" rel="noopener noreferrer">Apps demo</a>' +
        " · " +
        '<a href="https://demo.moqui.org/store" target="_blank" rel="noopener noreferrer">eCommerce demo</a></span>' +
        '<span>Questions? <a href="https://forum.moqui.org/?utm_source=moqui.org" target="_blank" rel="noopener noreferrer">Join the Forum</a>' +
        " · " +
        '<a href="https://github.com/moqui/moqui-framework/releases/latest">Download latest</a></span>' +
      "</div></div>" +
      '<nav class="site-nav" aria-label="Primary">' +
        '<div class="nav-inner">' +
          '<a class="logo" href="/" aria-label="Moqui home">' +
            '<img src="/img/MoquiLogoNew.png" alt="Moqui">' +
          "</a>" +
          '<button type="button" class="nav-toggle" aria-expanded="false" aria-label="Open menu">' +
            '<i class="fa-solid fa-bars" aria-hidden="true"></i>' +
          "</button>" +
          '<ul class="nav-list">' + renderNav(pageId) + "</ul>" +
        "</div>" +
      "</nav>"
    );
  }

  function renderFooter() {
    return (
      '<footer class="site-footer"><div class="footer-inner">' +
        '<div class="footer-grid">' +
          "<div>" +
            "<h2>Moqui Ecosystem</h2>" +
            "<p>Open source framework, business artifacts, and applications — public domain (CC0) with a patent grant.</p>" +
            '<p><a href="https://creativecommons.org/publicdomain/zero/1.0/">CC0 1.0 Universal</a> · ' +
            '<a href="https://github.com/moqui/moqui-framework/blob/master/LICENSE.md">License</a></p>' +
          "</div>" +
          "<div><h2>Explore</h2><ul>" +
            '<li><a href="/framework.html">Framework</a></li>' +
            '<li><a href="/mantle.html">Business Artifacts</a></li>' +
            '<li><a href="/applications.html">Applications</a></li>' +
            '<li><a href="/docs/">Documentation</a></li>' +
          "</ul></div>" +
          "<div><h2>Community</h2><ul>" +
            '<li><a href="https://forum.moqui.org/?utm_source=moqui.org" target="_blank" rel="noopener noreferrer">Forum</a></li>' +
            '<li><a href="https://github.com/moqui" target="_blank" rel="noopener noreferrer">GitHub</a></li>' +
            '<li><a href="/service.html">Service Providers</a></li>' +
            '<li><a href="/addons.html">Add-ons</a></li>' +
          "</ul></div>" +
        "</div>" +
        '<div class="footer-copy">This site is static HTML hosted on GitHub Pages. Directory listings are maintained by pull request to <a href="https://github.com/moqui/moqui-site">moqui/moqui-site</a>.</div>' +
      "</div></footer>"
    );
  }

  function bindNav(root) {
    var nav = root.querySelector(".site-nav");
    var toggle = root.querySelector(".nav-toggle");
    if (toggle && nav) {
      toggle.addEventListener("click", function () {
        var open = nav.classList.toggle("is-open");
        toggle.setAttribute("aria-expanded", open ? "true" : "false");
        toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      });
    }
  }

  function init() {
    var pageId = currentPageId();
    var header = document.getElementById("site-header");
    var footer = document.getElementById("site-footer");
    if (header) {
      header.innerHTML = renderHeader(pageId);
      bindNav(header);
    }
    if (footer) footer.innerHTML = renderFooter();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
