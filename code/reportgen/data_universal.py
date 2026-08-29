"""Verified source data for the universal stick-on-anything label report.

Question being answered: does a cheap, multi-surface, privacy-preserving
property label already exist? The answer turned out to be layered, so the data
is organised to keep three separate things apart:

  1. The **physical label** - cheap, durable, multi-surface. Already exists,
     and the market is mature. Prices below are per label at the pack size
     actually sold.
  2. The **machine-readable clothing tag** - NFC and QR on fabric. Also
     already exists, as B2B custom hardware and as industrial laundry RFID.
  3. The **service behind the code** - a scan that resolves to an owner
     without exposing them. This is the part that is thin.

Prices are transcribed from the vendor's own page. GBP figures are left in GBP
and converted only where the report needs a comparison, so the source number
stays checkable.
"""

from __future__ import annotations

VERIFIED_BY_LEAD = {"gototags_price", "avery22806"}

# ---------------------------------------------------------------- sources ---

SOURCES: dict[str, tuple[str, str, str, str, str]] = {
    # --- printed clothing labels -------------------------------------------
    "stikins": ("Stikins information and testing", "Stikins",
                "https://www.stikins.co.uk/stikins-information/", "vendor", "2026"),
    "stikins_order": ("Stikins order page", "Stikins",
                      "https://www.stikins.co.uk/order/", "vendor", "2026"),
    "nameit": ("Classic white iron-on name labels", "Name It Labels",
               "https://www.nameitlabels.co.uk/product/"
               "classic-white-iron-on-name-labels/", "vendor", "2026"),
    "mabels": ("Tag Mates stick-on clothing labels", "Mabel's Labels",
               "https://mabelslabels.com/tag-mates-stick-on-clothing-labels",
               "vendor", "2026"),
    "mynametags": ("My Nametags frequently asked questions", "My Nametags",
                   "https://www.mynametags.com/faq", "vendor", "2026"),
    "easy2name": ("Iron-on name tapes", "Easy2Name",
                  "https://www.easy2name.com/iron-on-name-tapes", "vendor", "2026"),
    "namebubbles": ("Custom clothing labels pack", "Name Bubbles",
                    "https://www.namebubbles.com/products/"
                    "custom-clothing-labels-pack", "vendor", "2026"),
    "labelplanet": ("Do you supply labels that can be washed?", "Label Planet",
                    "https://www.labelplanet.co.uk/labels-blog/product-information/"
                    "faq-do-you-supply-labels-washed/", "vendor", "2026"),

    # --- machine-readable fabric tags ---------------------------------------
    "scivas": ("Washable NFC woven tag", "SCIVAS",
               "https://scivas.com/custom-nfc-tags/washable-nfc-woven-tag.html",
               "vendor", "2026"),
    "datamars": ("RFID textile tracking \u2014 LaundryChip", "Datamars Textile ID",
                 "https://textile-id.com/our-solutions/rfid-textile-tracking/",
                 "vendor", "2026"),

    # --- raw label and tag cost ---------------------------------------------
    "gototags_price": ("Printed NFC sticker, NTAG213 \u2014 volume pricing",
                       "GoToTags",
                       "https://store.gototags.com/printed-nfc-sticker-ntag213/",
                       "vendor", "2026"),
    "avery22806": ("Product 22806, 2\u2033 square labels, 300 pack", "Avery",
                   "https://www.avery.com/products/labels/22806", "vendor", "2026"),

    # --- campus disposal policy ---------------------------------------------
    "liberty": ("Lost and found", "Liberty University",
                "https://www.liberty.edu/flamespass/lost-and-found/",
                "official", "2026"),
    "uga": ("Lost and found, Miller Learning Center",
            "University of Georgia Libraries",
            "https://www.libs.uga.edu/mlc/about/lost-found", "official", "2026"),
    "vtech": ("Lost and found", "Virginia Tech",
              "https://campuslife.vt.edu/secl_services/Lost_and_Found.html",
              "official", "2026"),
    "boise": ("Policy 12160, lost and found property", "Boise State University",
              "https://www.boisestate.edu/policy/lost-and-found-property/",
              "official", "2024"),
    "uwhub": ("HUB lost and found policy A-12", "University of Washington",
              "https://hub.washington.edu/wordpress/wp-content/uploads/2025/10/"
              "A-12-HUB-Lost-and-Found-Policy.pdf", "official", "2025"),
    "tamu": ("A new home for what lost its home", "The Battalion, Texas A&amp;M",
             "https://thebatt.com/life-arts/a-new-home-for-what-lost-its-home/",
             "news", "2023"),
    "whitman": ("Exploring Whitman's lost and found", "The Pioneer via UWire",
                "https://www.uwire.com/2015/02/12/exploring-whitmans-lost-found/",
                "news", "2015"),

    # --- drinkware ----------------------------------------------------------
    "citron": ("Smart QR technology", "Citron",
               "https://citron.ae/pages/smart-qr-technology", "vendor", "2026"),
    "nalgene_custom": ("Customize", "Nalgene",
                       "https://nalgene.com/customize/", "vendor", "2026"),
    "nalgene_faq": ("Frequently asked questions and lifetime guarantee", "Nalgene",
                    "https://nalgene.com/faq/", "vendor", "2026"),
    "yeti": ("Rambler customisation FAQ", "YETI",
             "https://www.yeti.com/rambler-custom-faq.html", "vendor", "2026"),
    "camelbak": ("Fit Cap 32oz insulated stainless steel bottle", "CamelBak",
                 "https://www.camelbak.com/product/"
                 "fit-cap-32oz-water-bottle%2C-insulated-stainless-steel/"
                 "CB-2898.html", "vendor", "2026"),
}

# --------------------------------------------------- printed clothing labels -

# vendor, pack, pack price, per unit, currency, durability claim, carries
PRINTED_LABELS = [
    ("Name It Labels", "100 iron-on", "\u00a311", 0.11, "GBP",
     "machine wash and tumble dry", "Name"),
    ("Stikins", "120 stick-on", "\u00a318", 0.15, "GBP",
     "BS EN ISO6330, 60 washes at 40\u00b0C, dishwasher", "Name, phone, school"),
    ("Mabel's Tag Mates", "100 stick-on", "$23", 0.23, "USD",
     "laundry safe, dishwasher safe on smooth surfaces", "Name, icon"),
    ("My Nametags", "56 stick-on", "\u00a315.95", 0.285, "GBP",
     "up to 60\u00b0C, on care label only", "Name, phone"),
    ("Easy2Name", "30 iron-on", "\u00a38.95", 0.298, "GBP",
     "up to 60\u00b0C, tumble dry", "Name"),
    ("Name Bubbles", "94 mixed", "$29.99", 0.319, "USD",
     "waterproof, hot dryers", "Name, icon"),
]

# ------------------------------------------------ machine-readable on fabric -

FABRIC_TAGS = [
    ("SCIVAS washable NFC woven tag", "$0.11&ndash;0.95", "100",
     "NTAG213/215/216 plus optional dynamic QR",
     "sew-on or iron-on, &ldquo;several domestic wash cycles&rdquo;"),
    ("Datamars LaundryChip FT401-QR", "quote only", "not published",
     "UHF RFID with integrated QR or Datamatrix",
     "industrial wash, detergents, tumble, pressing"),
]

# ------------------------------------------------------------- raw tag cost -

# GoToTags printed NTAG213, adhesive, explicitly flat non-metal surfaces
NFC_VOLUME = [(500, 0.73), (1_000, 0.58), (5_000, 0.40),
              (10_000, 0.35), (50_000, 0.24)]
NFC_MOQ = 500
NFC_LEAD_WEEKS = 3

# Avery 22806, 2in square, paper, permanent adhesive
AVERY = {"pack": 300, "price": 12.49, "unit": 12.49 / 300}

# ---------------------------------------------------- branded tag comparison -

BRANDED = [("PetHub", 9.95), ("ReturnMe", 9.99),
           ("ByteTag", 24.95), ("Crashtag", 29.90)]

# ------------------------------------------------------- campus bottle policy -

# institution, what they do with drink containers
BOTTLE_POLICY = [
    ("Virginia Tech", "Refuses them outright",
     "&ldquo;Water bottles or any drink containers&rdquo; are listed under "
     "items not accepted"),
    ("Boise State", "Immediate disposal",
     "Policy table gives water bottle disposition as "
     "&ldquo;Will Not Accept &mdash; Immediate Disposal&rdquo;"),
    ("Liberty", "Binned after 3 business days",
     "Everything else is held 120 days"),
    ("UGA, Miller Learning Center", "Discarded after 3 days",
     "Cited health and sanitation concerns; some donated to a swap shop"),
    ("UW, the HUB", "Refuses full containers",
     "Central desk takes over 1,000 items a month"),
]

# Texas A&M Memorial Student Center, September 2023
TAMU = {"reunited": 573, "total": 1_675, "annual": 12_000, "daily": "50\u2013100"}

# --------------------------------------------------------------- drinkware ---

DRINKWARE = [
    ("Citron <small>(UAE)</small>", "QR moulded into the bottle",
     "<b>Yes</b> &mdash; register at findmycitron.com, owner notified, "
     "details exchanged only if both sides agree",
     "250 ml and 350 ml models only"),
    ("Nalgene", "Custom print, from $23", "No &mdash; guarantee excludes loss",
     "32 oz wide mouth is $16.99"),
    ("YETI", "Laser engraving, $6 per side", "No", "Front fee waived at 24+ units"),
    ("CamelBak", "None found on the product page", "No", "Fit Cap 32 oz is $35"),
]

UNREACHABLE = ["Hydro Flask customise page (HTTP 403)",
               "Stanley Create pricing (feed exposed no prices)",
               "Petit-Fernand (fetch failed, search snippet only)",
               "YETI QR-engraving incompatibility (snippet only, not read in page)"]

# ------------------------------------ generic stickers WITH a real backend --

# name, pack, per unit USD-ish, surfaces, notes
BACKEND_TAGS = [
    ("Letstrack StickerTAG", "\u00a34.99 / 6", "\u00a30.83",
     "plastic, metal, leather, <b>fabric</b>, wood, glass",
     "masked call and text, dishwasher claim"),
    ("Boomerang Stick On", "$25 / 24", "$1.04",
     "laptops, phones, <b>water bottles</b>",
     "5-year weathering, free lifetime plan; clothing needs their Iron On"),
    ("Roam Smart QR", "$14.99 / 12", "$1.25",
     "hard clean surfaces; <b>explicitly not fabric</b>",
     "anonymous message plus what3words to 3 m"),
    ("SeQR Lost Item Labels", "$9.99 / 6", "$1.67",
     "wallet, laptop, phone, AirPods", "anonymous messaging, no subscription"),
    ("Pebblebee Link", "$8.99 / 5", "$1.80",
     "<b>water bottles</b>, lunchboxes, books",
     "dishwasher safe, no battery, finder needs no signup"),
    ("If Found", "\u00a314.99 / 5", "\u00a33.00", "multi-purpose, IP67",
     "email, SMS or WhatsApp to owner"),
    ("ReturnMe label tags", "$10.99 / 2", "$5.50",
     "phones, tablets, laptops, passports", "24/7 recovery service"),
]

# Dumb printed QR, no notification service included. Strong Asset Tags.
DUMB_QR = [(100, 1.55), (250, 1.25), (500, 0.89), (1_000, 0.79)]
DUMB_QR_CHEAPEST = (500, 0.65)  # indoor polyester tier

# Student-founded direct rivals
RIVALS = [
    ("Papertags", "University of Virginia", "$2.50 per sticker, 900+ sold",
     "2\u2033 \u00d7 2\u2033, NFC-enabled, customisable with a logo", True),
    ("Beacon Tags", "Washington University in St. Louis",
     "free QR labels given to students",
     "reported by KSDK; page returned HTTP 403, so unconfirmed", False),
]

# ------------------------------------------------------------- on-metal NFC -

# Seritag 29 mm on-metal NTAG213, ex VAT
ONMETAL = [(10, 1.06), (100, 0.90), (500, 0.85), (1_000, 0.81)]
ONMETAL_SPEC = {"thickness_mm": 0.32, "chip_mm": 0.75, "read_mm": "21\u201325",
                "temp": "\u221215 to +60\u00b0C"}

# ---------------------------------------------------------- laundry-grade ---

LAUNDRY = [
    ("RFIDSU PPS button NFC", "NTAG213, 15 mm disc, 3 mm thick",
     "~200 industrial wash cycles, \u221230 to +200\u00b0C", "quote only"),
    ("Avery Dennison AD LoG PFL", "sew-in printed fabric, UHF ISO18000-63",
     "designed for 50 home washes; 100% pass at 40\u00b0C over 50 cycles",
     "business direct, no price"),
    ("SCIVAS woven NFC", "NTAG213/215/216 plus dynamic QR",
     "&ldquo;several domestic wash cycles&rdquo;, vendor wording",
     "$0.11&ndash;0.95, MOQ 100"),
]

# ------------------------------------------------------------ 3M adhesives --

# product, substrates, cure to full strength, water
# NOTE: the 3M PDFs would not fetch. These values come from search-indexed
# copies of 3M's own technical datasheets, so they are consistent across three
# products but were NOT read in the primary document. Graded accordingly, and
# the report says so rather than implying a datasheet was opened.
ADHESIVES = [
    ("3M 300LSE", "low-surface-energy plastics, PP, powder coat, stainless",
     "<b>72 hours</b> to full bond", "100 h immersion, no appreciable loss"),
    ("3M 468MP", "stainless, aluminium, glass, ABS, PVC, PC",
     "24 h to specified, <b>72 h dwell</b>", "100 h immersion, no appreciable loss"),
    ("3M 9471LE", "ABS, PP, stainless \u2014 peel rises 7.7\u21928.6 N/cm",
     "<b>72 hours</b>", "100 h immersion, no appreciable effect"),
]
ADHESIVES_GRADE = "unverified"

# Avery Dennison publishes two grades; the contrast matters for fabric claims.
FABRIC_WASH = [("AD LoG PFL", 50, "tested, 100% pass at 40\u00b0C"),
               ("AD TexTrace Durable PFL", 11, "intended 10\u201312 home cycles")]

SOURCES.update({
    "papertags": ("UVA students reinventing how lost items find their way home",
                  "McIntire School, University of Virginia",
                  "https://experience.mcintire.virginia.edu/news/"
                  "uva-students-reinventing-lost-items-find-way-home/",
                  "news", "2026"),
    "letstrack": ("Label sticker tag", "Letstrack",
                  "https://shop.letstrack.com/products/label-sticker-tag",
                  "vendor", "2026"),
    "boomerang_stick": ("The Stick On", "Boomerang",
                        "https://theboomerangtag.com/products/the-stick-on",
                        "vendor", "2026"),
    "roam": ("Roam smart QR sticker", "Roam",
             "https://roamsmarttracker.com/products/roam-smart-qr-sticker",
             "vendor", "2026"),
    "seqr": ("Lost item labels", "SeQR",
             "https://www.seqrcontact.com/products/lost-item-labels",
             "vendor", "2026"),
    "pebblebee_link": ("Link labels", "Pebblebee",
                       "https://pebblebee.com/products/link-labels",
                       "vendor", "2026"),
    "iffound": ("If Found products and how it works", "If Found",
                "https://iffound.app/products/", "vendor", "2026"),
    "strongtags": ("QR code asset labels", "Strong Asset Tags",
                   "https://strongassettags.com/products/qr-code-asset-labels",
                   "vendor", "2026"),
    "seritag": ("29 mm on-metal NTAG213", "Seritag",
                "https://seritag.com/nfc-tags/29mm-onmetal-ntag213",
                "vendor", "2026"),
    "rfidsu": ("PPS button NFC laundry tags", "RFIDSU",
               "https://rfidsu.com/rfid-laundry-tags/"
               "pps-button-nfc-laundry-tags", "vendor", "2026"),
    "avdenn": ("AD LoG PFL product information sheet", "Avery Dennison",
               "https://rfid.averydennison.com/content/dam/rfid/en/products/"
               "textrace/info-sheets/AD-LoG-PFL-Product-Information-Sheet.pdf",
               "vendor", "2026"),
    "mmm300": ("300LSE technical datasheet", "3M",
               "https://technicaldatasheets.3m.com/en_US?pif=000045",
               "vendor", "2026"),
    "mmm468": ("468MP adhesive transfer tape datasheet", "3M",
               "https://multimedia.3m.com/mws/media/1581295O/"
               "3m-adhesive-transfer-tape-468mp.pdf", "vendor", "2026"),
})

UNREACHABLE += ["Beacon Tags / KSDK WashU article (HTTP 403)",
                "Amazon marketplace listings (pages inaccessible)",
                "3M published minimum bend radius (none found)"]
