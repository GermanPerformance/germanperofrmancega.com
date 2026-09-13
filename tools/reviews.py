#!/usr/bin/env python3
"""The five Google reviews the homepage shows, as data for the service pages.

index.html keeps its hand-placed review wall; each landing page picks two of
these by key. tools/test_landing_pages.py asserts every quote here still
appears verbatim in index.html, so the two cannot drift apart. Quotes are the
customers' own words, unedited; only the homepage's trailing ellipsis marks a
cut the owner made there.

Fields: name, meta (the line under the name), quote, price ("Great price" tag),
avatar (a letter with a colour key, or an image), photos, services.
"""

REVIEWS = {
    'kayode': {
        "name": 'Kayode Olaoye',
        "meta": '2 reviews · 1 photo',
        "quote": ('This shop offers some of the best service money can buy. All of the workers are reliable and friendly. My car and wallet couldn’t be happier. …'),
        "price": False,
        "avatar": {"letter": 'K', "key": 'kayode'},
        "photos": (
            {"src": 'assets/img/reviews/kayode-audi.webp', "alt": 'Kayode’s grey Audi outside German Performance', "width": 254, "height": 254},
        ),
        "services": None,
    },
    'chelsea': {
        "name": 'Chelsea Brown',
        "meta": '4 reviews',
        "quote": ("I've been coming here for years, and the quality of work and customer service is always great! They also work quickly, so there's very little downtime whenever I drop off my car. I'd recommend German Performance to anyone who needs a trustworthy mechanic!"),
        "price": False,
        "avatar": {"letter": 'C', "key": 'chelsea'},
        "photos": (
        ),
        "services": None,
    },
    'anan': {
        "name": 'anan barghouti',
        "meta": '7 reviews · 1 photo',
        "quote": ('There’s nothing but good things to say about this shop. This car needed a lot of work from oil leaks, engine mounts, airbag light, to coolant leaks, and they did this work in a day. Fast and great work. This if for sure my go to shop from now on. Highly recommend!'),
        "price": True,
        "avatar": {"letter": 'a', "key": 'anan'},
        "photos": (
            {"src": 'assets/img/reviews/anan-mercedes.webp', "alt": 'Anan’s black Mercedes outside German Performance', "width": 254, "height": 254},
        ),
        "services": None,
    },
    'sahir': {
        "name": 'Sahir Razi',
        "meta": '8 reviews · 1 photo',
        "quote": ('I had an excellent experience at this shop. I brought my car in, and from start to finish the service was outstanding. The team was professional, honest, and took the time to explain everything they were doing. They did an absolute 10/10 job, and the quality of the work exceeded my expectations. Their pricing was also very fair, especially considering the level of service and attention to detail. It’s hard to find a shop you can truly trust, but these guys definitely earned my business. I highly recommend them to anyone looking for reliable, high quality work on their German vehicle. I’ll definitely be coming back!'),
        "price": False,
        "avatar": {"letter": 'S', "key": 'sahir'},
        "photos": (
        ),
        "services": None,
    },
    'nageeb': {
        "name": 'Nageeb Alghoul',
        "meta": 'Local Guide · 25 reviews · 34 photos',
        "quote": ("I bought my BMW secondhand and it came with a whole list of issues, so I brought it to Zayd and his team and I'm so glad I did. They fixed my bumper, took care of some engine repairs, and even helped me install customizations including a new steering wheel, front lip, bumper, and side skirts. The whole team was great to work with from start to finish. Honest, skilled, and they clearly take pride in their work. Anytime I need anything for my car, this is where I'm going. Highly recommend!"),
        "price": True,
        "avatar": {"image": 'assets/img/reviews/nageeb-avatar.png', "width": 65, "height": 65},
        "photos": (
            {"src": 'assets/img/reviews/nageeb-bmw-front.webp', "alt": 'Nageeb’s white BMW with a cat on the hood', "width": 255, "height": 255},
            {"src": 'assets/img/reviews/nageeb-bmw-night.webp', "alt": 'Nageeb’s BMW parked beside a lit bridge at night', "width": 255, "height": 255},
            {"src": 'assets/img/reviews/nageeb-bmw-coast.webp', "alt": 'Nageeb’s white BMW at a coastal overlook', "width": 255, "height": 255},
        ),
        "services": 'Transmission, Exhaust, Electrical, Auto engine diagnostic, Engine repair, Vehicle Inspection',
    },
}
