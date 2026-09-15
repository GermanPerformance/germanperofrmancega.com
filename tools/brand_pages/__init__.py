"""The brand hubs' copy, one module per make.

tools/build_brand_hubs.py renders every HUB dict in HUBS. Keeping the copy
here, by make, keeps each file readable and the generator small;
tools/service_catalog.py still decides where each hub appears. Until
2026-09-15 these modules held the make-specific job pages, since retired
into the hubs (tools/redirects.py forwards their addresses).
"""

from .audi import HUB as AUDI
from .bmw import HUB as BMW
from .mercedes import HUB as MERCEDES
from .porsche import HUB as PORSCHE
from .volkswagen import HUB as VOLKSWAGEN

HUBS = (BMW, MERCEDES, AUDI, PORSCHE, VOLKSWAGEN)

_slugs = [h["slug"] for h in HUBS]
if len(_slugs) != len(set(_slugs)):
    raise SystemExit("brand_pages: a slug appears in more than one make module")
