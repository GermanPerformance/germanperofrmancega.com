<?xml version="1.0" encoding="UTF-8"?>
<!-- German Performance: how sitemap.xml looks when a person opens it in a
     browser. Search engines never use this file; they read the XML. Same
     Werkstatt palette as assets/css/tokens.css. -->
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:s="http://www.sitemaps.org/schemas/sitemap/0.9"
  xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"
  exclude-result-prefixes="s image">
  <xsl:output method="html" encoding="UTF-8" indent="yes"/>

  <xsl:template match="/">
    <html lang="en">
      <head>
        <meta charset="UTF-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1"/>
        <meta name="robots" content="noindex"/>
        <title>Sitemap · German Performance</title>
        <link rel="icon" href="/assets/img/favicon-144.png"/>
        <link rel="stylesheet" href="/assets/css/fonts.css"/>
        <style>
          :root { color-scheme: dark; }
          * { box-sizing: border-box; }
          body { margin: 0; background: #0a0a0a; color: #d2d5d9;
                 font: 15px/1.5 'Archivo', system-ui, -apple-system, 'Segoe UI', sans-serif; }
          main { max-width: 1100px; margin: 0 auto; padding: 48px 24px 72px; }
          header { border-bottom: 1px solid rgba(255,255,255,.18); padding-bottom: 24px; margin-bottom: 8px; }
          .kicker { color: #d4a017; font-size: 12px; letter-spacing: .14em; text-transform: uppercase; margin: 0 0 10px; }
          h1 { color: #f2f0ec; font-size: clamp(28px, 4vw, 40px); font-weight: 800; letter-spacing: -.02em; line-height: 1.05; margin: 0 0 12px; }
          .lede { color: #9aa0a6; margin: 0; max-width: 60ch; }
          .lede a { color: #f26152; text-decoration: none; }
          .lede a:hover { text-decoration: underline; }
          .stats { display: flex; gap: 32px; flex-wrap: wrap; padding: 20px 0; border-bottom: 1px solid rgba(255,255,255,.09); }
          .stat b { display: block; color: #f2f0ec; font-size: 26px; font-weight: 700; }
          .stat span { color: #8a8f94; font-size: 12px; letter-spacing: .1em; text-transform: uppercase; }
          .wrap { overflow-x: auto; }
          table { width: 100%; border-collapse: collapse; margin-top: 8px; }
          th { text-align: left; color: #8a8f94; font-size: 12px; font-weight: 600; letter-spacing: .1em; text-transform: uppercase;
               padding: 14px 12px 10px; border-bottom: 1px solid rgba(255,255,255,.18); }
          td { padding: 12px; border-bottom: 1px solid rgba(255,255,255,.09); vertical-align: middle; }
          tr:hover td { background: #101214; }
          td.n { color: #8a8f94; width: 3ch; text-align: right; font-variant-numeric: tabular-nums; }
          td.u a { color: #f2f0ec; text-decoration: none; word-break: break-all; }
          td.u a:hover { color: #f26152; }
          td.u small { display: block; color: #8a8f94; font-size: 12px; }
          td.d { color: #d4a017; white-space: nowrap; font-variant-numeric: tabular-nums; }
          td.i { width: 72px; }
          td.i img { display: block; width: 56px; height: 56px; object-fit: cover; border: 1px solid rgba(212,160,23,.42); }
          td.i .none { display: block; width: 56px; height: 56px; border: 1px dashed rgba(255,255,255,.18); }
          footer { color: #8a8f94; font-size: 13px; margin-top: 32px; }
          footer a { color: #9aa0a6; }
        </style>
      </head>
      <body>
        <main>
          <header>
            <p class="kicker">XML sitemap</p>
            <h1>German Performance</h1>
            <p class="lede">Every indexable page on <a href="https://germanperformancega.com/">germanperformancega.com</a>,
              the date it last changed, and the photograph that illustrates it. Search engines read
              the XML behind this page; this view is for people.</p>
          </header>
          <div class="stats">
            <div class="stat"><b><xsl:value-of select="count(s:urlset/s:url)"/></b><span>pages</span></div>
            <div class="stat"><b><xsl:value-of select="count(s:urlset/s:url/image:image)"/></b><span>images</span></div>
            <div class="stat"><b><xsl:for-each select="s:urlset/s:url/s:lastmod"><xsl:sort order="descending"/><xsl:if test="position()=1"><xsl:value-of select="."/></xsl:if></xsl:for-each></b><span>last updated</span></div>
          </div>
          <div class="wrap">
            <table>
              <thead>
                <tr><th>#</th><th>Photo</th><th>Page</th><th>Last modified</th></tr>
              </thead>
              <tbody>
                <xsl:for-each select="s:urlset/s:url">
                  <tr>
                    <td class="n"><xsl:value-of select="position()"/></td>
                    <td class="i">
                      <xsl:choose>
                        <xsl:when test="image:image/image:loc">
                          <img src="{image:image/image:loc}" alt="" loading="lazy" width="56" height="56"/>
                        </xsl:when>
                        <xsl:otherwise><span class="none"></span></xsl:otherwise>
                      </xsl:choose>
                    </td>
                    <td class="u">
                      <a href="{s:loc}"><xsl:value-of select="substring-after(s:loc, 'https://germanperformancega.com')"/></a>
                      <xsl:if test="image:image/image:loc">
                        <small><xsl:value-of select="substring-after(image:image/image:loc, 'https://germanperformancega.com')"/></small>
                      </xsl:if>
                    </td>
                    <td class="d"><xsl:value-of select="s:lastmod"/></td>
                  </tr>
                </xsl:for-each>
              </tbody>
            </table>
          </div>
          <footer>Generated by <code>tools/build_sitemap.py</code>. Robots: <a href="/robots.txt">/robots.txt</a></footer>
        </main>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
