#!/usr/bin/env python3
"""Build the universal stick-on-anything label report.

    python3 research/build_universal.py  ->  research/universal-label.html
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import data_universal as D  # noqa: E402
from charts import ACCENT, NEGATIVE, POSITIVE, Bar, hbar  # noqa: E402
from shell import REPORTS, Doc  # noqa: E402

OUT = REPORTS / "universal-label.html"
S = D.SOURCES
LEAD = D.VERIFIED_BY_LEAD


def cite(*keys: str, extra: str = "") -> str:
    bits = []
    for k in keys:
        t, org, url, kind, yr = S[k]
        tick = " &#10003;" if k in LEAD else ""
        bits.append(f'<a href="{url}">{org}, <i>{t}</i></a> ({yr}){tick}')
    s = "<b>Source:</b> " + "; ".join(bits) + "."
    return f'<p class="srcnote">{s}{" " + extra if extra else ""}</p>'


def chip(kind: str, txt: str) -> str:
    cls = {"no": "c-none", "yes": "c-strong", "part": "c-mod",
           "vendor": "c-ven", "official": "c-off", "academic": "c-aca",
           "news": "c-mod"}[kind]
    return f'<span class="chip {cls}">{txt}</span>'


d = Doc()

MASTHEAD = """
<div class="masthead">
  <div class="kicker">Prior Art &middot; Universal Property Labels</div>
  <h1>It exists, it is a dollar, and someone at your own
  university already sells it.</h1>
  <div class="standfirst">The cheap stick-on-anything label with a
  privacy-preserving scan is not an opening &mdash; it is a crowded shelf. Seven
  products with real notification back-ends were verified, the cheapest at about
  <b>&pound;0.83 a tag</b>. Students at UVA have sold over 900. A student at
  WashU reportedly gives them away. Your price advantage over PetHub is real but
  irrelevant, because PetHub is not who you are competing with.</div>
  <div class="meta">
    <div><b>Question</b>Does a cheap universal label already exist?</div>
    <div><b>Answer</b>Yes &mdash; at least 7, verified</div>
    <div><b>Evidence base</b>__NSRC__ primary sources</div>
    <div><b>Prepared</b>29 August 2026</div>
  </div>
</div>"""

# =============================================================== VERDICT ====

d.h2("Verdict", "verdict")
d.p("You asked whether a tag that sticks to anything &mdash; clothes, water "
    "bottles, chargers &mdash; already exists, and said you are far cheaper "
    "than the pet tag. Both halves need correcting. <b>It exists in quantity</b>, "
    "and <b>your cost comparison is against the wrong product</b>. PetHub costs "
    "$9.95 because it is a machined aluminium pet tag on a collar ring. The "
    "products you are actually competing with are printed vinyl stickers with an "
    "anonymous relay behind them, and they already sell for about a dollar.",
    "lede")

d.box("warn", "The two facts that should change what you say on stage",
      "<ul>"
      "<li><b>Students at the University of Virginia are already selling this.</b> "
      "Papertags, out of the McIntire School, is a 2&Prime;&nbsp;&times;&nbsp;2&Prime; "
      "NFC-enabled sticker, customisable with a logo, at <b>$2.50 each with more "
      "than 900 sold</b>. Same idea, same customer, already shipping.</li>"
      "<li><b>A student at your own university reportedly did it too.</b> Beacon "
      "Tags at WashU was reported as handing out free QR labels to recover "
      "misplaced campus items. The article returned HTTP 403 so <b>this is "
      "unconfirmed</b> &mdash; but find out before a judge does, because if it is "
      "true it will be the first question you get.</li>"
      "</ul>"
      + cite("papertags"))

d.box("insight", "What survives all of this",
      "<p>Nothing above touches the finding from the earlier report, and it is "
      "still the only defensible one: <b>every product here sells to an "
      "individual. None is wired into an institution.</b> Papertags sells you a "
      "sticker. It does not know that your university runs a lost-property desk, "
      "holds your contact details, and throws away water bottles after three "
      "days.</p>")

# ========================================================== BACKEND MARKET ==

d.h2("1. Seven products already do exactly this", "backend")
d.p("These are passive stickers with a real service behind the scan &mdash; the "
    "finder scans, the owner is notified, and in most cases the owner's identity "
    "is masked. All verified from the vendor's own product page.")

d.table(
    ["Product", "Pack", "Per tag", "Surfaces claimed", "Notes"],
    [[f"<b>{n}</b>", p, f"<b>{u}</b>", s, x] for n, p, u, s, x in D.BACKEND_TAGS],
    title="Universal QR stickers with a notification back-end",
    sub="Cheapest verified is Letstrack at about 83p. Note the surfaces column: "
        "only Letstrack claims fabric and hard surfaces in one product.",
    source=cite("letstrack", "boomerang_stick", "roam", "seqr",
                "pebblebee_link", "iffound"))

d.fig(hbar([Bar("PetHub (pet tag)", 9.95, color=NEGATIVE),
            Bar("If Found", 3.75, color=NEGATIVE),
            Bar("Papertags (UVA students)", 2.50, color=ACCENT),
            Bar("Pebblebee Link", 1.80, color=ACCENT),
            Bar("SeQR", 1.67, color=ACCENT),
            Bar("Roam", 1.25, color=ACCENT),
            Bar("Boomerang Stick On", 1.04, color=POSITIVE),
            Bar("Letstrack", 1.05, color=POSITIVE)],
           unit="", dp=2, label_w=230, width=580, row_h=28),
      "Per-tag price, products with a real notification back-end",
      "US dollars, converting Letstrack and If Found at roughly 1.26. The market "
      "floor is about a dollar \u2014 not ten.",
      source=cite("pethub_price" if "pethub_price" in S else "iffound"))

d.box("caveat", "Where your cost claim actually lands",
      "<p>Against PetHub at $9.95 you are roughly <b>ten times cheaper</b>, and "
      "that sounds impressive until someone names Letstrack or Boomerang. "
      "Against the real market you are competing at <b>parity</b>, and parity on "
      "price is not a pitch.</p>"
      "<p>The raw materials say the floor could go lower: a plain paper Avery "
      f"label is <b>${D.AVERY['unit']:.3f}</b> each in a 300 pack, a printed "
      "NTAG213 sticker is <b>$0.58</b> at a thousand, and a dumb laminated-vinyl "
      "QR asset label is <b>$0.79</b> at a thousand. But every one of those is "
      "just the sticker &mdash; no service, no relay, no notification. The "
      "dollar you see in the market is the <i>service</i>, not the substrate."
      "</p>"
      + cite("avery22806", "gototags_price", "strongtags"))

# ======================================================== CLOTHING LABELS ===

d.h2("2. The clothing-label industry you did not know you were entering",
     "clothing")
d.p("There is a large, mature, cheap market for sticking identity onto clothes. "
    "It sells to parents of school children, and to care homes. It has been "
    "solving your fabric problem for decades &mdash; badly, but cheaply.")

d.table(
    ["Vendor", "Pack", "Price", "Per label", "Durability claim", "Carries"],
    [[f"<b>{v}</b>", p, pr, f"<b>{u:.2f}</b> {c[:3]}", dur, car]
     for v, p, pr, u, c, dur, car in D.PRINTED_LABELS],
    title="Mainstream printed clothing labels",
    sub="Every one of these prints a name, and several actively recommend "
        "printing a phone number. That is the exact opposite of a privacy "
        "relay \u2014 and it is the incumbent behaviour you have to displace.",
    source=cite("nameit", "stikins", "stikins_order", "mabels", "mynametags",
                "easy2name", "namebubbles"))

d.box("warn", "Stikins is the uncomfortable one",
      "<p>Read its specification and it is close to the physical product you "
      "described: a <b>multipurpose stick-on label for clothes, shoes and hard "
      "goods</b>, independently tested to <b>BS EN ISO6330 for 60 washes at "
      "40&nbsp;&deg;C</b>, surviving washer, tumble dryer and dishwasher. "
      "<b>15p a label.</b></p>"
      "<p>Mabel's Tag Mates makes the same move from the other side &mdash; a "
      "stick-on clothing label the vendor also markets as dishwasher-safe on "
      "bottles, phones, chargers and school supplies, at 23&cent;.</p>"
      "<p>So the durable multi-surface sticker at your price point <b>is already "
      "a shipping product</b>. It just prints a name instead of resolving a "
      "code. That is a software gap, not a materials gap &mdash; which is good "
      "news for a hackathon, and bad news for a patent.</p>"
      + cite("stikins", "mabels"))

d.table(
    ["Product", "Price", "MOQ", "Technology", "Wash rating"],
    [[f"<b>{n}</b>", p, m, t, w] for n, p, m, t, w in D.FABRIC_TAGS],
    title="Machine-readable fabric tags that already exist",
    sub="These prove the technology is solved. Both are business-to-business "
        "channels rather than consumer products.",
    source=cite("scivas", "datamars", "rfidsu", "avdenn"))

d.box("insight", "The laundry-grade numbers are better than you would guess",
      "<p>Avery Dennison's sew-in UHF fabric label is designed for <b>50 home "
      "wash and dry cycles</b> and passed <b>100% over 50 cycles</b> at "
      "40&nbsp;&deg;C with detergent and oxygen bleach. RFIDSU's 15&nbsp;mm NFC "
      "button survives <b>about 200 industrial wash cycles</b> and "
      "&minus;30&nbsp;to&nbsp;+200&nbsp;&deg;C. SCIVAS will sell you a woven "
      "NFC-plus-QR clothing label from <b>$0.11 at a minimum of 100</b>.</p>"
      "<p><b>Fabric is not your hard problem.</b> It is a solved, purchasable "
      "component.</p>"
      + cite("avdenn", "rfidsu", "scivas"))

# ============================================================ THE BOTTLE ====

d.h2("3. The water bottle: strong problem, one real competitor", "bottle")

d.box("caveat", "First, soften the claim before someone tests it",
      "<p>&ldquo;The most-lost item on campus is the water bottle&rdquo; is "
      "<b>credible but not universally evidenced</b>. Whitman's caretaker gives "
      "the clearest count &mdash; <i>a couple hundred water bottles</i> every "
      "year, the most consistent item. But Texas A&amp;M, which logs over "
      f"<b>{D.TAMU['annual']:,} items a year</b> at "
      f"<b>{D.TAMU['daily']} a day</b>, says &ldquo;so many water "
      "bottles&rdquo; while naming <b>earbuds and headphones</b> as the most "
      "common. Say <i>one of the most-lost</i> and you cannot be contradicted."
      "</p>"
      + cite("whitman", "tamu"))

d.p("The disposal evidence, by contrast, is overwhelming and is the better "
    "argument anyway. Five institutions, in their own published words:")

d.table(
    ["Institution", "Policy", "Exact provision"],
    [[f"<b>{i}</b>", f"<b>{p}</b>", e] for i, p, e in D.BOTTLE_POLICY],
    title="What universities do with drink containers",
    sub="This is the sharpest statement of the problem available: the item is "
        "so hard to reunite that the rational institutional response is to "
        "refuse it at the door.",
    source=cite("vtech", "boise", "liberty", "uga", "uwhub"))

d.box("win", "Reframe the pitch around this, not around frequency",
      "<p>Boise State's policy table gives the disposition of a water bottle as "
      "<b>&ldquo;Will Not Accept &mdash; Immediate Disposal&rdquo;</b>. Virginia "
      "Tech lists drink containers under items it does not accept at all.</p>"
      "<p>That is not a storage problem, it is an <b>identification</b> problem. "
      "Nobody bins a labelled item. A two-cent label converts a bottle from "
      "refuse-on-arrival into a two-second lookup &mdash; and Texas A&amp;M "
      f"already reunites <b>{D.TAMU['reunited']}/{D.TAMU['total']}</b> of what "
      f"it does accept, about "
      f"<b>{100*D.TAMU['reunited']/D.TAMU['total']:.0f}%</b>, when it has "
      "something to work with.</p>"
      + cite("boise", "vtech", "tamu"))

d.table(
    ["Brand", "Personalisation offered", "Recovery scheme?", "Price anchor"],
    [[f"<b>{b}</b>", p, r, a] for b, p, r, a in D.DRINKWARE],
    title="Do the drinkware brands already do this?",
    sub="One does. It is not an American one.",
    source=cite("citron", "nalgene_custom", "nalgene_faq", "yeti", "camelbak"))

d.box("warn", "Citron is your closest direct competitor and you should cite it",
      "<p>Citron, a UAE drinkware brand, moulds a <b>QR code into the bottom of "
      "the bottle</b>. The owner registers at findmycitron.com; a finder scans; "
      "the owner is notified; <b>contact details are exchanged only if both "
      "sides agree</b>. That is your privacy model, already shipping, on the "
      "exact object you named.</p>"
      "<p>Two things limit it, and both are your opening: it covers only "
      "<b>Citron's own 250 ml and 350 ml bottles</b>, and it is a brand feature "
      "rather than a label you can apply to the bottle you already own. Nalgene, "
      "YETI and CamelBak offer engraving and custom printing but <b>no recovery "
      "scheme at all</b> &mdash; Nalgene's guarantee explicitly excludes loss."
      "</p>"
      + cite("citron", "nalgene_faq", "yeti"))

# ========================================================== ENGINEERING =====

d.h2("4. One tag will not cover every surface. Plan for three.", "surfaces")
d.p("This is the part that will bite a one-day build, and it is physics rather "
    "than product design.")

d.table(
    ["Adhesive", "Bonds to", "Cure to full strength", "Water"],
    [[f"<b>{n}</b>", s, c, w] for n, s, c, w in D.ADHESIVES],
    title="3M adhesive figures",
    sub="Read the middle column twice. A sticker applied on the morning of a "
        "demo is nowhere near full strength that evening. Caveat: 3M's PDFs "
        "would not fetch, so these values come from search-indexed copies of "
        "3M's own datasheets \u2014 consistent across three products, but not "
        "read in the primary document. Treat the 72-hour figure as a strong "
        "planning assumption rather than a citation.",
    source=cite("mmm300", "mmm468"))

d.table(
    ["Fabric tag", "Home wash cycles", "Basis"],
    [[f"<b>{n}</b>", f"<b>{c}</b>", b] for n, c, b in D.FABRIC_WASH],
    title="Avery Dennison publishes two very different fabric grades",
    sub="Same 60 \u00d7 31.75 mm sew-in format, a five-fold difference in wash "
        "life. If you quote a wash number, quote which product it belongs to.",
    source=cite("avdenn"))

d.box("warn", "Three constraints",
      "<ul>"
      "<li><b>72 hours to full bond.</b> 300LSE, 468MP and 9471LE all build "
      "strength over three days. Apply your demo labels <b>now</b>, not "
      "tomorrow.</li>"
      "<li><b>Metal kills plain NFC.</b> A stainless bottle needs an on-metal "
      f"tag with a ferrite layer: Seritag's 29 mm on-metal NTAG213 is "
      f"<b>{D.ONMETAL_SPEC['thickness_mm']} mm</b> overall, reads at only "
      f"<b>{D.ONMETAL_SPEC['read_mm']} mm</b>, and costs "
      f"<b>${D.ONMETAL[0][1]:.2f}</b> in single units, falling to "
      f"<b>${D.ONMETAL[-1][1]:.2f}</b> at a thousand.</li>"
      "<li><b>Nobody publishes a dishwasher test.</b> 3M publishes water "
      "immersion and humidity data, not dishwasher cycles. Several tag vendors "
      "claim dishwasher safety; that is marketing. <b>Do not repeat it as a "
      "specification.</b></li>"
      "</ul>"
      + cite("seritag", "mmm300"))

d.box("insight", "So what do you actually build",
      "<p>Accept three formats rather than pretending one label does everything. "
      "<b>Hard smooth surfaces</b> &mdash; laptop, plastic bottle, charger, "
      "notebook &mdash; take a laminated vinyl QR at well under a dollar. "
      "<b>Fabric</b> takes a woven or iron-on tag, and you can buy an NFC-plus-QR "
      "one from $0.11. <b>Stainless steel</b> needs an on-metal NFC tag at about "
      "$0.81, or simply a printed QR, which does not care what it is stuck to."
      "</p>"
      "<p><b>The QR does not have the metal problem at all.</b> For a weekend "
      "build that is a decisive advantage over NFC, and it is worth saying out "
      "loud rather than treating QR as the fallback.</p>"
      + cite("seritag", "scivas", "strongtags"))

# ============================================================== POSITION ====

d.h2("5. Where this leaves the pitch", "position")

d.table(
    ["Claim", "Status after this research"],
    [["&ldquo;A cheap sticker you can put on anything&rdquo;",
      chip("no", "Exists") + " Seven verified products, from about $1"],
     ["&ldquo;The finder stays anonymous&rdquo;",
      chip("no", "Exists") + " Letstrack masks calls; Citron requires mutual consent"],
     ["&ldquo;Far cheaper than existing tags&rdquo;",
      chip("part", "Only versus PetHub") + " Market floor is already ~$1"],
     ["&ldquo;Works on clothing&rdquo;",
      chip("part", "Partly open") + " Only Letstrack claims fabric plus hard "
      "surfaces in one product"],
     ["&ldquo;Solves the campus water bottle&rdquo;",
      chip("part", "Strong problem") + " Citron does it for its own bottles only"],
     ["<b>&ldquo;The university's own identity system resolves the tag&rdquo;</b>",
      chip("yes", "Open") + " <b>No product found does this</b>"],
     ["<b>&ldquo;Campus chokepoints are the scanner network&rdquo;</b>",
      chip("yes", "Open") + " <b>No product found does this</b>"],
     ["<b>&ldquo;Feeds the lost-property desk that already exists&rdquo;</b>",
      chip("yes", "Open") + " <b>No product found does this</b>"]],
    title="Claim by claim",
    sub="The three in bold are unchanged from the previous report. Everything "
        "else has been taken.")

d.box("win", "The honest, and much stronger, framing",
      "<p>Stop leading with the tag. Lead with the institution.</p>"
      "<p>&ldquo;Anyone can sell a student a QR sticker &mdash; students at UVA "
      "already have, nine hundred of them. The sticker is not the product. "
      "<b>The product is that Virginia Tech refuses to accept a water bottle, "
      "and Boise State bins it on arrival, while both universities hold the "
      "contact details of the person who dropped it.</b> We close that gap. The "
      "label is just the cheapest way to carry the identifier.&rdquo;</p>"
      "<p>That version cannot be beaten by naming a competitor, because none of "
      "them is trying to do it.</p>"
      + cite("papertags", "vtech", "boise"))

# =========================================================== LIMITATIONS ====

d.h2("Limitations", "limits")
d.ul([
    "<b>Almost everything here is vendor marketing.</b> No independent test of "
    "any consumer tag's durability or recovery rate was found. Wash-cycle and "
    "adhesion numbers from 3M, Avery Dennison and Stikins are the exceptions, "
    "being tied to named standards.",
    "<b>The Beacon Tags WashU claim is unconfirmed.</b> The article returned "
    "HTTP 403. Treat it as a lead to check locally, not a fact.",
    "<b>Prices mix currencies.</b> GBP figures are transcribed as published; "
    "dollar conversions in the chart are approximate.",
    "<b>Per-unit prices assume the pack size the vendor sells.</b> Several "
    "generic asset-label prices require 500 or 1,000 units.",
    "<b>Sources that could not be opened</b>, and from which nothing is "
    "asserted: " + "; ".join(D.UNREACHABLE) + ".",
])

# =============================================================== SOURCES ====

d.h2("Sources", "sources")
rows = []
for k, (t, org, url, kind, yr) in sorted(S.items(), key=lambda x: x[1][1]):
    tick = " &#10003;" if k in LEAD else ""
    rows.append([f"<b>{org}</b>{tick}", f'<a href="{url}">{t}</a>',
                 chip(kind if kind in ("vendor", "official", "news")
                      else "academic",
                      "vendor/PR" if kind == "vendor" else kind), yr])
d.table(["Organisation", "Document", "Grade", "Year"], rows,
        title=f"{len(S)} primary sources",
        sub="&#10003; marks sources the lead agent opened personally.")

d.h2("Reverting this document", "revert")
d.p("Delete <code>research/universal-label.html</code>, "
    "<code>research/build_universal.py</code> and "
    "<code>research/data_universal.py</code>. Nothing outside those three files "
    "was touched.")

# ================================================================= WRITE ====

_mast = MASTHEAD.replace("__NSRC__", str(len(S)))
OUT.write_text(d.html("Does the universal property label already exist?", _mast),
               encoding="utf-8")
print(f"wrote {OUT} ({OUT.stat().st_size:,} bytes, {d.fig_n} figures, "
      f"{d.tab_n} tables, {len(S)} sources)")
