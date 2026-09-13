"""The make-specific service pages, one module per make.

tools/build_service_pages.py renders every dict in PAGES. Keeping the
copy here, by make, keeps each file readable and the generator small;
tools/service_catalog.py still decides where each page appears.
"""

from .audi import PAGES as AUDI
from .bmw import PAGES as BMW
from .mercedes import PAGES as MERCEDES
from .porsche import PAGES as PORSCHE
from .volkswagen import PAGES as VOLKSWAGEN

PAGES = BMW + MERCEDES + AUDI + PORSCHE + VOLKSWAGEN

_slugs = [p["slug"] for p in PAGES]
if len(_slugs) != len(set(_slugs)):
    raise SystemExit("brand_pages: a slug appears in more than one make module")
