#!/usr/bin/env python3
"""Build the loss-pivot verification report.

    python3 research/build_loss_pivot.py

Writes research/loss-and-reunification.html. Self-contained, no assets.
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import charts as C  # noqa: E402
from charts import Bar  # noqa: E402
from shell import REPORTS, Doc  # noqa: E402

OUT = REPORTS / "loss-and-reunification.html"

S = {
    "cohn": ("Civic honesty around the globe (Science 365:70-73)",
             "Cohn, Marechal, Tannenbaum & Zund",
             "https://static.poder360.com.br/2019/06/science.aau8712.full-1.pdf",
             "academic", "2019"),
    "letters": ("Lost-letter technique meta-analysis (Journal of Economic Psychology 105)",
                "Asanov, Schirmacher & Buhren",
                "https://doi.org/10.1016/j.joep.2024.102759", "academic", "2024"),
    "perth": ("Are stamped letters returned? A lost-letter experiment (PeerJ)",
              "Grueter et al.", "https://pmc.ncbi.nlm.nih.gov/articles/PMC5088574/",
              "academic", "2016"),
    "london": ("Lost letter measure of social capital (PLOS ONE)",
               "Holland, Silva & Mace",
               "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0043294",
               "academic", "2012"),
    "usb": ("Users Really Do Plug in USB Drives They Find (IEEE S&P)",
            "Tischer et al.",
            "https://faculty.cc.gatech.edu/~mbailey/publications/oakland16_usb.pdf",
            "academic", "2016"),
    "china": ("Nudging civic honesty: a QR-mediated lost-wallet field experiment "
              "(Scientific Reports 15)", "Han et al.",
              "https://www.nature.com/articles/s41598-025-87804-z", "academic", "2025"),
    "lord": ("Characterization of animals with microchips entering animal shelters "
             "(JAVMA 235:160)", "Lord, Ingwersen, Gray & Wintz",
             "https://avmajournals.avma.org/view/journals/javma/235/2/javma.235.2.160.xml",
             "academic", "2009"),
    "rajala": ("Reunifying lost pets with their owners (JAVMA 230:1835)",
               "Rajala-Schultz et al.",
               "https://avmajournals.avma.org/view/journals/javma/230/12/javma.230.12.1835.xml",
               "academic", "2007"),
    "aspca": ("Search methods used to locate missing cats and dogs (Animals)",
              "Weiss, Slater & Lord",
              "https://pmc.ncbi.nlm.nih.gov/articles/PMC4494319/", "academic", "2012"),
    "tfl": ("Lost Property Office transparency data FY2017-18-19",
            "Transport for London",
            "https://foi.tfl.gov.uk/FOI-1592-2223/lost-property-office-transparency-data-"
            "FY2017-18-19.pdf", "official", "2018/19"),
    "tsa": ("Lost and found", "US Transportation Security Administration",
            "https://www.tsa.gov/contact/lost-and-found", "official", "2026"),
    "uw": ("HUB Lost and Found policy A-12", "University of Washington",
           "https://hub.washington.edu/wordpress/wp-content/uploads/2025/10/"
           "A-12-HUB-Lost-and-Found-Policy.pdf", "official", "2025"),
    "standrews": ("Lost and found property standard operating procedure",
                  "University of St Andrews",
                  "https://www.st-andrews.ac.uk/policy/estate-facilities-management-"
                  "security/lost-and-found-property.pdf", "official", "2026"),
    "fresno": ("Property and Equipment Procedures Manual", "Fresno State",
               "https://adminfinance.fresnostate.edu/procurement/documents/"
               "property-manual-revised-08-24.pdf", "official", "2024"),
    "uber": ("Contact your driver about a lost item", "Uber",
             "https://help.uber.com/en/riders/article/contact-driver-about-a-lost-item"
             "?nodeId=842c1dd3-62c2-4513-bbeb-a9044c0faab1", "vendor", "2026"),
    "iata": ("Baggage tracking implementation guide (Resolution 753)",
             "International Air Transport Association",
             "https://www.iata.org/contentassets/5316edd3aafb4866876e37883211cfc4/"
             "baggage_tracking_implementation_guide.pdf", "official", "2024"),
    "flash": ("Smartphone flash spectral characterisation (Biosensors 12:1060)",
              "Vu et al.",
              "https://www.mdpi.com/2079-6374/12/12/1060", "academic", "2022"),
    "qrfield": ("Naturalistic observation of public QR code scanning (iJIM 20:14)",
                "Ball, Warmelink, Nightingale & Crawford",
                "https://online-journals.org/index.php/i-jim/article/view/61501",
                "academic", "2026"),
    "qrtextile": ("Durability of QR codes applied to polyester textiles (MSc thesis)",
                  "Hasan, Kaunas University of Technology",
                  "https://epubl.ktu.edu/object/elaba:269083756/269083756.pdf",
                  "academic", "2026"),
    "screenprint": ("Secured tag printing on textile substrates "
                    "(Int J Adv Manuf Technol 102)", "Koehl, Agrawal & Campagne",
                    "https://doi.org/10.1007/s00170-018-3134-z", "academic", "2019"),
    "wa": ("Travel tips: luggage tags", "Washington State Attorney General",
           "https://www.atg.wa.gov/travel-tips", "official", "2026"),
    "apple": ("Mark a device as lost with Find My", "Apple",
              "https://support.apple.com/en-us/104978", "official", "2026"),
    "aspcapro": ("Retention of pet ID tags and outcomes for lost pets", "ASPCApro",
                 "https://www.aspcapro.org/resource/retention-pet-id-tags-and-outcomes-"
                 "lost-pets", "official", "2026"),
    'iso14443': ('ISO/IEC 14443-2:2016 — Radio frequency power and signal interface', 'ISO/IEC', 'https://cdn.standards.iteh.ai/samples/66288/402d789d691e47309c6db0c954609355/ISO-IEC-14443-2-2016.pdf', 'official', '2016'),
    'an11564': ('AN11564 — NFC antenna design guide', 'NXP Semiconductors', 'https://www.nxp.com/docs/en/application-note/AN11564.pdf', 'official', '2016'),
    'ntag': ('NTAG213/215/216 product data sheet', 'NXP Semiconductors', 'https://www.nxp.com/docs/en/data-sheet/NTAG213_215_216.pdf', 'official', '2015'),
    'identiv': ('ID-Tiny A613 ST25TV data sheet', 'Identiv', 'https://identiv.com/wp-content/uploads/2026/07/ID-Tiny-A613-ST25TV_Datasheet_06_26.pdf', 'vendor', '2026'),
    'avery_circus': ('AD Circus NFC NTAG213 data sheet', 'Avery Dennison', 'https://rfid.averydennison.com/content/dam/rfid/en/products/rfid-products/data-sheets/datasheet-Circus-NFC-NTAG213.pdf', 'vendor', '2026'),
    'avery_dura': ('AD Circus NTAG213 Dura 2.0 data sheet', 'Avery Dennison', 'https://rfid.averydennison.com/content/dam/rfid/en/products/rfid-products/data-sheets/datasheet-AD-Circus-NTAG213-Dura-2-0.pdf', 'vendor', '2026'),
    'avery_bullseye': ('AD Bullseye On-Metal data sheet', 'Avery Dennison', 'https://rfid.averydennison.com/content/dam/rfid/en/products/rfid-products/data-sheets/datasheet-Bullseye-On-Metal.pdf', 'vendor', '2026'),
    'bopla': ('Transparent RFID antennas whitepaper', 'Bopla / inotec', 'https://www.bopla.de/fileadmin/user_upload/RFID_Whitepaper.pdf', 'vendor', '2024'),
    'arxivnfc': ('Characterising smartphone NFC read range across commercial tags', 'Rahman et al.', 'https://export.arxiv.org/pdf/2210.12327v1.pdf', 'academic', '2022'),
    'armata': ('Extra small 6 mm NFC FPC inlay NTAG213', 'Armata', 'https://www.armata.fi/en/rfid-tags/655-adhesive-extra-small-6mm-nfc-fpc-inlay-tag-ntag213.html', 'vendor', '2026'),
    'gototags': ('Clear wet NFC inlay NTAG213 20 x 10 mm', 'GoToTags', 'https://store.gototags.com/clear-wet-nfc-inlay-ntag213-20-x-10-mm-rectangle/', 'vendor', '2026'),
    'apple_nfc': ('Adding support for background tag reading (Core NFC)', 'Apple', 'https://developer.apple.com/documentation/corenfc/adding-support-for-background-tag-reading', 'official', '2026'),
    'android_nfc': ('NFC basics', 'Android Developers', 'https://developer.android.com/develop/connectivity/nfc/nfc', 'official', '2026'),
}
LEAD = {"cohn", "tfl", "flash", "iso14443", "apple_nfc"}


def cite(*keys: str, extra: str = "") -> str:
    bits = []
    for k in keys:
        t, org, url, kind, yr = S[k]
        tick = " &#10003;" if k in LEAD else ""
        bits.append(f'<a href="{url}">{org}, <i>{t}</i></a> ({yr}){tick}')
    s = "<b>Source:</b> " + "; ".join(bits) + "."
    return f"{s} {extra}" if extra else s


def chip(k: str) -> str:
    m = {"sup": ("c-strong", "Supported"), "part": ("c-mod", "Partly supported"),
         "analog": ("c-mod", "Supported by analogy"), "no": ("c-weak", "Not established"),
         "official": ("c-off", "Official"), "academic": ("c-aca", "Peer-reviewed"),
         "vendor": ("c-ven", "Vendor claim"), "keep": ("c-strong", "Keep"),
         "drop": ("c-none", "Drop"), "invert": ("c-weak", "Inverts")}
    cls, txt = m[k]
    return f'<span class="chip {cls}">{txt}</span>'


d = Doc()

MASTHEAD = """
<div class="masthead">
  <div class="kicker">Verification &middot; Loss &amp; Reunification</div>
  <h1>Your premise holds. Your ink does not survive the pivot.</h1>
  <div class="standfirst">Testing the claim that lost items are frequently found, that
  finders frequently try to return them, and that the attempt fails because the owner
  cannot be identified &mdash; then re-examining a covert marking ink for a world with
  no adversary in it.</div>
  <div class="meta">
    <div><b>Claim</b>Found &rarr; attempted &rarr; blocked on identity</div>
    <div><b>Links (a) and (b)</b>Supported</div>
    <div><b>Link (c)</b>Supported by analogy, not proven</div>
    <div><b>Prepared</b>28 August 2026</div>
  </div>
</div>"""

# ================================================================= VERDICT ==

d.h2("Verdict", "verdict")
d.p("The pivot is well judged. Loss is a bigger and more tractable problem than theft, "
    "and your causal story is broadly right &mdash; with one important correction and one "
    "gap you should know about before pitching it.", "lede")

d.table(
    ["Your claim", "Verdict", "Best evidence"],
    [["<b>(a)</b> Lost items get found by other people, a lot", chip("sup"),
      "290 of 297 dropped USB drives were picked up within days. TSA alone reports "
      "90,000&ndash;100,000 items left at checkpoints <i>per month</i>. TfL received "
      "333,921 items in a year; one US campus union building processes over 1,000 items "
      "a month."],
     ["<b>(b)</b> Finders frequently try to return them", chip("sup"),
      "Across 78 lost-letter studies and 53,504 letters, mean return was 50%. Cohn's "
      "17,303-wallet experiment got 40&ndash;72% of finders to email a stranger. 87% of "
      "people who found a pet said finding the owner was extremely important."],
     ["<b>(c)</b> The attempt fails because the owner cannot be identified", chip("analog"),
      "No experiment has cleanly compared identifiable versus unidentifiable objects. But "
      "the lost-pet literature is a large natural experiment: microchipped stray cats are "
      "returned at a median 38.5% versus 1.8% for strays generally."]],
    title="The claim, link by link",
    sub="Two links are solidly evidenced. The third is strongly suggested by the closest "
        "available analogue but has never been tested directly on objects.",
    source=cite("usb", "tsa", "tfl", "letters", "cohn", "rajala", "lord"))

d.box("warn", "The correction: identifiable is not the same as contactable",
      "<p>Your model has one step where the evidence says there are two. When shelters "
      "scanned a microchipped stray and still failed to reach the owner, the reasons were "
      "measured: <b>35.4% incorrect or disconnected phone number</b>, <b>24.3% owner did "
      "not respond</b>, <b>17.2% registered to a different organisation</b>.</p>"
      "<p>So the chain is <b>found &rarr; willing &rarr; identifiable &rarr; contact route "
      "still live &rarr; owner responds</b>. A permanent mark fixes link three and does "
      "nothing for links four and five. An ink that resolves to a phone number a student "
      "changed two years ago is a mark that works and a return that fails.</p>"
      + cite("lord"))

d.box("insight", "And the honest gap you should say out loud",
      "<p>Every major finder experiment supplies the finder with contact details. Cohn "
      "created <b>a unique email address for every one of the 17,303 wallets</b>. The USB "
      "study used labelled drives and resumes. The 2025 Chinese wallet study put a visible "
      "QR sticker on all 660 wallets.</p>"
      "<p>These establish the <i>ceiling</i>: when a finder can contact the owner, "
      "40&ndash;72% do. <b>None of them measures what happens when they cannot</b>, because "
      "no experiment has run that arm. If you claim a specific recovery uplift, you are "
      "extrapolating. Say so, and cite the pet data as your analogue.</p>"
      + cite("cohn", "usb", "china"))

# =============================================================== LINK (A/B) ==

d.h2("1. Links (a) and (b): finders exist, and they try", "finders")
d.p("The volume side is not in doubt, and neither is willingness. What is striking is how "
    "consistently willingness lands in the same band across wildly different methods, "
    "countries and decades.")

d.fig(
    C.hbar([
        Bar("Pet finders saying finding the owner was 'extremely important'", 87,
            color=C.PALETTE[0]),
        Bar("Cohn wallets with a large sum \u2014 finder emailed owner", 72,
            color=C.POSITIVE),
        Bar("USB finders who said they intended to return the drive", 68,
            color=C.PALETTE[0]),
        Bar("China wallet study \u2014 finder scanned the QR contact code", 66.3,
            color=C.POSITIVE),
        Bar("China wallet study \u2014 finder phoned the owner", 59.3, color=C.POSITIVE),
        Bar("Perth lost letters (stamped) returned", 61.3, color=C.ACCENT),
        Bar("Cohn wallets with money \u2014 finder emailed owner", 51, color=C.POSITIVE),
        Bar("Lost-letter meta-analysis, 78 studies", 50, color=C.ACCENT),
        Bar("Cohn wallets with no money \u2014 finder emailed owner", 40,
            color=C.POSITIVE),
        Bar("Perth lost letters (unstamped) returned", 30.7, color=C.ACCENT),
    ], unit="%", dp=1, label_w=330),
    "When a finder can act, a lot of them do",
    "Every figure here is from a situation where the finder had a route to the owner. "
    "Green is wallet field experiments, orange is lost-letter studies, blue is stated "
    "intent. The consistency across methods is the point.",
    cite("cohn", "letters", "perth", "usb", "china", "rajala",
         extra="Bases: Cohn 17,303 wallets in 40 countries; meta-analysis 53,504 letters "
               "across 78 studies; Perth 300 letters; China 660 wallets; USB 62 survey "
               "respondents of 135 who opened a drive (self-selected); pet finders 156 "
               "completed surveys."))

d.p("The volumes are equally clear. Of <b>297 USB drives</b> dropped around a university "
    "campus, <b>290 were picked up</b>. Institutions are drowning in found property: TSA "
    "handles 90,000&ndash;100,000 items left at checkpoints every month; the University of "
    "Washington's student union processes over 1,000 items a month; Transport for London "
    "received 333,921 items in 2018/19.")
d.raw(f'<p class="srcnote">{cite("usb", "tsa", "uw", "tfl")}</p>')

d.box("caveat", "Two honest deductions from the same data",
      "<p>Willingness is not the same as follow-through. In the USB study <b>68% said they "
      "intended to return the drive</b>, but only <b>54 of 297 drives (18%)</b> were "
      "physically handed back. And in the Perth letter experiment, adding a small cost to "
      "the finder &mdash; making them buy a stamp &mdash; cut returns from <b>61.3% to "
      "30.7%</b>.</p>"
      "<p>Friction halves it. Whatever you build has to be a single, obvious, free action.</p>"
      + cite("usb", "perth"))

# ================================================================ LINK (C) ==

d.h2("2. Link (c): does identity actually drive reunification?", "identity")
d.p("No object experiment has tested this. The closest large-sample real-world test is "
    "animals, and it is a good analogue: a creature that cannot say who owns it, made "
    "identifiable by a cheap implanted tag, in a system that routinely scans.")

d.fig(
    C.pairbar([("Stray dogs", 21.9, 52.2), ("Stray cats", 1.8, 38.5)],
              ("All strays", "Microchipped strays"), label_w=170,
              colors=(C.NEGATIVE, C.POSITIVE), vmax=60, row_h=26),
    "Return-to-owner rates, with and without an identifier",
    "Shelter-level median return-to-owner rates across 53 animal shelters in 23 US states, "
    "August 2007 to March 2008. For cats the difference is more than twentyfold.",
    cite("lord", extra="<b>Important:</b> these are shelter-level medians comparing the "
                       "microchipped subset against all strays, not a randomised "
                       "individual-level comparison. Owners who microchip are plausibly "
                       "also more likely to search, so part of this gap is selection, not "
                       "causation. Treat the direction as solid and the magnitude as an "
                       "upper bound."))

d.p("The same study measured how often the owner was found at all, broken down by whether "
    "usable registration existed. This is the cleanest available statement of your "
    "hypothesis:")

d.fig(
    C.hbar([
        Bar("Owner details already in the shelter's own database", 86.2, color=C.POSITIVE),
        Bar("Registered in a microchip registry", 77.0, color=C.POSITIVE),
        Bar("Chip present but not registered anywhere", 41.6, color=C.NEGATIVE),
    ], unit="%", dp=1, label_w=300, vmax=100),
    "Owner found, by quality of the identity record",
    "Percentage of microchipped stray animals whose owner was located. Bases: 1,498, 1,121 "
    "and 806 animals respectively. A chip with no live registration behind it recovers "
    "barely half as well as one with a maintained record.",
    cite("lord"))

d.fig(
    C.hbar([
        Bar("Phone number incorrect or disconnected", 35.4, color=C.NEGATIVE),
        Bar("Owner did not respond", 24.3, color=C.ACCENT),
        Bar("Registered to a different organisation", 17.2, color=C.ACCENT),
    ], unit="%", dp=1, label_w=280, vmax=45),
    "When identification succeeded but reunification still failed",
    "Reasons the owner was not found, among 876 microchipped animals whose owners could "
    "not be reached. <b>This is the chart that should shape your product.</b> The mark "
    "worked. The contact route was dead.",
    cite("lord"))

d.box("warn", "A finding that cuts against the simple version of your story",
      "<p>A survey of 156 people who found a pet reported that only <b>10% of "
      "reunifications were attributed to information on the animal's tag</b>. A national "
      "US owner survey found <b>93% of lost dogs and 75% of lost cats were recovered</b>, "
      "but only <b>15% of dog recoveries and 2% of cat recoveries</b> happened because "
      "someone was contacted via tag or microchip.</p>"
      "<p>Most reunifications happen by the owner searching, not the finder calling. That "
      "does not refute your premise, but it reframes the size of the prize: identity "
      "marking is not the main channel today. Your bet is that it <i>could</i> be, and "
      "that is a defensible bet &mdash; the pet data shows the marked-and-registered "
      "subgroup does far better. Just do not claim it is how recovery normally works.</p>"
      + cite("rajala", "aspca"))

d.h3("The same pattern, in your own earlier data")
d.fig(
    C.hbar([Bar("Telephones", 48.3, color=C.POSITIVE), Bar("Valuables", 43.5, color=C.POSITIVE),
            Bar("Bags", 41.9, color=C.POSITIVE), Bar("Books, documents & cards", 14.9,
                                                     color=C.ACCENT),
            Bar("Miscellaneous", 13.2, color=C.ACCENT), Bar("Keys", 11.3, color=C.ACCENT),
            Bar("Clothing", 9.6, color=C.NEGATIVE), Bar("Eyewear", 7.5, color=C.NEGATIVE),
            Bar("Jewellery", 3.4, color=C.NEGATIVE), Bar("Umbrellas", 2.3, color=C.NEGATIVE)],
           unit="%", dp=1, label_w=230),
    "Reclaim rate by item category, Transport for London",
    "Percentage of found items reclaimed by their owner, 2018/19, from 333,921 items. "
    "Items that announce their owner (a phone that rings and has a lock screen) recover at "
    "twenty times the rate of items that do not (an umbrella).",
    cite("tfl", extra="Note the mechanism here is <i>owner-initiated</i> search, not "
                      "finder-initiated contact. It shows identifiability correlates with "
                      "recovery; it does not isolate the finder's behaviour."))

# ============================================================== OPERATIONS ==

d.h2("3. How lost-and-found actually works, and why that matters", "ops")
d.p("A crucial operational finding: almost every published lost-property workflow is "
    "<b>owner-initiated</b>. The owner searches; the institution matches. Nobody goes "
    "looking for the owner.")

d.table(
    ["Operator", "Who initiates", "What triggers proactive contact"],
    [["<b>Uber</b>", "Owner", "Nothing. The rider must open the app, find the trip and "
      "request an anonymised call to the driver."],
     ["<b>Hotels</b>", "Owner", "Guest submits an enquiry with dates and description; "
      "staff respond within 72 hours."],
     ["<b>TSA</b>", "Owner", "Owner must describe the item, time and identifying "
      "features. Unclaimed after 30 days it is destroyed or sold."],
     ["<b>University of St Andrews</b>", "Mixed",
      "The receiving unit makes an initial reasonable effort to identify the owner; if "
      "that fails the item goes to a central office and waits."],
     ["<b>Fresno State</b>", "<b>Staff, but only for one item type</b>",
      "A found <b>university ID card</b> is sent to the ID office so it can notify the "
      "individual. Phones and keys are destroyed after a week."],
     ["<b>Airlines</b>", "<b>System</b>",
      "The bag tag's 10-digit licence plate number keys the bag to the passenger record "
      "at every scan point. Reunification is automatic and 66% of mishandled bags are "
      "resolved within 48 hours."]],
    title="Who goes looking for whom",
    sub="Read the last two rows together. The only cases with proactive, staff-initiated "
        "contact are the ones where the object carries an identifier already bound to a "
        "live institutional record.",
    source=cite("uber", "tsa", "standrews", "fresno", "iata"))

d.box("win", "Fresno State is your product, in miniature",
      "<p>Fresno State's own procedures manual says a found <b>university ID card</b> is "
      "forwarded to the ID office <i>so that office can notify the person</i>. Everything "
      "else &mdash; phones, keys &mdash; is destroyed after a week or auctioned after "
      "three months.</p>"
      "<p>The institution already runs a working reunification pipeline. It applies to "
      "exactly one object, because that is the only object with a campus identity on it. "
      "<b>Your entire product is extending that pipeline to everything else a student "
      "carries.</b> That is a far stronger pitch than a new ink, and it is evidenced.</p>"
      + cite("fresno"))

# ================================================================== THE INK =

d.h2("4. What the pivot does to the ink", "ink")
d.p("It inverts the first requirement and promotes the fifth. In the theft case there is "
    "an adversary who must not find the mark. In the loss case <b>there is no adversary at "
    "all</b> &mdash; the only person who will ever look for your mark is someone trying to "
    "help. Hiding it from them is working against yourself.")

d.table(
    ["Requirement", "Under theft", "Under loss", "Status"],
    [["<b>1. Not easily visible</b>",
      "Protective &mdash; stops the thief finding and removing it",
      "<b>No protective function whatsoever.</b> The only remaining reasons to keep a mark "
      "discreet are aesthetic, and privacy: you do not want a phone number readable by "
      "everyone.", chip("invert")],
     ["<b>2. Not easily removed</b>",
      "Critical &mdash; adversary actively attacks it",
      "Still wanted, but much easier. Nothing is trying to remove it; it only has to "
      "survive washing, abrasion and normal wear.", chip("keep")],
     ["<b>3. Harmless to humans</b>", "Required", "Required, unchanged.", chip("keep")],
     ["<b>4. Simple to apply</b>", "Required", "Required, and more so at campus scale.",
      chip("keep")],
     ["<b>5. Easily detectable</b>",
      "Detector is a police officer or pawnbroker who might own a UV torch",
      "<b>Detector is a random member of the public in a coffee shop.</b> This becomes the "
      "binding requirement, and a covert mark fails it outright.", chip("invert")]],
    title="The same five requirements, re-scored for loss",
    sub="Requirements 2, 3 and 4 survive intact. Requirements 1 and 5 now point in "
        "opposite directions, and 5 is the one that determines whether the product works.",
    source=cite("flash", "qrfield"))

d.box("warn", "The measurement that settles it",
      "<p>A spectral study of smartphone flashes across four handsets (iPhone 6s, 8, XR "
      "and Samsung Note8) found they are <b>phosphor-converted white LEDs peaking at "
      "435&ndash;455 nm</b> with a broad 500&ndash;700 nm band. <b>There is no 365 nm "
      "output.</b></p>"
      "<p>So an unmodified phone cannot excite an ordinary UV-fluorescent mark. A finder in "
      "a caf&eacute; would need to own a dedicated 365 nm torch <i>and</i> think to sweep "
      "your water bottle with it. No research quantifies how many people would do that, "
      "and the honest answer is approximately none.</p>"
      "<p>To be precise about the physics: the phone's <i>camera</i> can photograph visible "
      "fluorescence perfectly well if something else supplies the excitation. The failure "
      "is the light source, not the sensor.</p>"
      + cite("flash"))

d.h3("What replaces it")
d.p("An overt, low-disclosure marker resolving through a proxy. The evidence for each "
    "component:")

d.ul([
    "<b>Visible contact affordance works.</b> In the 2025 Chinese field experiment, 660 "
    "wallets each carried a visible sticker reading \u201cScan the QR code to contact the "
    "owner\u201d. <b>66.3% of recipients scanned it and 59.3% phoned the owner.</b> The "
    "wallets were handed to reception staff rather than found in the wild, so this is not "
    "a population finder rate \u2014 but it shows the affordance is used when present.",
    "<b>Never print the actual contact details.</b> The Washington State Attorney General "
    "explicitly advises against putting a home address on a luggage tag, because it tells "
    "a thief where the empty house is. Use a code that resolves through your service and "
    "relays the message; reveal nothing about the owner.",
    "<b>Durable visible marking on textiles is a solved problem.</b> QR codes sublimated "
    "onto polyester at 20 mm or larger stayed <b>100% readable through five 40&nbsp;&deg;C "
    "wash and tumble-dry cycles</b>; heat-transfer at 30&ndash;50 mm likewise. Embroidered "
    "codes failed. Separately, screen-printed tags on cotton and polyester survived "
    "<b>7,500 Martindale abrasion cycles with under 20% erosion</b> and ten 60&nbsp;&deg;C "
    "wash cycles with as little as 2% erosion.",
    "<b>Do not assume scanning is automatic.</b> A naturalistic study observed 7,356 people "
    "entering a university library past a displayed QR code: <b>58 approached and only 22 "
    "scanned it &mdash; 0.30%</b>. That was an unmotivated poster rather than a found "
    "object, and motive plainly matters, but it is a warning against assuming a code gets "
    "used simply because it exists.",
    "<b>Keep a covert mark only as a secondary layer.</b> It has one real use in the loss "
    "case: proving ownership in a dispute over an unlabelled item, and surviving after a "
    "visible label is scuffed off. It should never be the primary discovery route.",
])
d.raw(f'<p class="srcnote">{cite("china", "wa", "qrtextile", "screenprint", "qrfield")}</p>')

d.fig(
    C.vbar([Bar("Sublimation\n\u226520 mm", 100, color=C.POSITIVE),
            Bar("Heat transfer\n30\u201350 mm", 100, color=C.POSITIVE),
            Bar("Sublimation\n10 mm", 0, color=C.NEGATIVE),
            Bar("Embroidery", 0, color=C.NEGATIVE)],
           unit="%", height=260),
    "QR readability after five wash and tumble-dry cycles",
    "Percentage of codes still fully readable, on 100% polyester interlock, ISO 6330, "
    "40 \u00b0C, decoded five times each in under three seconds by a standard phone. "
    "Of 33 samples overall, 21 stayed fully readable and 3 degraded &mdash; all three "
    "were embroidered.",
    cite("qrtextile"))

# ================================================================== ADVICE ==

d.h2("5. NFC: how it works, and what it can and cannot be", "nfc")
d.p("NFC resolves the aesthetic objection better than anything else available, because it "
    "needs no visible marking at all. But the physics imposes hard limits on how small it "
    "can go, and \u201cunremovable\u201d is the one requirement it cannot meet as a "
    "sticker.", "lede")

d.h3("How it actually works")
d.ul([
    "<b>It is magnetic coupling, not radio.</b> NFC runs at <b>13.56 MHz \u00b1 7 kHz</b> "
    "and operates in the <i>near field</i>. The reader drives an alternating current "
    "through a coil, producing an oscillating magnetic field. ISO/IEC 14443-2 requires the "
    "reader to produce between <b>1.5 and 7.5 A/m</b> at the tag.",
    "<b>The tag has no battery and no transmitter.</b> The tag is a coil plus a chip. The "
    "reader's changing magnetic field induces a voltage in the tag's coil by Faraday "
    "induction; the chip rectifies and regulates that to power itself. The reader's field "
    "is literally the tag's power supply.",
    "<b>The tag answers by changing how much power it draws.</b> This is <b>load "
    "modulation</b>: the tag switches a load across its own coil, which changes the "
    "impedance the reader sees in its coil. For Type A the tag does this against a "
    "subcarrier at <b>fc/16 = 847.5 kHz</b>. Nothing is transmitted; the reader is "
    "detecting a tiny disturbance in its own field.",
    "<b>This is why range is centimetres and why size matters so much.</b> In the near "
    "field the coupling falls off roughly as the cube of distance, and the mutual "
    "inductance between the two coils scales with <b>coil area</b> and turns. Halving the "
    "tag's dimensions does far more damage than intuition suggests.",
    "<b>Tuning matters.</b> The coil and its capacitance form an LC circuit resonant near "
    "13.56 MHz. NXP's design guidance gives typical antenna values of 0.3\u20133 \u00b5H "
    "inductance and quality factor Q of 20\u201335. Anything that detunes the circuit "
    "\u2014 principally metal \u2014 destroys power transfer.",
    "<b>The data format is NDEF.</b> A URI record holds a URL. That is what makes a phone "
    "offer to open your page.",
])
d.raw(f'<p class="srcnote">{cite("iso14443", "an11564", "ntag")}</p>')

d.h3("Can it be tiny, flat, soft and invisible?")

d.table(
    ["Requirement", "Answer", "Evidence"],
    [["<b>Tiny</b>", "<b>Yes, within limits</b>",
      "Identiv's ID-Tiny is <b>3.5 \u00d7 13 mm</b> with 320 bytes. A 6 mm round inlay "
      "exists but its vendor quotes a read range of about <b>2 mm</b> \u2014 that is touch "
      "contact, not tap. Measured phone read ranges in a peer-reviewed test: a 160 \u00d7 "
      "80 mm coil gave 8.1 cm, an 80 \u00d7 80 mm coil 5.0 cm, and the best commercial tag "
      "5.6 cm. Smaller means closer."],
     ["<b>Flat</b>", "<b>Yes, easily</b>",
      "A clear PET wet inlay measures <b>136 \u00b5m</b> total thickness \u2014 about the "
      "thickness of a sheet of paper. A 20 \u00d7 10 mm clear inlay is 0.2 mm."],
     ["<b>Soft and flexible</b>", "<b>Yes</b>",
      "PET and polyimide inlays flex readily and conform to curves. Datasheets rarely "
      "publish a minimum bend radius, so a crease across the chip or antenna trace is the "
      "failure mode to test for."],
     ["<b>Invisible</b>", "<b>Almost</b>",
      "The substrate is genuinely clear, but the antenna is an etched aluminium coil and "
      "<i>is</i> visible. Truly transparent conductors exist \u2014 a metal-mesh and "
      "carbon-nanotube hybrid reaches <b>85\u201390% optical transparency</b> \u2014 but "
      "at roughly half the range in a matched comparison, and the mesh is still visible "
      "on close inspection. Hidden under an opaque label, none of this matters."],
     ["<b>Unremovable</b>", "<b>No, not as a sticker</b>",
      "Permanent acrylic adhesives and destructible face stock make a tag <i>hard</i> to "
      "remove and make removal obvious, but a determined person with a heat gun and a "
      "blade wins. Genuine permanence needs embedding at manufacture \u2014 in-mould, "
      "overmoulded, potted in resin, or sewn and heat-sealed into a textile."],
     ["<b>Durable</b>", "<b>Yes, demonstrably</b>",
      "An IP68-rated 22 mm inlay is datasheet-tested to <b>60 cycles of 60 \u00b0C domestic "
      "wash and tumble dry</b> (ISO 6330) plus heat transfer at 160 \u00b0C for 20 seconds "
      "per side. That comfortably covers a backpack."]],
    title="The five requirements against real datasheets",
    sub="Every figure here is from a manufacturer datasheet, an ISO standard or a "
        "peer-reviewed measurement, not from marketing copy.",
    source=cite("identiv", "avery_circus", "avery_dura", "gototags", "bopla", "arxivnfc",
                "armata"))

d.box("warn", "The one that will bite you: metal",
      "<p>An NFC tag stuck to aluminium or steel stops working. A conductive surface near "
      "the coil develops <b>eddy currents</b> that oppose the reader's field, absorb power "
      "and detune the resonant circuit. NXP's own antenna design note describes exactly "
      "this mechanism.</p>"
      "<p>The fix is a <b>ferrite layer</b> between tag and metal to redirect the flux. "
      "That works, but it makes the tag bigger, thicker and opaque: a typical on-metal "
      "NFC label carries a <b>35 mm antenna in a 38 mm die-cut</b> with an opaque face.</p>"
      "<p>For your target items this splits cleanly. <b>AirPods cases, backpacks, "
      "notebooks and plastic bottles are fine</b> \u2014 they are non-conductive, and your "
      "own example is the best case of all. <b>Aluminium laptop lids and steel water "
      "bottles are the hard ones</b>, and there the honest answer is either an on-metal tag "
      "on the plastic underside, or a different marking method entirely.</p>"
      + cite("an11564", "avery_bullseye"))

d.box("win", "The part that makes this work: no app required",
      "<p>Apple's Core NFC documentation confirms that <b>iPhone XS and later read NDEF "
      "tags in the background with no app installed</b>. The system reads the first URI "
      "record, shows a notification, and the user taps it to open the link. It will not "
      "fire while the camera or Apple Pay is in use, in airplane mode, or before the phone "
      "has been unlocked once.</p>"
      "<p>Android reads NDEF tags when the screen is unlocked and dispatches the URI by "
      "intent; if no installed app claims it, behaviour falls back to the browser and, "
      "from Android 17, requires an explicit interaction to open a web link.</p>"
      "<p>So a finder taps a phone against an AirPods case and gets a notification. That is "
      "the entire interaction, and it needs no visible marking, no app and no account. It "
      "is a materially better user experience than a QR code, which requires the finder to "
      "see a code, open the camera and frame it.</p>"
      + cite("apple_nfc", "android_nfc"))

d.box("caveat", "But solve discovery, or none of it matters",
      "<p>NFC removes the visible mark. It does not remove the need for the finder to know "
      "there is something to tap. An unmarked AirPods case looks exactly like an unmarked "
      "AirPods case.</p>"
      "<p>Two ways out, and you should probably do both. First, a <b>very small discreet "
      "symbol</b> \u2014 a few millimetres, in the conventional place manufacturers "
      "already put regulatory marks \u2014 signalling that the item is tappable. Second, "
      "and more reliably, <b>train the institution</b>: campus lost-property desks tap "
      "everything on intake as a matter of routine. The second path does not depend on "
      "public awareness at all, and the desks already inspect items for names by hand.</p>"
      "<p>Cost is not the obstacle: clear NTAG213 inlays list at roughly "
      "<b>$0.14\u20130.16 each at volume</b>.</p>"
      + cite("gototags", "fresno"))

d.h2("6. What to build", "build")

d.box("insight", "The design the evidence points at",
      "<p><b>A visible, durable, low-disclosure identity marker bound to the campus ID "
      "system, plus a proactive notification pipeline in the lost-property office.</b></p>"
      "<p>Concretely, four parts:</p>"
      "<ol>"
      "<li><b>Mark</b> \u2014 an overt printed or sublimated code, not covert ink. It says "
      "only \u201cfound me? scan\u201d and a short code. No name, no number, no address.</li>"
      "<li><b>Resolve</b> \u2014 the code resolves to a relay page that lets the finder "
      "notify the owner without seeing who they are, and tells them the nearest hand-in "
      "point. One tap, no app, no account.</li>"
      "<li><b>Bind to a live record</b> \u2014 this is the part the pet data says everyone "
      "gets wrong. 35.4% of failures were dead phone numbers. Binding to a university "
      "account that the registrar already keeps current eliminates that failure mode "
      "entirely, and no consumer tag service can match it.</li>"
      "<li><b>Push, do not wait</b> \u2014 make the lost-property office scan intake and "
      "notify automatically, the way Fresno State already does for ID cards and the way "
      "airlines do for bags. Every workflow examined here is owner-initiated; that is the "
      "gap.</li>"
      "</ol>")

d.table(
    ["Keep from the original idea", "Change", "Why"],
    [["Durable marking", "Make it <b>visible</b>",
      "There is no adversary in the loss case. The only person who will look for the mark "
      "is trying to help you."],
     ["Detectability", "Target the phone everyone already has, not a UV torch",
      "Smartphone flashes emit 435\u2013455 nm and no 365 nm. An unmodified phone cannot "
      "excite UV ink."],
     ["Wash and abrasion resistance", "Keep it \u2014 this requirement survives intact",
      "Sublimated QR at \u226520 mm survived five wash cycles at 100% readability; screen "
      "print survived 7,500 abrasion cycles with under 20% erosion."],
     ["Identity as the mechanism", "Add a <b>live</b> contact route, not a static one",
      "35.4% of identified pets failed to reunite on a dead phone number alone."],
     ["Campus as the context", "Exploit the registrar, not just the buildings",
      "A university already maintains current contact details for every student. That is "
      "the single biggest structural advantage you have and it is free."],
     ["Covert ink", "Demote to an optional second layer",
      "Useful for proving ownership in a dispute or surviving a scuffed label. Useless as "
      "the primary discovery route."]],
    title="Carrying the good parts of the idea across the pivot",
    source=cite("flash", "qrtextile", "screenprint", "lord", "fresno"))

# ============================================================== LIMITATIONS =

d.h2("Limitations", "limits")
d.ul([
    "<b>Link (c) is not directly evidenced and cannot honestly be presented as if it "
    "were.</b> No experiment has compared identifiable with unidentifiable objects. The "
    "pet analogue is strong but it is an analogue.",
    "<b>The microchip comparison is confounded by selection.</b> Owners who microchip are "
    "plausibly more attached and more likely to search, and the figures are shelter-level "
    "medians rather than individual-level matched comparisons.",
    "<b>The Chinese wallet study handed items to reception staff at institutions</b> "
    "&mdash; pharmacies, museums, hotels, police stations. Those are unusually "
    "conscientious finders in an unusually clear situation. It is not a coffee-shop "
    "stranger rate.",
    "<b>Lost-letter studies are a proxy, not lost property.</b> Posting an addressed letter "
    "is a much lower-effort act than tracking down the owner of a water bottle.",
    "<b>Stated intent overstates behaviour.</b> 68% of USB finders said they meant to "
    "return the drive; 18% of drives came back.",
    "<b>The QR scanning study measured an unmotivated public poster</b>, not a found "
    "object. Its 0.30% should be read as a caution about assuming scans, not as a forecast "
    "of your conversion rate.",
    "<b>Textile durability results are from two studies on woven cotton and polyester.</b> "
    "Knits, nonwovens, coated fabrics and dry cleaning are untested.",
    "<b>No operator publishes the fraction of found items carrying identification</b>, "
    "which is the single statistic that would let you size this market precisely. It does "
    "not appear to exist.",
])

d.h2("Sources", "sources")
rows = []
for k, (t, org, url, kind, yr) in sorted(S.items(), key=lambda x: x[1][1]):
    tick = " &#10003;" if k in LEAD else ""
    rows.append([f"{org}{tick}", f'<a href="{url}">{t}</a>', yr, chip(kind)])
d.table(["Organisation", "Publication", "Year", "Type"], rows,
        title="Sources", sub=f"{len(S)} sources, all opened. A tick marks those the author "
                             "read personally to verify a load-bearing figure.",
        source="<b>Rebuild:</b> <code>python3 research/build_loss_pivot.py</code>")

OUT.write_text(d.html("Loss and reunification: verifying the premise", MASTHEAD),
               encoding="utf-8")
print(f"wrote {OUT} ({OUT.stat().st_size:,} bytes, {d.fig_n} figures, "
      f"{d.tab_n} tables, {len(S)} sources)")
