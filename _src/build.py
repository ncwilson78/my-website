"""Assemble subpages from fragments so every page shares one header and footer."""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "_src"

HEAD = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} | Nicholas Wilson</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="https://ncwilson78.github.io/my-website/{path}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://ncwilson78.github.io/my-website/{path}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta name="twitter:card" content="summary">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;500;600&family=Spectral:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../assets/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<header class="site-head">
  <div class="wrap">
    <a class="site-name" href="../">Nicholas Wilson</a>
    <nav class="site-nav" aria-label="Main">
      <ul>
        <li><a href="../#work"{work_current}>Work</a></li>
        <li><a href="../#notes"{notes_current}>Essays</a></li>
        <li><a href="../#commitments">Principles</a></li>
        <li><a href="../#experience">Experience</a></li>
        <li><a href="../#contact">Contact</a></li>
      </ul>
    </nav>
  </div>
</header>

<main id="main" class="wrap">
"""

FOOT = """
</main>

<footer class="site-foot">
  <div class="wrap">
    <ul>
      <li><a href="mailto:nicholascwilson@gmail.com">Email</a></li>
      <li><a href="https://www.linkedin.com/in/ncwilson78">LinkedIn</a></li>
      <li><a href="https://github.com/ncwilson78">GitHub</a></li>
      <li><a href="https://scholar.google.com/citations?user=HXoupjkAAAAJ">Google Scholar</a></li>
    </ul>
    <p>Views expressed here are my own and do not represent Harvard University. Course content and staff research data are not published on this site.</p>
  </div>
</footer>
</body>
</html>
"""

for frag in sorted(SRC.glob("*/*.html")):
    text = frag.read_text()
    meta = dict(re.findall(r"^<!--\s*(\w+):\s*(.*?)\s*-->$", text, flags=re.M))
    body = re.sub(r"^<!--\s*\w+:.*?-->\n", "", text, flags=re.M)
    section = frag.parent.name
    rel = f"{section}/{frag.name}"
    page = HEAD.format(
        title=meta["title"],
        description=meta["description"].replace('"', "&quot;"),
        path=rel,
        work_current="",
        notes_current="",
    ) + body + FOOT
    out = ROOT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page)
    print("wrote", rel)
