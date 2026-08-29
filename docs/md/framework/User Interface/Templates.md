# Templates

While a wide variety of screens can be built with XML Forms and the various XML Screen widgets and layout elements. Quite a lot can be done with the OOTB elements. Here is an example of a more complex screen, the Task Summary screen from the HiveMind PM application that is made with only OOTB elements and some custom CSS:

<img src="/docs/attachment/100177/summary.png" width="880" height="449" />
<br><br>

Sometimes you need a more flexible layout, styling, widgets, or custom interactive behavior. For things that will be used in many places, and where you want them to render consistently, add screen and form widgets (including layout elements) using FTL macros to add or extend XML Screen elements. For everything else, especially one-off things, an explicit template is the way to get any sort of HTML output you want.

This is especially useful for custom web site such as corporate or ecommerce sites where custom HTML is needed to get a very specific form and function.

Custom templates also apply to other forms of output like XML, CSS, and XSL-FO. In a XML Screen this is done with the *render-mode* element and one or more *text* subelements for each *render-mode.text*.**type** to support for the screen. In the current version of Moqui Framework only text output is supported for screen rendering, but in the future or in custom code other elements under the *render-mode* element could be used to define output for non-text screen rendering such as for GWT or Swing.

If the screen is rendered with a render mode and there is no *text* subelement with a **type** matching the active render mode then it will simply render nothing for the block and continue with rendering the screen. The options for the *text*.**type** attribute match the **type** attribute on the *screen-facade.screen-text-output* element in the Moqui Conf XML file where the macro template to use for each output type is defined. Currently supported options include: csv, html, text, xml, and xsl-fo.

Other attributes (in addition to **type**) available on the *text* element include:

-   **location**: This is the template or text file location and can be any location supported by the Resource Facade including file, http, component, content, etc.
-   **template**: Interpret the text at the location as an FTL or other template? Supports any template type supported by the Resource Facade. Defaults to true, set to false if you want the text included literally.
-   **encode**: If true the text will be encoded so that it does not interfere with markup of the target output. Templates ignore this setting and are never encoded. For example, if output is HTML then data presented will be HTML encoded so that all HTML-specific characters are escaped.
-   **no-boundary-comment**: Defaults to false. If true won't ever put boundary comments before this (for opening ?xml tag, etc).

The `webroot.xml` screen is the default root screen in the OOTB runtime directory and has a good example of including templates for different render modes:

```
<widgets>
  <render-mode>
    <text type="html"
      location="component://webroot/screen/includes/Header.html.ftl"/>
    <text type="xsl-fo" no-boundary-comment="true"
      location="component://webroot/screen/includes/Header.xsl-fo.ftl"/>
  </render-mode>
  <subscreens-active/>
  <render-mode>
    <text type="html"
      location="component://webroot/screen/includes/Footer.html.ftl"/>
    <text type="xsl-fo"><![CDATA[
      ${sri.getAfterScreenWriterText()}
      </fo:flow></fo:page-sequence></fo:root>
      ]]>
    </text>
  </render-mode>
</widgets>
```

This is an example of a screen with subscreens so it has *render-mode* elements before and after the *subscreens-active* element to decorate (or wrap) what comes from the subscreens. This shows text elements with a **location** to include a FTL template and inline *text* in a CDATA block right under the *text* element.
