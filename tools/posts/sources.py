"""The external references the articles cite: (label, url) pairs.

Every URL here was fetched live on 2026-09-15. Prefer manufacturer,
government and standards-body pages; swap a source the day it dies.
NHTSA and the FTC serve their pages to browsers but refuse automated
fetches, so a checker that reports 403 on them is seeing the bot wall,
not a dead page.
"""

BMW_BOOKS = ("BMW USA: Maintenance resources and service and warranty books",
             "https://www.bmwusa.com/explore/bmw-value/bmw-ultimate-service/service-and-warranty-books.html")
MB_MANUALS = ("Mercedes-Benz USA: Service and warranty manuals by model year",
              "https://www.mbusa.com/en/owners/service-warranty-manuals")
MB_FLUIDS = ("Mercedes-Benz Operating Fluids: approved oils, brake fluids and coolants by sheet number",
             "https://operatingfluids.mercedes-benz.com/")
FTC_WARRANTY = ("Federal Trade Commission: Auto warranties and auto service contracts",
                "https://consumer.ftc.gov/articles/auto-warranties-and-auto-service-contracts")
FTC_MAGMOSS = ("Federal Trade Commission: Nixing the Fix &mdash; warranties, Mag-Moss and restrictions on repairs",
               "https://www.ftc.gov/business-guidance/blog/2019/03/nixing-fix-warranties-mag-moss-restrictions-repairs")
ZF_OIL = ("ZF Aftermarket: ZF oil change kits and when transmission oil should be changed",
          "https://aftermarket.zf.com/en/aftermarket-portal/knowledge-hub/inbrief-zf-oil-change-kits/")
EPA_MVAC = ("US EPA: Motor vehicle air conditioner (MVAC) system servicing and Section 609 certification",
            "https://www.epa.gov/mvac")
NHTSA_RECALLS = ("NHTSA: Check for recalls by VIN",
                 "https://www.nhtsa.gov/recalls")
CARFAX = ("CARFAX: Vehicle history reports",
          "https://www.carfax.com/vehicle-history-reports/")
