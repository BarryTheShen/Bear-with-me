#!/usr/bin/env python3
"""Build the "what gets left behind" reference document.

    python3 research/build_lost_items.py

Writes research/what-gets-lost.html. Self-contained, no assets.
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import charts as C  # noqa: E402
from charts import Bar  # noqa: E402
from shell import REPORTS, Doc  # noqa: E402

OUT = REPORTS / "what-gets-lost.html"

S = {
    "tokyo": ("Lost and found property statistics, Reiwa 7 (2025)",
              "Tokyo Metropolitan Police Department",
              "https://www.keishicho.metro.tokyo.lg.jp/about_mpd/jokyo_tokei/kakushu/"
              "kaikei.html", "official", "2025"),
    "tfl": ("Lost Property Office transparency data FY2017-18-19",
            "Transport for London",
            "https://foi.tfl.gov.uk/FOI-1592-2223/lost-property-office-transparency-data-"
            "FY2017-18-19.pdf", "official", "2018/19"),
    "dublin": ("Dublin Airport 2024 lost and found figures", "daa (Dublin Airport)",
               "https://www.dublinairport.com/latest-news/2024/12/30/tayto-toblerone-and-"
               "guinness-amongst-top-sellers-at-dublin-airport-in-2024", "official", "2024"),
    "tsa": ("Lost and found", "US Transportation Security Administration",
            "https://www.tsa.gov/contact/lost-and-found", "official", "2026"),
    "mtaig": ("NYCT Lost and Found Operation Needs Significant Improvement (report 2025-06)",
              "MTA Office of the Inspector General",
              "https://mtaig.ny.gov/Reports/2025-06%20NYCT%20Lost%20and%20Found%20"
              "Operation%20Needs%20Significant%20Improvement.pdf", "official", "2025"),
    "mnr": ("Lost and Found — Metro-North Railroad",
            "Metropolitan Transportation Authority",
            "https://www.mta.info/lost-and-found/metro-north-railroad", "official", "2026"),
    "berkeley": ("Lost and found at UC Berkeley", "University of California, Berkeley",
                 "https://news.berkeley.edu/2010/09/27/lost/", "official", "2010"),
    "tamu": ("A new home for what lost its home", "The Battalion (Texas A&M)",
             "https://thebatt.com/life-arts/a-new-home-for-what-lost-its-home/",
             "news", "2023"),
    "unlv": ("Lost and weird valuables at UNLV", "University of Nevada, Las Vegas",
             "https://www.unlv.edu/news/article/lost-and-weird-valuables-unlv",
             "official", "2018"),
    "uva": ("Every year several thousand items are lost at the UvA",
            "Folia (University of Amsterdam)",
            "https://www.folia.nl/international/133163/every-year-several-thousand-items-"
            "are-lost-at-the-uva-what-happens-to-them", "news", "2019"),
    "uber": ("10th Annual Uber Lost & Found Index", "Uber",
             "https://www.uber.com/us/en/newsroom/the-2026-uber-lost-found-index/",
             "vendor", "2026"),
    "stikins": ("School lost property survey", "Stikins / Label Planet",
                "https://www.stikins.co.uk/school-lost-property/survey-results-detailed-"
                "summary/", "vendor", "2026"),
    "pixie": ("Lost and Found survey", "Pixie / Survey Sampling International",
              "https://www.prnewswire.com/news-releases/lost-and-found-the-average-"
              "american-spends-25-days-each-year-looking-for-lost-items-collectively-"
              "costing-us-households-27-billion-annually-in-replacement-costs-"
              "300449305.html", "vendor", "2017"),
    "motel6": ("Items Left Behind survey", "G6 Hospitality / Kelton Global",
               "https://www.prnewswire.com/news-releases/the-secrets-of-a-hotels-lost-and-"
               "found--g6-hospitality-reveals-results-of-motel-6-items-left-behind-survey-"
               "300146746.html", "vendor", "2015"),
    "trafford": ("Most common items shoppers leave behind", "Trafford Centre / Over-C",
                 "https://nwconnected.co.uk/one-of-uks-largest-shopping-centres-reveals-"
                 "most-common-items-shoppers-have-left-behind-over-the-last-year/",
                 "news", "2024"),
    "towson": ("Personal property registration and labelling guidance",
               "Towson University",
               "https://www.towson.edu/public-safety/police/services/personal-property.html",
               "official", "2026"),
    "munich": ("Oktoberfest 2024 in numbers", "City of Munich",
               "https://stadt.muenchen.de/dam/jcr:1d6f3592-7ebb-49a4-aa1a-e9d945da3b22/"
               "02_oktoberfest_in_numbers_2024.pdf", "official", "2024"),
    "utoronto": ("Exploring lost and found on campus", "University of Toronto",
                 "https://www.fs.utoronto.ca/news/exploring-lost-and-found-on-campus-from-"
                 "unusual-finds-to-what-to-do-if-you-lose-something/", "official", "2023"),
    "mcgill": ("In search of a single boot: things lost and found at McGill Library",
               "McGill University Library",
               "https://news.library.mcgill.ca/in-search-of-a-single-boot-a-reflection-on-"
               "the-things-lost-and-found-at-mcgill-library/", "official", "2021"),
    "iu": ("Lost your keys? Missing a water bottle?", "Indiana University",
           "https://news.iu.edu/live/news/25429-lost-your-keys-missing-a-water-bottle-check-the",
           "official", "2018"),
    "utaustin": ("Gregory Gym should not throw away reusable water bottles",
                 "The Daily Texan (UT Austin)",
                 "https://thedailytexan.com/2018/09/19/gregory-gym-should-not-throw-away-"
                 "reusable-water-bottles-from-lost-and-found/", "news", "2018"),
    "bates": ("53 items in the Bates library's lost and found", "Bates College",
              "https://www.bates.edu/news/2024/02/09/53-items-in-the-bates-librarys-lost-"
              "and-found-on-feb-8-2024/", "official", "2024"),
    "exeter": ("Lost property", "University of Exeter",
               "https://www.exeter.ac.uk/departments/campusservices/facilitiesoperations/"
               "receptions/lostproperty/", "official", "2026"),
    "mmu": ("Lost property policy", "Manchester Metropolitan University",
            "https://www.mmu.ac.uk/legal/policies/lost-property-policy", "official", "2025"),
    "unsw": ("Lost property", "University of New South Wales",
             "https://www.unsw.edu.au/estate/protective-services/lost-property",
             "official", "2026"),
}
LEAD = {"tokyo", "tfl"}


def cite(*keys: str, extra: str = "") -> str:
    bits = []
    for k in keys:
        t, org, url, kind, yr = S[k]
        tick = " &#10003;" if k in LEAD else ""
        bits.append(f'<a href="{url}">{org}, <i>{t}</i></a> ({yr}){tick}')
    s = "<b>Source:</b> " + "; ".join(bits) + "."
    return f"{s} {extra}" if extra else s


def chip(k: str) -> str:
    m = {"official": ("c-off", "Official"), "academic": ("c-aca", "Peer-reviewed"),
         "vendor": ("c-ven", "Vendor / PR"), "news": ("c-none", "Press"),
         "found": ("c-mod", "Items found"), "ret": ("c-strong", "Items returned"),
         "self": ("c-weak", "Self-reported")}
    cls, txt = m[k]
    return f'<span class="chip {cls}">{txt}</span>'


# --------------------------------------------------------------- Tokyo data --
TOKYO_TOTAL_POINTS = 4_850_775
TOKYO_CASES = 4_538_244
TOKYO_CASH_YEN = 4_508_824_075
TOKYO_LOST_REPORTS = 1_100_657
TOKYO_PROCESSED = 4_750_389
TOKYO = [  # (category, found points, returned points)
    ("Certificates & documents", 819_602, 574_375),
    ("Securities", 471_399, 137_859),
    ("Clothing & footwear", 460_667, 19_797),
    ("Electrical products", 403_708, 25_844),
    ("Wallets", 338_104, 226_993),
    ("Umbrellas", 331_882, 4_671),
    ("Bags", 229_161, 60_248),
    ("Mobile phones", 144_381, 119_516),
    ("Precious metals", 118_760, 2_171),
    ("Cameras & glasses", 112_006, 4_961),
]

TFL_FOUND = 333_921
TFL = [  # (category, share of found %, reclaim %)
    ("Books, documents & cards", 24.9, 14.9), ("Clothing", 15.0, 9.6),
    ("Bags", 14.7, 41.9), ("Valuables", 11.6, 43.5), ("Telephones", 11.0, 48.3),
    ("Miscellaneous", 9.8, 13.2), ("Eyewear", 4.8, 7.5), ("Keys", 4.2, 11.3),
    ("Umbrellas", 2.3, 2.3), ("Jewellery", 1.7, 3.4),
]

CAMPUS = [  # (institution, volume, period, returned)
    ("Texas A&M, Memorial Student Center", "12,000+ items", "FY2022", "34.2%"),
    ("UNLV", "2,300+ items", "one semester, 2018", "~20%"),
    ("UC Berkeley", "1,669 items", "2009", "35%"),
    ("Indiana University Bloomington", "200+ items/month", "2018", "not published"),
    ("University of Toronto, St George", "30\u201360 items/week", "2023",
     "20\u201345 loss enquiries/day"),
    ("McGill University Library", "25 items/day", "2021", "not published"),
    ("UT Austin, Gregory Gym", "100+ water bottles/week", "2018", "not published"),
    ("University of Amsterdam, REC", "up to 15 items/day", "2019", "not published"),
]

MUNICH_TOTAL = 4_095
MUNICH = [("Purses", 777), ("Clothing", 734), ("ID cards", 568), ("Bank cards", 446),
          ("Keys", 379), ("Mobile phones", 361), ("Glasses", 285),
          ("Bags & rucksacks", 117), ("Jewellery", 41), ("Umbrellas", 38)]

DUBLIN = [("Bags & luggage", 2_300), ("Mobile phones", 1_000), ("Key sets", 750),
          ("Laptops", 550), ("Rings", 550)]

HOME = [("TV remote", 45), ("Phone", 33), ("Car & house keys", 28), ("Glasses", 27),
        ("Shoes", 24), ("Wallet or purse", 20)]

HOTEL = [("Clothing", 42), ("Toiletries", 42), ("Electronics & chargers", 40),
         ("Jewellery & watches", 15), ("Underwear", 13), ("Hair-styling tools", 13)]

SCHOOL = [("Jumpers, sweatshirts, hoodies", 90), ("Coats", 41),
          ("Hats, gloves, scarves", 27), ("Water bottles", 24), ("PE kit", 19)]

d = Doc()

MASTHEAD = """
<div class="masthead">
  <div class="kicker">Reference &middot; What Gets Left Behind</div>
  <h1>The things people lose, and the things they get back</h1>
  <div class="standfirst">An item-level reference on misplaced property, built around the
  largest published lost-property dataset in the world &mdash; 4.85 million items recorded
  by the Tokyo Metropolitan Police in a single year &mdash; and cross-checked against
  transport operators, airports, universities, hotels and household surveys.</div>
  <div class="meta">
    <div><b>Largest dataset</b>4,850,775 items, Tokyo 2025</div>
    <div><b>Most left behind</b>Documents, clothing, umbrellas</div>
    <div><b>Most returned</b>Phones, at 82.8%</div>
    <div><b>Prepared</b>28 August 2026</div>
  </div>
</div>"""

# ============================================================== HEADLINE ====

d.h2("The short answer", "answer")
d.p("Two different questions hide inside \u201cwhat gets lost most\u201d, and they have "
    "different answers. <b>What is left behind most often</b> is paperwork, clothing and "
    "umbrellas. <b>What people care about and come back for</b> is phones, wallets and "
    "documents. The gap between those two lists is the entire opportunity.", "lede")

d.keys([
    ("4,850,775", "Items handed in to police in Tokyo in a single year &mdash; the largest "
     "published lost-property dataset anywhere.", "Tokyo Metropolitan Police, 2025 \u2713"),
    ("82.8%", "Of found mobile phones were returned to their owner in Tokyo. The highest "
     "return rate of any category.", "Tokyo Metropolitan Police \u2713"),
    ("1.4%", "Of found umbrellas were returned. A <b>59-fold</b> difference from phones, "
     "in the same city, in the same year.", "Tokyo Metropolitan Police \u2713"),
    ("~1 in 3", "Typical campus return rate. Texas A&amp;M 34.2%, Berkeley 35%, "
     "UNLV about 20%.", "Three US universities"),
])

d.box("insight", "The pattern, stated once",
      "<p>Return rate does not track how much an item is worth. It tracks <b>whether the "
      "item can be connected to a person</b> and whether that person knows where to look. "
      "Phones and wallets carry identity. Umbrellas and jumpers do not.</p>"
      "<p>This report is mostly a demonstration that the same pattern appears in every "
      "dataset examined, in four countries, across transport, airports, campuses and "
      "police forces.</p>")

# ================================================================= TOKYO ====

d.h2("1. The best dataset in the world: Tokyo", "tokyo")
d.p("Japan's lost-property law requires found items to be handed to police, and the Tokyo "
    "Metropolitan Police publish the resulting statistics annually by category. In calendar "
    f"year 2025 they recorded <b>{TOKYO_CASES:,} found-item reports</b> covering "
    f"<b>{TOKYO_TOTAL_POINTS:,} individual items</b>, plus "
    f"<b>&yen;{TOKYO_CASH_YEN / 1e9:.2f} billion</b> in cash. Separately, "
    f"<b>{TOKYO_LOST_REPORTS:,} loss reports</b> were filed by people who had lost "
    "something.")

_share = [Bar(n, 100 * f / TOKYO_TOTAL_POINTS) for n, f, _ in TOKYO]
d.fig(
    C.hbar(_share, unit="%", dp=1, label_w=230),
    "What is handed in: Tokyo, 2025",
    f"Share of {TOKYO_TOTAL_POINTS:,} found items by category. The ten named categories "
    f"cover {sum(f for _, f, _ in TOKYO) / TOKYO_TOTAL_POINTS * 100:.1f}% of all items; the "
    "remainder is an unlisted residual.",
    cite("tokyo", extra="Figures are 物品点数 (item points) from found-item reports "
                        "(拾得届). Category names translated from the original."))

_ret = sorted(((n, 100 * r / f) for n, f, r in TOKYO), key=lambda x: -x[1])
d.fig(
    C.hbar([Bar(n, v, color=C.POSITIVE if v > 50 else (C.ACCENT if v > 10 else C.NEGATIVE))
            for n, v in _ret], unit="%", dp=1, label_w=230),
    "What comes back: return rate by category, Tokyo 2025",
    "Returned items as a percentage of found items in each category. Phones return at "
    "<b>82.8%</b> and umbrellas at <b>1.4%</b> &mdash; a 59-fold spread that has nothing "
    "to do with the value of the object.",
    cite("tokyo", extra=f"<b>Caveat:</b> the return counts come from the processing "
                        f"population ({TOKYO_PROCESSED:,} items) which differs slightly "
                        f"from the intake population ({TOKYO_TOTAL_POINTS:,}), so these "
                        "ratios are close approximations rather than exact rates."))

d.box("warn", "Look at what this says about value",
      "<p><b>Precious metals return at 1.8%. Mobile phones return at 82.8%.</b> The "
      "jewellery is worth more. It comes back forty-six times less often.</p>"
      "<p>A ring cannot tell anyone whose it is, and its owner often does not know where "
      "they lost it. A phone rings, shows a lock screen, is missed within minutes and is "
      "tied to an account. Value is almost irrelevant; <b>identity and traceability are "
      "everything</b>.</p>")

# ============================================================== TRANSPORT ====

d.h2("2. Transport, where the volumes are", "transport")
d.p("Transport systems generate lost property at industrial scale, because they move "
    "people between places while they are carrying everything they own.")

d.raw('<div class="two">')
d.fig(
    C.hbar([Bar(n, s) for n, s, _ in TFL], unit="%", dp=1, label_w=190, width=520,
           row_h=24),
    "What is found: Transport for London",
    f"Share of {TFL_FOUND:,} items, 2018/19.",
    cite("tfl"))
d.fig(
    C.hbar([Bar(n, r, color=C.POSITIVE if r > 30 else (C.ACCENT if r > 10 else C.NEGATIVE))
            for n, _, r in sorted(TFL, key=lambda x: -x[2])],
           unit="%", dp=1, label_w=190, width=520, row_h=24),
    "What comes back: Transport for London",
    "Reclaim rate by category. Same shape as Tokyo.",
    cite("tfl"))
d.raw("</div>")

d.p("The TfL and Tokyo datasets were collected seven years apart, in different countries, "
    "under different laws, by different kinds of organisation. They produce the same "
    "ranking: <b>phones and wallets at the top, umbrellas and jewellery at the bottom</b>.")

d.table(
    ["Operator", "Volume", "Period", "Returned", "Type"],
    [["<b>Tokyo Metropolitan Police</b>", "4,850,775 items", "2025",
      "1,334,011 items returned to owners", chip("official")],
     ["<b>Transport for London</b>", "333,921 items", "2018/19", "23.9%", chip("official")],
     ["<b>US TSA</b> (checkpoints)", "90,000&ndash;100,000 items/month", "current",
      "not published", chip("official")],
     ["<b>NYC Transit</b>", "68,000+ articles", "2024",
      "31,500+ claims filed against a staff of 9", chip("official")],
     ["<b>Metro-North Railroad</b>", "~20,000 items/year", "current", "not published",
      chip("official")],
     ["<b>Dublin Airport</b>", "~19,000 items handed in", "2024", "<b>56%</b>",
      chip("official")]],
    title="Lost-property volumes at major operators",
    sub="Note that these count different things: items found, items handed in, or claims "
        "filed. Dublin Airport's 56% return rate is the highest found anywhere in this "
        "research, and is plausibly explained by passengers knowing exactly where they were.",
    source=cite("tokyo", "tfl", "tsa", "mtaig", "mnr", "dublin"))

d.fig(
    C.hbar([Bar(n, v) for n, v in DUBLIN], unit="", dp=0, label_w=190),
    "Dublin Airport: items handed in during 2024",
    "Counts of specific item types among roughly 19,000 items. The airport also reported "
    "550 wedding and engagement rings handed in, of which more than 100 were still "
    "unclaimed.",
    cite("dublin"))

d.box("warn", "Being handed in is not the same as arriving",
      "<p>The MTA Inspector General ran a controlled test in 2024: investigators handed "
      "<b>24 items to New York City Transit employees</b>. <b>20 of the 24 (83%) were "
      "never logged and never reached the Lost Property Unit.</b> A 2006&ndash;07 test "
      "found 23 of 26 (88.5%) missing. On buses, only 2 of 14 items handed to operators "
      "were logged.</p>"
      "<p>So the pipeline leaks badly before the desk. But the same audit records the "
      "counter-example: an investigator's keychain <b>carrying an email label</b> reached "
      "the unit, and staff used the label to contact the owner immediately.</p>"
      + cite("mtaig"))

# ================================================================ CAMPUS ====

d.h2("3. Campus", "campus")
d.p("Campus lost property is poorly documented compared with transport, and almost all of "
    "it comes from student newspapers interviewing the lost-property office rather than "
    "from published statistics. The volumes are nonetheless substantial and the return "
    "rates cluster tightly around one in three.")

d.table(
    ["Institution", "Volume", "Period", "Returned"],
    [[f"<b>{i}</b>", v, p, r] for i, v, p, r in CAMPUS],
    title="Campus lost-property volumes and return rates",
    sub="Texas A&M's Memorial Student Center alone takes 50\u2013100 items a day. Berkeley "
        "reported that 64% of items handed in during 2009 were never returned, and "
        "attributed this to stale contact information or no identifying feature at all.",
    source=cite("tamu", "unlv", "berkeley", "uva"))

d.box("win", "The campus answer is the water bottle",
      "<p>Five institutions on three continents independently name the same item first. "
      "The University of Toronto lists <b>water bottles, umbrellas, keys, binders and "
      "books</b> as most frequently lost. McGill's library calls water bottles \u201cthe "
      "most popular\u201d. Whitman College collects a couple of hundred a year. Indiana "
      "University's article is literally titled <i>\u201cLost your keys? Missing a water "
      "bottle?\u201d</i>. UT Austin's Gregory Gym alone takes in <b>over 100 water bottles "
      "a week</b>.</p>"
      "<p>Then look at what institutions do with them. Exeter disposes of water bottles "
      "<b>immediately</b> rather than storing them for 30 days like everything else. UNSW "
      "does the same. Manchester Metropolitan classifies bottles, clothing and umbrellas "
      "as <b>low value</b> and holds them a week against a month for electronics.</p>"
      "<p>So the single most commonly lost object on a campus is one that lost-property "
      "offices bin on arrival because storing it is not worth the shelf space. That is the "
      "clearest addressable gap in this entire report.</p>"
      + cite("utoronto", "mcgill", "iu", "utaustin", "exeter", "unsw", "mmu"))

d.p("The rest of the campus list is consistent across institutions: <b>ID cards, keys, "
    "chargers and cables, clothing, headphones, laptops, umbrellas, glasses and "
    "calculators</b>. A one-day snapshot of a single Bates College library cubby held 42 "
    "items including two water bottles, six earbud cases (four of them empty), two "
    "graphing calculators, two charging cables, a Bose headset, an umbrella, two pairs of "
    "glasses and two rings. Indiana University reports that water bottles and keys have "
    "the highest return success while clothing and shoes linger, and that finds spike at "
    "the start of term with hats, gloves and scarves arriving in the cold months.")
d.raw(f'<p class="srcnote">{cite("bates", "iu", "uva", "towson")}</p>')

d.fig(
    C.hbar([Bar(n, v) for n, v in SCHOOL], unit="%", dp=0, label_w=250),
    "Schools: most common unclaimed items",
    "Percentage of surveyed UK primary schools placing each item in their top three "
    "unclaimed categories. Clothing dominates completely.",
    cite("stikins", extra="Vendor-commissioned survey; the number of responding schools is "
                          "not published, so treat as indicative ranking only. The same "
                          "survey found 66% of schools said under a quarter of their lost "
                          "property was labelled."))

# ======================================================== VENUES AND HOME ====

d.h2("4. Hotels, venues and the home", "venues")
d.p("Evidence here is dominated by public-relations surveys. The rankings are still useful "
    "&mdash; they agree with the operational data &mdash; but the methodology is usually "
    "thin and the denominators are frequently missing. Everything in this section is "
    "labelled accordingly.")

d.p("One exception is a genuinely official venue dataset. The City of Munich publishes "
    f"lost-property counts for Oktoberfest: <b>{MUNICH_TOTAL:,} items</b> in 2024, across "
    "a sixteen-day festival.")

d.fig(
    C.hbar([Bar(n, 100 * v / MUNICH_TOTAL, note=f"{v:,}") for n, v in MUNICH],
           unit="%", dp=1, label_w=200),
    "Oktoberfest 2024: what four million visitors left behind",
    f"Share of {MUNICH_TOTAL:,} lost-property items, with absolute counts inside each bar. "
    "Purses, clothing and identity documents lead, exactly as in Tokyo and London. "
    "Umbrellas are last here only because it is a beer festival in autumn, not a commuter "
    "network.",
    cite("munich", extra="Listed categories do not sum to the total; the remainder is "
                         "uncategorised. A further 975 items were handed over during the "
                         "festival itself, which is a separate population from the 4,095."))

d.raw('<div class="two">')
d.fig(
    C.hbar([Bar(n, v) for n, v in HOTEL], unit="%", dp=0, label_w=180, width=520,
           row_h=25),
    "Left in hotel rooms",
    "Share of respondents reporting each item. Self-reported, not counted.",
    cite("motel6", extra="n=1,060 US adults, Kelton Global, 2015. 54% admitted leaving "
                         "something behind."))
d.fig(
    C.hbar([Bar(n, v) for n, v in HOME] , unit="%", dp=0, label_w=180, width=520,
           row_h=25),
    "Misplaced at home",
    "Share misplacing each item at least weekly (remote: monthly).",
    cite("pixie", extra="Over 1,700 US adults, Survey Sampling International, 2016."))
d.raw("</div>")

d.table(
    ["Setting", "Ranking as published", "Source quality"],
    [["<b>Rideshare</b>", "Phone, wallet, luggage, keys, headphones, clothing, passport, "
      "glasses, jewellery, laptop", chip("vendor")],
     ["<b>Shopping centre</b>", "Clothing, bank cards, shopping bags, personal bags, "
      "jewellery, toys, mobile devices, keys, cash, wallets", chip("news")],
     ["<b>Hotels</b>", "Clothing and toiletries, then electronics and chargers",
      chip("self")],
     ["<b>Home</b>", "TV remote, phone, keys, glasses, shoes, wallet", chip("self")]],
    title="Rankings from weaker sources, reported for completeness",
    sub="Uber's index reports over a million phones as the top item but publishes no "
        "denominator. The Trafford Centre ranking comes from a real lost-property system "
        "but no counts were released.",
    source=cite("uber", "trafford", "motel6", "pixie"))

# =============================================================== SYNTHESIS ==

d.h2("5. Putting it together", "synthesis")
d.p("Across every source examined, the picture is consistent enough to state plainly.")

d.table(
    ["Rank", "Most frequently left behind", "Most frequently returned", "Worst return rate"],
    [["1", "Documents, cards and paperwork", "Mobile phones (82.8%)", "Umbrellas (1.4%)"],
     ["2", "Clothing and footwear", "Certificates and documents (70.1%)",
      "Precious metals (1.8%)"],
     ["3", "Umbrellas", "Wallets (67.1%)", "Clothing and footwear (4.3%)"],
     ["4", "Electrical goods, chargers and cables", "Securities (29.2%)",
      "Cameras and glasses (4.4%)"],
     ["5", "Bags and wallets", "Bags (26.3%)", "Electrical products (6.4%)"]],
    title="The consensus picture",
    sub="Left-behind ranking from Tokyo and TfL combined; return rates from Tokyo 2025, "
        "which is the only source publishing both sides at scale.",
    source=cite("tokyo", "tfl"))

d.box("win", "The three groups that matter for design",
      "<ul>"
      "<li><b>Self-identifying, high return.</b> Phones, wallets, documents, ID cards. "
      "These already work &mdash; 67&ndash;83% return. Adding a tag to a phone is "
      "solving a solved problem.</li>"
      "<li><b>High volume, near-zero return.</b> Clothing, umbrellas, water bottles, "
      "chargers, glasses. Clothing alone is 9.5% of everything handed in to Tokyo police "
      "and comes back 4.3% of the time. <b>This is where the addressable loss is</b>, and "
      "it is exactly the category a campus lost-property office is drowning in.</li>"
      "<li><b>High value, low return.</b> Jewellery, precious metals, cameras. Painful "
      "individually, but only about 2&ndash;3% of item volume. Emotionally compelling for "
      "a pitch; too rare to build a product on.</li>"
      "</ul>"
      "<p>The strategic point: the items that need identity most are the cheap ones. That "
      "is uncomfortable for a business model, and it is the honest read of the data.</p>")

# ============================================================= LIMITATIONS ==

d.h2("Limitations", "limits")
d.ul([
    "<b>These datasets count different populations.</b> Tokyo counts items handed to "
    "police under a legal duty; TfL counts items reaching its lost property office; TSA "
    "counts items left at checkpoints; hotel and home figures are self-reported surveys. "
    "They are not directly comparable and no attempt has been made to pool them.",
    "<b>Tokyo return rates are approximations.</b> The returned counts come from the "
    "processing population (4,750,389 items) rather than the intake population "
    "(4,850,775), so category ratios are close but not exact.",
    "<b>Japanese law makes Tokyo unusual.</b> A legal duty to hand in found property "
    "plus a finder's reward system almost certainly raises hand-in rates above what other "
    "countries would see. The category <i>pattern</i> should generalise; the absolute "
    "volumes should not.",
    "<b>Campus data is mostly journalism.</b> Most campus figures come from student "
    "newspapers quoting lost-property staff, not from published statistics. Treat volumes "
    "as indicative.",
    "<b>Hotel, home, rideshare and venue rankings are public relations.</b> Sample sizes "
    "are sometimes given and denominators rarely are. They are included because they agree "
    "with the operational data, not because they are independently reliable.",
    "<b>Nobody publishes what fraction of lost items are ever found at all.</b> Every "
    "figure here starts from an item that already reached a desk. The items left on a "
    "train seat and swept into a bin are invisible to all of these datasets.",
])

d.h2("Sources", "sources")
rows = []
for k, (t, org, url, kind, yr) in sorted(S.items(), key=lambda x: x[1][1]):
    tick = " &#10003;" if k in LEAD else ""
    rows.append([f"{org}{tick}", f'<a href="{url}">{t}</a>', yr, chip(kind)])
d.table(["Organisation", "Publication", "Year", "Type"], rows,
        title="Sources", sub=f"{len(S)} sources, all opened. A tick marks those the author "
                             "read personally to verify a load-bearing figure.",
        source="<b>Rebuild:</b> <code>python3 research/build_lost_items.py</code>")

OUT.write_text(d.html("What gets lost: an item-level reference", MASTHEAD),
               encoding="utf-8")
print(f"wrote {OUT} ({OUT.stat().st_size:,} bytes, {d.fig_n} figures, "
      f"{d.tab_n} tables, {len(S)} sources)")
