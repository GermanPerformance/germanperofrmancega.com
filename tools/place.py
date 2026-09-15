#!/usr/bin/env python3
"""The shop's Google listing, and every Maps URL the site points at.

Google holds two places at 2144 Parkwood Rd: the building itself (a
compound_building, place ID ChIJEdXuCGO69YgRGGeIaFmvDCk) and the shop's
Business Profile (an auto_repair_shop -- the entity with the name, hours,
photos and the reviews). A map query for the bare street address resolves
to the building, so the old embed pinned "2144 Parkwood Rd" and its "View
larger map" opened the building rather than the shop. Everything here is
built from the listing instead, and the Maps URLs forms carry the place ID
so Google never has to guess.

Verified 2026-09-15 against the embed service's own response: the
name+address query returns gcid:auto_repair_shop with this place ID, the
bare address returns gcid:compound_building, and a keyless `q=place_id:`
query returns no entity at all (blank map, "Open in Maps" button). No API
key is involved, so there is nothing to restrict or pay for.

Import this module; do not spell a Maps URL anywhere else.
"""

import html

NAME = "German Performance"
PLACE_ID = "ChIJJaj9smW69YgR1LaFkB65Sjk"
# The listing's CID: the second half of its feature id (0x394ab91e9085b6d4)
# in decimal. ?cid= is the permanent profile URL, the one sameAs wants.
CID = "4128315549363320532"
# Google's own pin for the listing, as the Business Profile publishes it.
GEO = {"latitude": 33.8456418, "longitude": -84.0556775}

QUERY = "German+Performance,+2144+Parkwood+Rd+NW,+Snellville,+GA+30078"

PROFILE = f"https://maps.google.com/?cid={CID}"
PLACE = ("https://www.google.com/maps/search/?api=1"
         f"&query={QUERY}&query_place_id={PLACE_ID}")
DIRECTIONS = ("https://www.google.com/maps/dir/?api=1"
              f"&destination={QUERY}&destination_place_id={PLACE_ID}")
# The keyless embed geocodes its query itself; with the name in front of
# the address it lands on the listing and draws the business card.
EMBED = f"https://www.google.com/maps?q={QUERY}&output=embed"
WRITE_REVIEW = f"https://search.google.com/local/writereview?placeid={PLACE_ID}"


def attr(url):
    """A URL as an HTML attribute value: the ampersands escaped."""
    return html.escape(url, quote=False)
