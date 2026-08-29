#!/usr/bin/env python3
"""Build the one-day prototype build guide.

    python3 research/build_oneday.py  ->  research/one-day-build.html
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import charts as C  # noqa: E402
from charts import Bar  # noqa: E402
from shell import REPORTS, Doc  # noqa: E402

OUT = REPORTS / "one-day-build.html"

S = {
    "avery": ("AD Circus NFC NTAG213 data sheet", "Avery Dennison",
              "https://rfid.averydennison.com/content/dam/rfid/en/products/rfid-products/"
              "data-sheets/datasheet-Circus-NFC-NTAG213.pdf", "vendor", "2026"),
    "gtt": ("Clear wet NFC inlay NTAG213, 20 x 10 mm", "GoToTags",
            "https://store.gototags.com/clear-wet-nfc-inlay-ntag213-20-x-10-mm-rectangle/",
            "vendor", "2026"),
    "identiv": ("ID-Tiny A613 ST25TV data sheet", "Identiv",
                "https://identiv.com/wp-content/uploads/2026/07/"
                "ID-Tiny-A613-ST25TV_Datasheet_06_26.pdf", "vendor", "2026"),
    "bullseye": ("AD Bullseye On-Metal data sheet", "Avery Dennison",
                 "https://rfid.averydennison.com/content/dam/rfid/en/products/"
                 "rfid-products/data-sheets/datasheet-Bullseye-On-Metal.pdf",
                 "vendor", "2026"),
    "ntag": ("NTAG213/215/216 product data sheet", "NXP Semiconductors",
             "https://www.nxp.com/docs/en/data-sheet/NTAG213_215_216.pdf",
             "official", "2015"),
    "tagwriter": ("NFC TagWriter user manual", "NXP Semiconductors",
                  "https://inspire.nxp.com/tagwriter/tag-writer-user-manual.pdf",
                  "official", "2024"),
    "apple_bg": ("Adding support for background tag reading", "Apple",
                 "https://developer.apple.com/documentation/corenfc/"
                 "adding-support-for-background-tag-reading", "official", "2026"),
    "apple_write": ("Core NFC: NDEF writing (WWDC19 session 715)", "Apple",
                    "https://developer.apple.com/videos/play/wwdc2019/715/",
                    "official", "2019"),
    "an13219": ("AN13219 — NFC antenna design with ferrite", "NXP Semiconductors",
                "https://www.nxp.com/docs/en/application-note/AN13219.pdf",
                "official", "2021"),
    "vhb": ("3M VHB Tape 5952 technical data sheet", "3M",
            "https://multimedia.3m.com/mws/media/2366487O/3m-vhb-tape-5952.pdf",
            "vendor", "2024"),
    "lse": ("3M adhesive transfer tapes with 300LSE", "3M",
            "https://multimedia.3m.com/mws/media/142939O/"
            "adh-transfer-tapes-with-adhesive-300lse.pdf", "vendor", "2024"),
    "e6000": ("E6000 Industrial technical data sheet", "Eclectic Products",
              "https://eclecticproducts.com/downloads/tds-e6000-industrial-english-clear.pdf",
              "vendor", "2024"),
    "avery_fabric": ("Printable fabric instructions (3384)", "Avery",
                     "https://www.avery.com/help/article/printable-fabric-instructions-3384",
                     "vendor", "2026"),
    "twilio": ("Trial account restrictions", "Twilio",
               "https://www.twilio.com/docs/usage/trials", "official", "2026"),
    "resend": ("Pricing and quotas", "Resend", "https://resend.com/pricing",
               "vendor", "2026"),
    "amzn": ("Timeskey clear NTAG213 stickers, 30-pack", "Amazon listing",
             "https://www.amazon.com/dp/B0DSLB8B5K", "vendor", "2026"),
    "adafruit": ("NTAG213 NFC sticker (product 4032)", "Adafruit",
                 "https://www.adafruit.com/product/4032", "vendor", "2026"),
    "sparkfun": ("Adhesive MIFARE Classic 1K tag", "SparkFun",
                 "https://www.sparkfun.com/rfid-tag-adhesive-mifare-classicr-1k-"
                 "13-56-mhz.html", "vendor", "2026"),
    "vercel": ("Limits (Hobby plan)", "Vercel", "https://vercel.com/docs/limits",
               "vendor", "2026"),
}
LEAD = {"avery", "gtt", "apple_bg", "twilio"}


def cite(*keys: str, extra: str = "") -> str:
    bits = []
    for k in keys:
        t, org, url, kind, yr = S[k]
        tick = " &#10003;" if k in LEAD else ""
        bits.append(f'<a href="{url}">{org}, <i>{t}</i></a> ({yr}){tick}')
    s = "<b>Source:</b> " + "; ".join(bits) + "."
    return f"{s} {extra}" if extra else s


def chip(k: str) -> str:
    m = {"official": ("c-off", "Official"), "vendor": ("c-ven", "Vendor"),
         "go": ("c-strong", "Do it"), "no": ("c-none", "Skip"),
         "risk": ("c-weak", "Risk")}
    cls, txt = m[k]
    return f'<span class="chip {cls}">{txt}</span>'


d = Doc()

MASTHEAD = """
<div class="masthead">
  <div class="kicker">Build Guide &middot; One Day</div>
  <h1>Ship a working tag-to-owner prototype today</h1>
  <div class="standfirst">Exact sizes, a shopping list, an hour-by-hour plan, the
  no-code way to write NFC tags, what to glue with, and a demo script that will not
  fail in front of judges. The software is already written and tested &mdash; it is
  in <code>research/prototype/app.py</code>.</div>
  <div class="meta">
    <div><b>Tag size</b>20 &times; 10 &times; 0.2 mm</div>
    <div><b>Cost</b>Around $0.30&ndash;0.45 a tag retail</div>
    <div><b>Software</b>Written, tested, zero dependencies</div>
    <div><b>Biggest risk</b>Metal. Read section 5</div>
  </div>
</div>"""

# ================================================================== SIZE ====

d.h2("1. How big is it, exactly", "size")
d.p("You conflated two products. They are different, and the difference matters.", "lede")

d.table(
    ["Product", "Outer size", "Antenna", "Thickness", "Notes"],
    [["<b>GoToTags clear rectangle</b>", "<b>20 &times; 10 mm</b>", "18 &times; 8 mm",
      "<b>0.2 mm</b>", "Clear PET, permanent acrylic adhesive, flexible, NTAG213 "
      "144 bytes. <b>This is the one to use.</b>"],
     ["<b>Avery AD Circus NFC</b>", "&Oslash; 22 mm", "&Oslash; 20 mm",
      "<b>0.136 mm</b>", "The 136 &micro;m figure you remembered. Round, clear PET "
      "face, thinner but a bigger footprint."],
     ["<b>Identiv ID-Tiny</b>", "13 &times; 3.5 mm", "same",
      "0.21 mm", "Smallest practical. Tiny antenna means very short range."],
     ["<b>On-metal (ferrite)</b>", "&Oslash; 38 mm", "&Oslash; 35 mm",
      "thicker, opaque", "Needed for steel bottles and aluminium laptops. Big and "
      "not discreet."]],
    title="Real dimensions from manufacturer datasheets",
    sub="The thinnest is not the smallest. The 136 &micro;m Avery is 22 mm across; "
        "the 20 &times; 10 mm GoToTags is 200 &micro;m thick.",
    source=cite("gtt", "avery", "identiv", "bullseye"))

d.box("insight", "What that actually feels like",
      "<p>The recommended tag is <b>20 &times; 10 mm and 0.2 mm thick</b>. So:</p>"
      "<ul>"
      "<li><b>Footprint:</b> smaller than an adult thumbnail. Shorter than a US "
      "penny is wide (19.05 mm) in one direction, half that in the other.</li>"
      "<li><b>Thickness:</b> about <b>two sheets of office paper</b>. A US penny is "
      "1.52 mm, so the tag is roughly <b>eight times thinner than a penny</b>.</li>"
      "<li><b>Feel:</b> flexible, and under a printed label you cannot feel a step "
      "with a fingertip.</li>"
      "</ul>"
      "<p>The Avery round one is thinner still &mdash; 0.136 mm, around <b>1.4 sheets "
      "of paper</b>, or roughly two human hairs &mdash; but it is 22 mm across.</p>")

d.fig(
    C.hbar([
        Bar("On-metal ferrite tag (for steel)", 38, color=C.NEGATIVE),
        Bar("Avery AD Circus, round", 22, color=C.ACCENT),
        Bar("GoToTags rectangle (recommended)", 20, color=C.POSITIVE),
        Bar("US penny, for scale", 19.05, color=C.PALETTE[7]),
        Bar("Identiv ID-Tiny", 13, color=C.PALETTE[0]),
    ], unit=" mm", dp=1, label_w=270, vmax=45),
    "Largest dimension of the whole tag",
    "Everything usable sits between 13 and 22 mm across. Only the on-metal tag, which "
    "needs a ferrite layer, is meaningfully bigger.",
    cite("gtt", "avery", "identiv", "bullseye"))

d.box("warn", "Why you cannot just go smaller",
      "<p>Range comes from the <b>area</b> of the antenna coil, because this is "
      "near-field magnetic coupling. Shrinking the tag shrinks the coil and the range "
      "collapses fast. A 6 mm round tag is sold, and its vendor quotes a read range of "
      "about <b>2 mm</b> &mdash; that is not a tap, that is touching it in exactly the "
      "right spot.</p>"
      "<p>Peer-reviewed phone measurements: a 160 &times; 80 mm coil read at 8.1 cm, an "
      "80 &times; 80 mm coil at 5.0 cm, and the best commercial tag tested at 5.6 cm. "
      "At 20 &times; 10 mm expect roughly <b>1&ndash;2 cm</b> &mdash; fine for a "
      "deliberate tap, useless for a wave.</p>")

# ============================================================== SHOPPING ====

d.h2("2. Shopping list", "shopping")

d.table(
    ["Item", "Why", "Notes"],
    [["<b>NTAG213 clear stickers, 30&ndash;50 pack</b>", "The tags themselves",
      "About $13 for 30&ndash;50 on Amazon. <b>Insist on NTAG213/215.</b> Cheap "
      "\u201cNFC\u201d packs are often NTAG203 or NTAG210 with too little memory, "
      "and SparkFun's adhesive tag is MIFARE Classic, which iPhones do not reliably "
      "read."],
     ["<b>2&ndash;3 on-metal ferrite tags</b>", "Steel bottle and laptop lid",
      "Buy these separately. Without one, a tag on steel simply will not read, and "
      "that failure is silent."],
     ["<b>3M 300LSE transfer tape</b>", "Sticking to plastic",
      "Thin, bonds to low-surface-energy plastics. Better than generic double-sided "
      "tape on an AirPods case."],
     ["<b>A few plain white printed labels</b>", "Hiding the tag, and the QR fallback",
      "Print your logo plus a small QR, stick over the tag."],
     ["<b>Needle and thread</b>", "Backpack and hoodie",
      "A sewn-in pocket takes ten minutes and needs no cure time. This is the only "
      "textile method that is definitely ready by demo time."],
     ["<b>Isopropyl alcohol wipes</b>", "Surface prep",
      "Adhesion on a greasy case is the difference between working and peeling off "
      "on stage."]],
    title="What to buy or scrounge",
    sub="Total cost is trivial. The binding constraint is delivery time, so buy "
        "locally or same-day if you can.",
    source=cite("amzn", "adafruit", "sparkfun", "lse"))

d.box("warn", "Two purchases that will waste your day",
      "<ul>"
      "<li><b>Generic \u2018NFC stickers\u2019 with no chip named.</b> If the listing "
      "does not say NTAG213, NTAG215 or NTAG216, do not buy it.</li>"
      "<li><b>MIFARE Classic tags.</b> Widely sold, cheap, and not reliably readable "
      "by iPhone. SparkFun's adhesive RFID tag is one of these.</li>"
      "</ul>")

# ================================================================ TIMELINE ==

d.h2("3. The hour-by-hour plan", "plan")

d.table(
    ["Hours", "Who", "What"],
    [["<b>0&ndash;1</b>", "Everyone",
      "Buy tags. Start the server: <code>python3 research/prototype/app.py</code>. "
      "Expose it with ngrok or deploy it, because the tag needs a public HTTPS URL."],
     ["<b>1&ndash;2</b>", "Hardware",
      "Write one tag with NFC Tools. Tap it with the actual demo phone. <b>Do not "
      "proceed until this works.</b> Everything else depends on it."],
     ["<b>1&ndash;4</b>", "Software",
      "The relay already works. Spend this time on what judges see: your branding, "
      "the building list, a campus map, an owner dashboard that looks finished."],
     ["<b>2&ndash;4</b>", "Hardware",
      "Tag five items. Apply, hide under printed labels, sew the backpack pocket. "
      "Test read after every single assembly step."],
     ["<b>4&ndash;6</b>", "Everyone",
      "Rehearse the demo end to end on the venue wifi, with the phones you will "
      "actually use. Find the failures now."],
     ["<b>6&ndash;8</b>", "Everyone",
      "Slides, the evidence story from the research reports, and a recorded video "
      "of the working demo as insurance."]],
    title="A realistic day",
    sub="Note the ordering: prove the tag reads before you build anything on top of "
        "it. Teams routinely lose a day to a tag that was never going to work.")

d.box("win", "The software is done",
      "<p><code>research/prototype/app.py</code> is a complete, tested implementation: "
      "create tags, owner claims a tag, finder taps and reports a location, owner's "
      "dashboard updates <b>live</b>. It is <b>pure Python standard library</b> "
      "&mdash; no pip install, no API keys, no accounts.</p>"
      "<p>The whole loop was tested end to end: a finder submission reached the owner's "
      "dashboard in real time, and the finder page names the item without revealing "
      "anything about the owner.</p>"
      "<p><b>Run it:</b> <code>python3 app.py</code>, then <code>ngrok http 8000</code> "
      "and restart with <code>BASE_URL=https://your.ngrok.app python3 app.py</code>.</p>")

# ============================================================ WRITING TAGS ==

d.h2("4. Writing the tags, with no code", "writing")

d.p("Use <b>NFC Tools</b> or <b>NXP TagWriter</b>. Both are free. The NXP manual gives "
    "the exact sequence:")

d.ol([
    "Copy the tag URL from the claim page &mdash; it looks like "
    "<code>https://your.ngrok.app/i/MXFNV8</code>.",
    "Open NFC TagWriter &rarr; <b>Write tags</b> &rarr; <b>New dataset</b> &rarr; "
    "<b>LINK</b>.",
    "Paste the URL &rarr; <b>SAVE &amp; WRITE</b> &rarr; <b>WRITE</b>, then hold the "
    "phone against the tag until it confirms.",
    "For a batch: <b>Write tags</b> &rarr; <b>My Datasets</b> &rarr; <b>Extras</b> "
    "&rarr; <b>Write Multiple</b>.",
    "Test by tapping with a different phone. <b>Only then</b> consider "
    "<b>Protect tags</b> &rarr; <b>Lock tag</b> &mdash; this is permanent and "
    "irreversible, so keep spare unlocked tags.",
])

d.table(
    ["Question", "Answer"],
    [["Can an iPhone <b>write</b> tags?",
      "Yes, iPhone 7 and later via Core NFC. Any recent iPhone can encode your tags."],
     ["Can a phone <b>read</b> with no app?",
      "iPhone XS and later read NDEF URL records in the background: a notification "
      "appears and the user taps it. Android reads when unlocked."],
     ["How long can the URL be?",
      "NTAG213 has 144 bytes of user memory, so keep the URL under about 130 "
      "characters. A short domain and a six-character code is comfortable."],
     ["Which phone for the judge demo?",
      "iPhone XS or later, or any modern Android. An iPhone 7 to 11 can write tags "
      "but will not do the background read that makes the demo magic."]],
    title="The things people get wrong",
    source=cite("tagwriter", "apple_bg", "apple_write", "ntag"))

# ============================================================== PACKAGING ==

d.h2("5. Sticking it on, and the metal problem", "packaging")

d.box("warn", "Read this before you glue anything",
      "<p><b>A plain NFC tag on steel or aluminium does not work.</b> The metal "
      "develops eddy currents that oppose the reader's field and detune the tag. It "
      "does not degrade gracefully &mdash; it just fails, silently, in front of the "
      "judge.</p>"
      "<p>Your steel water bottle and your aluminium laptop lid both need a "
      "<b>ferrite-backed on-metal tag</b>, which is about 38 mm and opaque. If you "
      "cannot get one today, stick the tag on the plastic underside of the laptop, or "
      "on a plastic sleeve on the bottle, or hold it off the metal with a 3&ndash;5 mm "
      "plastic spacer. Do not improvise this on stage.</p>"
      + cite("an13219", "bullseye"))

d.table(
    ["Item", "Method", "Ready in time?"],
    [["<b>AirPods case</b> (plastic)", "Trim a clear inlay, clean with IPA, apply with "
      "3M 300LSE, cover with a small printed label", "<b>Yes.</b> Pressure-sensitive, "
      "handles immediately"],
     ["<b>Backpack</b> (nylon)", "Sew a small fabric pocket into a seam and slip the "
      "tag inside", "<b>Yes.</b> No cure at all, 10&ndash;15 minutes"],
     ["<b>Hoodie</b>", "Sewn-in pocket, or iron-on patch with the tag inside "
      "(315 &deg;F, 30&ndash;45 s)", "Sewing yes. Iron-on yes but needs 24 h before it "
      "gets wet"],
     ["<b>Notebook</b>", "Tag inside the back cover, under a label", "<b>Yes</b>"],
     ["<b>Plastic bottle</b>", "300LSE under the existing wrap label", "<b>Yes</b>"],
     ["<b>Steel bottle</b>", "<b>On-metal ferrite tag</b> plus VHB, or plain tag on a "
      "plastic sleeve", "Only with the right tag"],
     ["<b>Laptop</b>", "Plastic underside with 300LSE. <b>Not the aluminium lid.</b>",
      "<b>Yes</b>, on the underside"]],
    title="Per-item method, ranked for today",
    source=cite("lse", "vhb", "avery_fabric", "an13219"))

d.fig(
    C.hbar([
        Bar("Sewn fabric pocket", 0.2, color=C.POSITIVE),
        Bar("3M 300LSE / VHB (handling strength)", 0.3, color=C.POSITIVE),
        Bar("Hot glue", 0.1, color=C.ACCENT),
        Bar("VHB to 50% strength", 0.3, color=C.POSITIVE),
        Bar("Iron-on patch", 0.8, color=C.ACCENT),
        Bar("VHB to 90% strength", 24, color=C.NEGATIVE),
        Bar("E6000 initial cure", 24, color=C.NEGATIVE),
        Bar("VHB to full strength", 72, color=C.NEGATIVE),
        Bar("E6000 full cure", 72, color=C.NEGATIVE),
    ], unit=" h", dp=1, label_w=270, vmax=80),
    "Cure times: what is actually ready today",
    "Anything above a couple of hours is not going to be set for your demo. Sewing and "
    "pressure-sensitive tape are the only genuinely same-day permanent options.",
    cite("vhb", "lse", "e6000", "avery_fabric"))

# =============================================================== SOFTWARE ==

d.h2("6. Software choices, if you rewrite it", "software")
d.p("The provided app is deliberately dependency-free so it cannot break. If you would "
    "rather build it in something you know, here is the fastest credible stack and the "
    "traps.")

d.table(
    ["Choice", "Verdict", "Why"],
    [["Next.js on Vercel Hobby + Supabase", chip("go"),
      "Fastest path to a public HTTPS URL with a database. Free tiers are ample for a "
      "demo."],
     ["Server-sent events for owner notification", chip("go"),
      "No API key, no deliverability risk, instant. This is what the provided app "
      "uses and it is the safest demo mechanism there is."],
     ["Discord webhook", chip("go"),
      "About ten minutes to set up and very reliable. Good visible \u2018ping\u2019 "
      "for a room."],
     ["Resend for real email", chip("go"),
      "Free tier is 3,000 a month and 100 a day. Verify your domain early, not at "
      "hour seven."],
     ["<b>Twilio SMS</b>", chip("no"),
      "<b>Trial accounts can only send to pre-verified numbers, up to five.</b> A "
      "judge's phone will not be one of them. This kills demos."],
     ["iOS App Clips", chip("no"),
      "Needs a full app binary and App Store Connect configuration. A plain HTTPS URL "
      "already works with no app."],
     ["Forking an existing project", chip("no"),
      "We looked. The candidates are a zero-star scaffold and an unmaintained PHP app. "
      "Nothing is worth the integration time."]],
    title="Stack decisions",
    source=cite("vercel", "resend", "twilio", "apple_bg"))

# =================================================================== DEMO ==

d.h2("7. The demo script", "demo")

d.box("insight", "Give the judge the phone",
      "<p>Do not demo it yourself. Hand the judge <i>their own</i> phone situation: "
      "put the tagged AirPods case on the table, ask them to tap their phone against "
      "it, and let them watch your teammate's screen light up across the room.</p>"
      "<p>That single interaction does the entire pitch. No app, no signup, two "
      "seconds.</p>")

d.ol([
    "<b>Set up:</b> teammate's phone on the table showing the owner dashboard, screen "
    "awake, page open. This is the receiving end.",
    "<b>Line:</b> \u201cThis is a normal AirPods case. There is nothing on the "
    "outside.\u201d Let them look.",
    "<b>Judge taps.</b> A notification appears on their phone. They tap it and your "
    "page opens in their browser.",
    "<b>They press one button</b> and choose a building.",
    "<b>The dashboard across the room updates instantly.</b> Point at it.",
    "<b>Land the point:</b> the finder never saw who owns it, the owner never saw who "
    "found it, and nobody installed anything.",
    "<b>Then the evidence:</b> phones return at 82.8% and umbrellas at 1.4% because "
    "phones can say whose they are. This makes everything else behave like a phone.",
])

d.table(
    ["What breaks", "Why", "Mitigation"],
    [["Tag on metal reads nothing", "Eddy currents detune it",
      "<b>Demo on the plastic AirPods case.</b> Keep the steel bottle as a "
      "\u2018here is the on-metal version\u2019 aside"],
     ["iPhone does not pop the notification", "Camera or Wallet open, airplane mode, "
      "or the phone has not been unlocked since boot",
      "Unlock, close the camera, tap the <b>top edge</b> of an iPhone, hold 1&ndash;2 s"],
     ["Judge has an iPhone older than XS", "No background tag reading",
      "Keep an Android and a modern iPhone on the table as the offered device"],
     ["Thick or metal phone case", "Blocks coupling", "Ask them to take it off"],
     ["Venue wifi dies", "Your URL is unreachable",
      "Run the server on a laptop hotspot; the provided app needs no internet at all"],
     ["Nobody can scan the QR fallback", "Too small or low contrast",
      "Print it at 20&ndash;25 mm minimum, black on white"],
     ["Tag gets overwritten by a curious judge", "It is writable",
      "Lock <i>one</i> demo tag after testing. Keep the rest unlocked"]],
    title="Failure modes, and what to do",
    sub="Every one of these has ended a hackathon demo somewhere. Rehearse against "
        "this list.",
    source=cite("apple_bg", "an13219"))

d.box("warn", "Record a video at hour six",
      "<p>Film the working demo while it works. If anything fails live, you play the "
      "video and keep talking. This costs five minutes and has saved more hackathon "
      "presentations than any amount of engineering.</p>")

# ============================================================== HONESTY ====

d.h2("8. What you cannot do today, and should just say", "honest")
d.ul([
    "<b>Truly unremovable.</b> A sticker is a sticker. Say that real permanence needs "
    "embedding at manufacture &mdash; in-mould or potted &mdash; and that the sticker "
    "is the pilot form factor.",
    "<b>Washing and abrasion validation.</b> Datasheets show an IP68 inlay surviving "
    "60 wash cycles at 60 &deg;C, but you will not have tested your own assembly. Cite "
    "the datasheet, do not claim you verified it.",
    "<b>On-metal at small size.</b> Ferrite tags are 38 mm and opaque. Be upfront that "
    "steel bottles and laptop lids are a known open problem.",
    "<b>Scale of the registry.</b> You will have five tags, not five thousand. The "
    "interesting claim is the workflow, not the database.",
    "<b>Proof it improves recovery.</b> You have strong analogous evidence &mdash; "
    "microchipped stray cats are returned at 38.5% against 1.8% &mdash; but no trial of "
    "your own. Present it as the hypothesis your pilot would test.",
])

d.h2("Sources", "sources")
rows = []
for k, (t, org, url, kind, yr) in sorted(S.items(), key=lambda x: x[1][1]):
    tick = " &#10003;" if k in LEAD else ""
    rows.append([f"{org}{tick}", f'<a href="{url}">{t}</a>', yr, chip(kind)])
d.table(["Organisation", "Publication", "Year", "Type"], rows,
        title="Sources", sub=f"{len(S)} sources. A tick marks those read personally to "
                             "verify a load-bearing figure.",
        source="<b>Rebuild:</b> <code>python3 research/build_oneday.py</code>")

OUT.write_text(d.html("One-day build guide", MASTHEAD), encoding="utf-8")
print(f"wrote {OUT} ({OUT.stat().st_size:,} bytes, {d.fig_n} figures, "
      f"{d.tab_n} tables, {len(S)} sources)")
