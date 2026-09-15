"""The supporting articles, as one registry.

Each article lives in the module of the money page it supports:
posts/general.py for the homepage, posts/bmw.py and posts/mercedes.py for
the two brand hubs. This package joins them so tools/build_posts.py,
tools/build_schema.py, tools/build_llms_txt.py and the brand hubs read one
POSTS, one POST_DATES and one READING, and so the guides index knows how
the articles group.

A post dict carries: slug, hub (the money page it supports), cluster,
title, description, eyebrow, h1, dek, intro, sections, sources, further,
cta_heading, cta_text. Blocks inside a section are a paragraph string,
("h3", text), ("list", [...]), ("callout", text) or ("table", (headers,
rows)). sources is a list of (label, url) external references; further
lists the slugs of related articles.
"""

from posts import bmw, general, mercedes
from posts.common import (  # noqa: F401
    AUTHOR_NOTE, BMW_HUB, COSTS, DEALER, DIAGNOSTICS, HOME, HOME_PAGE,
    MERCEDES_HUB, PROCESS, REPAIRS, SERVICES, STORY, link,
)

_MODULES = (general, bmw, mercedes)

POSTS = [post for m in _MODULES for post in m.POSTS]
POST_DATES = {slug: dates for m in _MODULES for slug, dates in m.POST_DATES.items()}
READING = {slug: title for m in _MODULES for slug, title in m.READING.items()}
SUMMARY = {slug: line for m in _MODULES for slug, line in m.SUMMARY.items()}

# Which money page each article on disk supports, the hand-written one included.
HUB_OF = {**{slug: meta["hub"] for slug, meta in general.HAND_WRITTEN.items()},
          **{post["slug"]: post["hub"] for post in POSTS}}
CLUSTER_OF = {**{slug: meta["cluster"] for slug, meta in general.HAND_WRITTEN.items()},
              **{post["slug"]: post["cluster"] for post in POSTS}}

# How the guides index and the nav group the articles: heading, hub, slugs
# in reading order (the hand-written dealer piece leads the general set).
GUIDES = (
    ("German cars", HOME_PAGE, (DEALER, COSTS, DIAGNOSTICS)),
    ("BMW", BMW_HUB, tuple(post["slug"] for post in bmw.POSTS)),
    ("Mercedes-Benz", MERCEDES_HUB, tuple(post["slug"] for post in mercedes.POSTS)),
)

# The guides index page.
GUIDES_PAGE = "guides.html"


def guides_for(hub):
    """The article slugs that support a money page, in reading order."""
    return tuple(slug for _, h, slugs in GUIDES for slug in slugs if h == hub)


def _check():
    seen = set()
    for post in POSTS:
        for key in ("slug", "hub", "cluster", "title", "description", "eyebrow", "h1",
                    "dek", "intro", "sections", "sources", "further", "cta_heading", "cta_text"):
            if key not in post:
                raise SystemExit(f"posts: {post.get('slug')}: missing {key}")
        if post["slug"] in seen:
            raise SystemExit(f"posts: duplicate slug {post['slug']}")
        seen.add(post["slug"])
        for other in post["further"]:
            if other not in READING:
                raise SystemExit(f"posts: {post['slug']}: further reading {other} has no title")
    for slug in POST_DATES:
        if slug not in READING or slug not in SUMMARY:
            raise SystemExit(f"posts: {slug}: needs a READING title and a SUMMARY line")
    for _, _, slugs in GUIDES:
        for slug in slugs:
            if slug not in POST_DATES:
                raise SystemExit(f"posts: guides list {slug}, which has no dates")


_check()
