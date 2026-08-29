#!/usr/bin/env python3
"""Build the covert-marking feasibility memo.

    python3 research/build_marking_memo.py

Writes research/covert-marking-feasibility.html. Self-contained, no assets.
Data is inline because this memo is short and single-purpose; the two larger
reports keep their figures in dedicated data modules.
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import charts as C  # noqa: E402
from charts import Bar, Effect  # noqa: E402
from shell import REPORTS, Doc  # noqa: E402

OUT = REPORTS / "covert-marking-feasibility.html"

S = {  # key: (title, org, url, kind, year)
    "cop_tool": ("Crime Reduction Toolkit (82 rated interventions)",
                 "UK College of Policing",
                 "https://www.college.police.uk/research/crime-reduction-toolkit",
                 "official", "2026"),
    "cop_tag": ("Crime Reduction Toolkit — Retail tagging to prevent shop theft",
                "UK College of Policing",
                "https://www.college.police.uk/research/crime-reduction-toolkit/"
                "retail-tagging-prevent-shop-theft", "official", "2017"),
    "cop_scp": ("Interventions — situational crime prevention (neighbourhood crime)",
                "UK College of Policing",
                "https://www.college.police.uk/guidance/neighbourhood-crime/"
                "interventions-situational-crime-prevention", "official", "2022"),
    "nz": ("Does Chemical Property Marking Deter Burglary? Results from a New Danish "
           "Experiment (Cambridge Journal of Evidence-Based Policing 6:226)",
           "Kyvsgaard, Ribe & Sorensen",
           "https://pmc.ncbi.nlm.nih.gov/articles/PMC9762862/", "academic", "2022"),
    "dk": ("Rapport om usynlig mærkning (invisible marking evaluation)",
           "Danish Ministry of Justice",
           "https://www.justitsministeriet.dk/wp-content/uploads/2017/01/"
           "rapport_om_usynlig_maerkning.pdf", "official", "2017"),
    "laycock": ("Property Marking: A Deterrent to Domestic Burglary? (Crime Prevention "
                "Unit Paper 3)", "Laycock, UK Home Office",
                "https://popcenter.asu.edu/sites/g/files/litvpz3631/files/problems/"
                "burglary_home/PDFs/Laycock_1985.pdf", "official", "1985"),
    "chainey": ("Evaluating the effectiveness of forensic marking (Security Journal)",
                "Chainey",
                "https://link.springer.com/article/10.1057/s41284-021-00308-z",
                "academic", "2021"),
    "ptsa": ("Fluorescent silica nanoparticle anti-counterfeiting ink (Materials 13)",
             "Wuhan University",
             "https://pmc.ncbi.nlm.nih.gov/articles/PMC7560414/", "academic", "2020"),
    "ucnp": ("Quantum yield of upconverting NaYF4:Yb,Er (Nanoscale)",
             "Royal Society of Chemistry",
             "https://pubs.rsc.org/en/content/articlelanding/2017/nr/c7nr02449e",
             "academic", "2017"),
    "dna": ("DNA-based molecular tagging: a review (Nature Communications)",
            "Nature Communications",
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC10539344/", "academic", "2023"),
    "sw_shop": ("SmartWater Home / Sole Trader pack", "SmartWater (DeterTech)",
                "https://shop.smartwater.com/shop/home-sole-trader-pack/",
                "vendor", "2026"),
    "sw_sds": ("SmartWater safety data sheet", "SmartWater Technology Research Ltd",
               "https://media.dustin.eu/media/d200001004272750/"
               "dna-m%C3%A4rkning-smartwater-cykelcrossatv-document.pdf",
               "vendor", "2017"),
    "sdna": ("SelectaDNA frequently asked questions", "Selectamark",
             "https://www.selectadna.co.uk/faqs", "vendor", "2026"),
    "sdna_kit": ("SelectaDNA tools and equipment kit", "Selectamark",
                 "https://www.selectadna.co.uk/dna-asset-marking/"
                 "selectadna-tools-and-equipment-kit", "vendor", "2026"),
    "datadot": ("DataDot for schools", "DataDot Technology",
                "https://www.datadotdna.com/schools/", "vendor", "2026"),
    "microtrace": ("Microtaggant identification particles", "Microtrace Solutions",
                   "https://www.microtracesolutions.com/technologies/core-technologies/"
                   "microtaggant-identification-particles", "vendor", "2026"),
    "usda": ("Microtaggant marking trials (technical report 9624-1302)",
             "USDA Forest Service",
             "https://www.fs.usda.gov/t-d/pubs/pdf/96241302.pdf", "official", "1996"),
    "sirchie": ("UV700 invisible ink safety data sheet", "Sirchie",
                "https://www.sirchie.com/media/resourcecenter/item/u/v/uv700_4.pdf",
                "vendor", "2016"),
    "niosh": ("General Safe Practices for Working with Engineered Nanomaterials",
              "US NIOSH", "https://www.cdc.gov/niosh/docs/2012-147/pdfs/2012-147.pdf",
              "official", "2012"),
    "fda": ("UV wands can give unsafe levels of radiation", "US FDA",
            "https://www.fda.gov/medical-devices/safety-communications/"
            "do-not-use-ultraviolet-uv-wands-give-unsafe-levels-radiation-"
            "fda-safety-communication", "official", "2022"),
    "phone": ("Smartphones as near-infrared detectors: a review",
              "PMC", "https://pmc.ncbi.nlm.nih.gov/articles/PMC7982329/",
              "academic", "2021"),
    "cpsc": ("FHSA requirements for hazardous substances", "US CPSC",
             "https://www.cpsc.gov/Business--Manufacturing/Business-Education/"
             "Business-Guidance/FHSA-Requirements", "official", "2026"),
    "rohs": ("RoHS Directive consolidated text", "European Union",
             "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=OJ:L_202401416",
             "official", "2024"),
    "psni": ("Preventing bicycle and e-bike theft", "Police Service of Northern Ireland",
             "https://www.psni.police.uk/preventing-bicycle-and-e-bike-theft",
             "official", "2026"),
    "polscot": ("Bike owners encouraged to register bikes on national database",
                "Police Scotland",
                "https://www.scotland.police.uk/what-s-happening/news/2023/december/"
                "bike-owners-across-scotland-encouraged-to-register-bikes-on-national-"
                "database/", "official", "2023"),
    "iu": ("Bike theft survey results", "Indiana University",
           "https://transportation.indiana.edu/about-us/news/bike-theft-survey.html",
           "academic", "2024"),
    "opid": ("Evaluation of Operation Identification, Volume 2 (NCJ 28908)",
             "US Department of Justice / National Institute of Justice",
             "https://www.ncjrs.gov/pdffiles1/Digitization/28908NCJRS.pdf",
             "official", "1975"),
    "sbd": ("Selectamark accredited product listing (PAS 820:2012)",
            "Secured by Design / Police Crime Prevention Initiatives",
            "https://www.securedbydesign.com/member-companies/product-category-search/"
            "product?id=0011i00000JpvkQAAR", "official", "2026"),
    "cdicsc": ("International Chemical Safety Card 0404 — cadmium sulfide",
               "IPCS / WHO / ILO",
               "https://www.inchem.org/documents/icsc/icsc/eics0404.htm",
               "official", "2018"),
    "rhod": ("Rhodamine B — aggregated GHS classifications",
             "US National Institutes of Health, PubChem",
             "https://pubchem.ncbi.nlm.nih.gov/compound/Rhodamine-B",
             "official", "2026"),
}
LEAD = {"cop_tool", "cop_tag", "nz"}


def cite(*keys: str, extra: str = "") -> str:
    bits = []
    for k in keys:
        t, org, url, kind, yr = S[k]
        tick = " &#10003;" if k in LEAD else ""
        bits.append(f'<a href="{url}">{org}, <i>{t}</i></a> ({yr}){tick}')
    s = "<b>Source:</b> " + "; ".join(bits) + "."
    return f"{s} {extra}" if extra else s


def chip(k: str) -> str:
    m = {"yes": ("c-strong", "Achievable"), "hard": ("c-weak", "Hard"),
         "no": ("c-none", "Not simultaneously"), "part": ("c-mod", "Partly"),
         "official": ("c-off", "Official"), "academic": ("c-aca", "Peer-reviewed"),
         "vendor": ("c-ven", "Vendor claim"), "null": ("c-none", "Null result"),
         "weak": ("c-weak", "Weak design")}
    cls, txt = m[k]
    return f'<span class="chip {cls}">{txt}</span>'


d = Doc()

MASTHEAD = """
<div class="masthead">
  <div class="kicker">Feasibility Memo &middot; Property Marking &middot; Revised</div>
  <h1>Feasible &mdash; and stronger once you stop hiding it from the thief</h1>
  <div class="standfirst">An assessment of property marking against five stated
  requirements: unobtrusive, durable, safe, easy to apply, easy to detect. The chemistry
  is largely solved and sold commercially. The evidence that a <i>covert</i> mark reduces
  theft or recovers property is weak to null &mdash; but the requirement was
  unobtrusiveness, not concealment from the offender, and that distinction rescues the
  idea.</div>
  <div class="meta">
    <div><b>Question</b>Is a marking ink feasible?</div>
    <div><b>Chemistry</b>Yes; already on sale at ~&pound;0.60/item</div>
    <div><b>Decisive blocker</b>Nobody checks &mdash; section 4</div>
    <div><b>Revised</b>28 August 2026</div>
  </div>
</div>"""

# ================================================================= VERDICT ==

d.h2("Verdict", "verdict")
d.p("Every individual requirement is achievable, and products meeting most of them have "
    "been sold to police forces for over twenty years. The idea is sound. What follows is "
    "an argument about <i>which half of it to build</i>, and one blocker that no "
    "formulation can fix.", "lede")

d.box("insight", "Scope correction, and it matters a lot",
      "<p>This memo originally read requirement 1 &mdash; \u201ccannot be seen easily\u201d "
      "\u2014 as concealment from the thief. That was wrong. The requirement is that the "
      "mark be <b>unobtrusive</b>: it should not deface a laptop lid or a bike frame. "
      "Whether an offender can discover it is explicitly not a constraint.</p>"
      "<p>That reading change is worth more than it sounds, because it removes the single "
      "biggest objection to the design. <b>The only mechanism in the entire evaluation "
      "literature with a measured effect is visible deterrence.</b> If the offender is "
      "allowed to know the item is marked, you can use that mechanism instead of fighting "
      "it \u2014 and you can attack resale value, which is what every successful "
      "intervention in this field has actually done.</p>")

d.keys([
    ("Conspicuous \u003e covert", "The only systematic review of an analogous "
     "intervention found <b>visible tags outperform hidden ones</b>. Being seen is a "
     "feature, not a defect.", "College of Policing \u2713"),
    ("p = 0.495", "The largest randomised trial of chemical property marking "
     "(12,000 households) found <b>no significant effect</b>. Marking alone does not work.",
     "North Zealand RCT \u2713"),
    ("0", "Items returned to owners in the classic Home Office marking trial, despite a "
     "40% fall in burglary. None of 21 detections involved marked goods.",
     "Laycock, Home Office 1985"),
    ("36% \u2192 10%", "Bicycles registered versus recovered at Indiana University. "
     "The mark was never the constraint. <b>Nobody checking it</b> was.",
     "IU survey, 2024"),
])

d.box("warn", "What survives the correction, and what does not",
      "<p><b>No longer a problem:</b> covertness versus deterrence. You can now ship an "
      "unobtrusive permanent mark <i>plus</i> an overt indication that the item is marked, "
      "which is exactly what the evidence supports and exactly what SmartWater and "
      "SelectaDNA already do with their warning stickers.</p>"
      "<p><b>Still a problem \u2014 chemistry:</b> requirement 2 fights requirement 4. A "
      "mark that survives washing, solvents and abrasion must be covalently bonded, driven "
      "into the fibre, or locked in a highly crosslinked film. All need substrate-specific "
      "pretreatment. A one-step pen that goes on anything and rubs off nothing remains an "
      "engineering contradiction, and it gets marginally harder when the offender knows "
      "where to scrub.</p>"
      "<p><b>Still the decisive problem \u2014 nobody checks.</b> This is unaffected by the "
      "correction. A mark only recovers property if somebody reads it, and no published "
      "measurement of real-world checking rates exists anywhere. Section 4.</p>")

d.box("win", "The one-sentence version",
      "<p>Build the mark so it is <b>unobtrusive but announced</b>, aim it at destroying "
      "resale value rather than at forensic identification, and spend most of your effort "
      "on the thing nobody builds \u2014 making somebody actually check.</p>")

# ============================================================ REQUIREMENTS ==

d.h2("1. Requirement-by-requirement", "reqs")

d.table(
    ["Requirement", "Feasible?", "Why", "Best existing approach"],
    [["<b>1. Unobtrusive</b><br><small>not concealment from the thief</small>",
      chip("yes"),
      "Solved, and now the easiest requirement of the five. A colourless fluorophore in a "
      "clear binder leaves no visible trace under normal light on any of your substrates. "
      "Because hiding it from the offender is <i>not</i> required, the cheap option is "
      "back on the table: an ordinary UV-fluorescent dye is entirely adequate, and you no "
      "longer need upconversion or a laser reader.",
      "UV-fluorescent dye in a clear water-based binder"],
     ["<b>2. Not easily removed</b>", chip("hard"),
      "The hard one. Surface deposits are mechanically weak and solvent-accessible. "
      "Durability requires covalent coupling or fibre penetration, which requires "
      "substrate-specific pretreatment.",
      "Silane coupling on glass/anodised aluminium; polymer grafting into textile fibre"],
     ["<b>3. Harmless to humans</b>", chip("part"),
      "Achievable with a water-based binder, but not automatic. The market-leading "
      "forensic liquid contains a Category 1 skin sensitiser, and a common UV marker pen "
      "is flammable and causes serious eye damage. Nanoparticle sprays add inhalation "
      "duties.",
      "Water-based acrylic or polyurethane emulsion, dauber not aerosol"],
     ["<b>4. Simple to apply</b>", chip("yes"),
      "Trivially, if you accept a surface film. Directly in tension with requirement 2 "
      "\u2014 see above.",
      "Pen, dauber or brush"],
     ["<b>5. Easily detectable</b>", chip("part"),
      "A 365 nm torch reveals UV fluorescence, and an unmodified phone camera can see the "
      "<i>visible</i> emission. But detection only proves a mark exists; reading an "
      "identity needs a microscope, a database lookup or a laboratory.",
      "UV torch to screen, microdot plus registry to identify"]],
    title="The five requirements assessed",
    sub="Individually each is solvable. The conflict is between 2 and 4, and it is "
        "physical rather than formulational.",
    source=cite("ptsa", "ucnp", "sw_sds", "sirchie", "phone"))

d.box("caveat", "Why requirement 2 is genuinely hard",
      "<p>Adhesion comes from three things: a cohesive crosslinked polymer network, "
      "chemical or mechanical coupling into the substrate, and immobilisation of the "
      "taggant inside that network. On <b>glass or anodised aluminium</b> silanes can "
      "condense to real Si\u2013O\u2013M bonds \u2014 but laptop lids are usually "
      "clear-coated or oily, which defeats coupling. On <b>carbon-fibre and painted "
      "frames</b> you are bonding to a clearcoat that itself delaminates. On <b>nylon and "
      "polyester</b> a surface film simply abrades and surfactant-extracts; durability "
      "needs dyeing-like penetration or grafting onto the fibre, typically with heat or "
      "solvent. On <b>polycarbonate</b> the surface energy is low and solvents cause "
      "stress cracking.</p>"
      "<p>Etching or roughening would fix adhesion, and simultaneously breaks "
      "requirements 1 and 3 by visibly damaging the item.</p>")

# ============================================================== CHEMISTRY ===

d.h2("2. What the chemistry can actually do", "chem")
d.p("With concealment from the offender off the requirement list, your reference case "
    "&mdash; ordinary UV ink &mdash; goes from being the weakest option to being the "
    "right one. The objection to it was always that a five-pound 365 nm torch reveals it "
    "to a thief as easily as to you. If that does not matter, UV fluorescence wins on "
    "every remaining axis: cheapest to make, simplest to apply, and readable with hardware "
    "the whole campus already owns.")

d.p("What still matters chemically is <b>durability</b>. The single most useful "
    "intervention available to you is encapsulating the dye rather than dissolving it, "
    "which addresses both photobleaching and solvent extraction at once.")

d.fig(
    C.hbar([Bar("Free dye in ink", 73, color=C.NEGATIVE),
            Bar("Dye encapsulated in silica nanoparticles", 13.5, color=C.POSITIVE)],
           unit="%", dp=1, label_w=280, vmax=80),
    "Fluorescence lost after one hour of UV exposure",
    "Intensity loss for a pyrene-based security dye after two 30-minute exposures at "
    "354 nm. Encapsulation cuts photobleaching more than fivefold, and the same "
    "encapsulation retained 92% of fluorescence after 240 hours in water.",
    cite("ptsa", extra="Tested on paper only. No wash or abrasion testing on the "
                       "substrates relevant here."))

d.table(
    ["Mechanism", "How it is read", "Covertness", "Practical problem"],
    [["<b>UV fluorescent dye</b><br><small>Stokes emission, ~365 nm excitation</small>",
      "Any UV torch; visible emission", "Low \u2014 any torch finds it",
      "Photobleaches, solvent- and detergent-soluble unless encapsulated"],
     ["<b>Upconverting phosphor</b><br><small>NaYF\u2084:Yb,Er, 980 nm excitation</small>",
      "980 nm laser diode", "<b>High</b> \u2014 no visible or UV cue",
      "Quantum yield only 0.6\u20132.1% for nanoparticles; needs a laser; phone "
      "cameras have infrared-blocking filters so cannot read it unmodified"],
     ["<b>Persistent phosphor</b><br><small>SrAl\u2082O\u2084:Eu,Dy afterglow</small>",
      "Charge with light, view in dark", "Low \u2014 glows visibly",
      "Hydrolyses in moisture; needs protective coating"],
     ["<b>SERS / Raman taggant</b>", "Handheld Raman spectrometer",
      "High", "Reader is roughly $21,000; signal ratios drift"],
     ["<b>Synthetic DNA</b>", "Swab, PCR, sequence",
      "High", "Laboratory turnaround; DNA degrades under UV, heat and humidity unless "
      "silica-encapsulated"],
     ["<b>Microtaggant / microdot</b><br><small>Layered coded particles, 20\u20131200 "
      "\u00b5m</small>", "UV torch to locate, microscope to read",
      "Medium", "Physically scrapeable; still needs a registry to mean anything"],
     ["<b>Elemental taggant</b>", "Handheld XRF",
      "High", "Reader is roughly $15,000\u201360,000"]],
    title="Candidate mechanisms, honestly compared",
    sub="The covertness column is now largely irrelevant to your brief \u2014 it is kept "
        "because it drives reader cost, which is not irrelevant. Read the last two columns "
        "together: the mechanisms that resist casual discovery all need instruments costing "
        "thousands, and you no longer need to pay that.",
    source=cite("ptsa", "ucnp", "dna", "microtrace", "phone"))

d.box("win", "The formulation to actually build",
      "<p><b>An encapsulated UV fluorophore in a clear, crosslinking water-based binder, "
      "applied by dauber.</b> Not upconversion, not DNA, not Raman. Those buy covertness "
      "you have now told me you do not need, and each one costs you either a "
      "$15,000\u201321,000 reader or a laboratory turnaround.</p>"
      "<p>The encapsulation is the part worth engineering. Dissolving a dye in a binder "
      "gives you something that photobleaches and washes out; locking the same dye inside "
      "silica nanoparticles cut UV-driven intensity loss from <b>73% to 13.5%</b> over an "
      "hour of exposure and retained <b>92%</b> of fluorescence after 240 hours immersed "
      "in water. That is a real, measured, replicable durability gain and it is the "
      "defensible technical contribution in this project.</p>"
      "<p>Read it with a 365 nm torch and an unmodified phone camera. Both are already in "
      "every pocket and every campus security office.</p>"
      + cite("ptsa", "phone"))

# =============================================================== EVIDENCE ===

d.h2("3. Does marking actually work? Read this before building", "evidence")
d.p("This is where the proposal runs into trouble. Property marking has been trialled "
    "since the 1970s, and the better the study design, the smaller the effect.")

d.fig(
    C.vbar([Bar("Treatment\n(kit + stickers)", 4.6, color=C.PALETTE[0]),
            Bar("Placebo\n(letter only)", 5.1, color=C.PALETTE[7]),
            Bar("Control\n(no contact)", 4.9, color=C.PALETTE[7])],
           unit="%", dp=1, height=290),
    "The largest randomised trial found nothing",
    "Percentage of previously burgled households burgled again within 15\u00bd months. "
    "12,000 households in North Zealand, Denmark, randomly assigned. Treatment versus "
    "control: <b>p = 0.495</b>. Placebo versus control: p = 0.682.",
    cite("nz", extra="Only 29% of the treatment group both registered and posted the "
                     "warning stickers, which the authors note limits the achievable "
                     "effect. A compliant-subgroup comparison gave p = 0.067 but is not "
                     "randomised and is subject to selection bias."))

d.table(
    ["Study", "Design", "Result", "Grade"],
    [["<b>North Zealand, Denmark</b><br><small>12,000 households</small>",
      "RCT with placebo arm",
      "Treatment 4.6% vs control 4.9%, <b>p=0.495</b>. No effect.", chip("null")],
     ["<b>Aarhus, Denmark</b><br><small>6,603 households</small>", "RCT",
      "Burglary 4.7% vs 6.2%, p=0.021 \u2014 but the effect was concentrated early and "
      "non-registrants also improved, suggesting chance or a Hawthorne effect. "
      "<b>Other theft: 1.4% vs 1.5%, p=0.983.</b>", chip("weak")],
     ["<b>South Wales</b><br><small>Home Office, Laycock 1985</small>",
      "Before/after, no external control",
      "40% fall in burglary \u2014 but accompanied by intense press and TV coverage, a "
      "Chief Constable's letter and door-to-door police visits. <b>Zero stolen goods "
      "returned. None of 21 detections involved marked goods.</b>", chip("weak")],
     ["<b>Huddinge, Sweden</b><br><small>Knutsson, ~3,500 homes</small>",
      "Participant vs non-participant",
      "<b>No effect on burglary or on clearance.</b>", chip("null")],
     ["<b>Operation ID, USA</b><br><small>Seattle and St Louis</small>",
      "Participant comparison, self-selected",
      "Participant burglary risk down 32.8%, but participation reached only about 7% in "
      "the best sector, the marking could not be separated from other programme "
      "activities, and <b>no appreciable recovery or return of property</b> was "
      "documented.", chip("weak")],
     ["<b>West Bromwich, England</b><br><small>345 kits, matched controls</small>",
      "Quasi-experiment with displacement zones",
      "82% relative reduction in the first six months, <b>back to baseline by twelve</b>. "
      "Treatment zone fell 25\u21925 while the adjacent displacement zone rose 25\u219231.",
      chip("weak")]],
    title="Every evaluation of property marking that could be found",
    sub="Note the pattern: randomised designs return null results; positive results come "
        "from designs without controls, and always from packages that included publicity "
        "and signage alongside the marking.",
    source=cite("nz", "dk", "laycock", "chainey"))

d.fig(
    C.effects([
        Effect("No control area \u2014 South Wales 1985", -40),
        Effect("Self-selected sample \u2014 Operation ID", -32.8),
        Effect("Matched controls, 6 months \u2014 W. Bromwich", -82),
        Effect("Matched controls, 12 months \u2014 W. Bromwich", 0),
        Effect("Randomised \u2014 Aarhus, burglary", -24),
        Effect("Randomised \u2014 Aarhus, other theft", -7),
        Effect("Randomised + placebo \u2014 North Zealand", -6),
        Effect("Participant vs non-participant \u2014 Sweden", 0),
    ], vmin=-90, vmax=20, label_w=290),
    "The stronger the study design, the smaller the effect",
    "Reported change in the target crime for each evaluation. This is a display of "
    "heterogeneous headline figures across incompatible designs, not a meta-analysis "
    "\u2014 the point is the gradient, not any individual bar. Only the two randomised "
    "trials support causal inference, and only one of those reached significance.",
    cite("nz", "dk", "laycock", "chainey",
         extra="West Bromwich at 12 months and Sweden are plotted at zero because both "
               "reported no sustained or detectable effect. The Aarhus and North Zealand "
               "bars are relative differences derived from the published prevalence rates; "
               "the North Zealand difference was not statistically significant (p=0.495)."))

d.box("warn", "The recovery evidence is worse than the deterrence evidence",
      "<p>Deterrence at least produces the occasional positive result. Recovery \u2014 the "
      "thing your ink is actually for \u2014 produces almost nothing:</p>"
      "<ul>"
      "<li><b>South Wales, Home Office 1985:</b> zero stolen goods returned to owners. Of "
      "21 detections in the trial period, none involved marked goods. Only four marked "
      "items were taken in participant burglaries at all.</li>"
      "<li><b>Operation Identification, United States:</b> the multi-site evaluation found "
      "participant burglary risk down 32.8%, but participation reached only about 7% in the "
      "best sector, the contribution of marking could not be separated from the other "
      "programme activities, and there was <b>no documented appreciable recovery or return "
      "of property</b> attributable to the scheme. Property-recovery measures showed no "
      "significant results.</li>"
      "<li><b>Sweden:</b> no effect on burglary <i>or on clearance</i>.</li>"
      "</ul>"
      "<p>Three separate national programmes, decades apart, all failed at the specific job "
      "you are designing for.</p>"
      + cite("laycock", "opid", "nz"))

d.box("win", "The sticker finding is now your best asset, not your problem",
      "<p>The Danish review states it directly: prior research measures <b>warning "
      "stickers</b>, not the marks themselves \u2014 and there is no reason to expect "
      "deterrence if offenders are unaware the property is marked. Under the original "
      "covert reading, that was fatal: an invisible mark deters nobody.</p>"
      "<p>Under the corrected reading it is the opposite. <b>The one component with any "
      "measured effect is the component you are now allowed to include.</b> Ship the "
      "unobtrusive permanent mark <i>and</i> an overt, tamper-evident indication that the "
      "item carries it. That is not a compromise of the design; it is the design the "
      "evidence actually supports.</p>"
      "<p>Two cautions. The measured sticker effects were short-lived, faded within twelve "
      "months, and in West Bromwich displaced theft to the adjacent area. And the "
      "retail-tagging review's finding that conspicuous beats inconspicuous is about "
      "<i>retail</i> tags with alarms attached. Neither result licenses a strong claim; "
      "both point the same direction.</p>"
      + cite("nz", "chainey", "cop_tag"))

d.p("For calibration: the College of Policing rates 82 interventions in its Crime "
    "Reduction Toolkit, and property marking is <b>not one of them</b> \u2014 there is no "
    "systematic review of sufficient quality to rate. The nearest rated analogue is retail "
    "tagging, which comes out as <b>\u201cmixed findings\u201d on strong evidence</b>: no "
    "statistically significant overall effect on crime. And crucially, that review found "
    "<b>conspicuous tags outperformed inconspicuous ones</b>.")
d.raw(f'<p class="srcnote">{cite("cop_tool", "cop_tag", "cop_scp")}</p>')

# ================================================================ CHECKING ==

d.h2("4. The blocker nobody costs in: who checks?", "checking")
d.p("Suppose the ink is perfect. Invisible, indestructible, harmless, one-swipe, readable "
    "with a two-pound torch. It still does nothing unless somebody looks.")

d.fig(
    C.funnel([
        ("Item is marked", 100.0, "your product works"),
        ("Item is stolen and later encountered", 100.0, "by police, a buyer, a resale platform"),
        ("Someone thinks to check for a mark", 0.0, "no published rate exists, anywhere"),
        ("Mark is read and matched to a registry", 0.0, "requires reader plus database"),
        ("Owner is contacted and item returned", 0.0, "the only outcome that matters"),
    ], title=""),
    "The chain your ink sits at the start of",
    "The bars after the second stage are drawn at zero because <b>no published measurement "
    "of real-world checking rates could be located</b> for police property rooms, "
    "pawnbrokers, second-hand dealers or online marketplaces. That is an absence of "
    "evidence, not a measured zero \u2014 but it is the single most decision-relevant fact "
    "in this memo.",
    cite("psni", "polscot", "iu",
         extra="What does exist: Police Scotland publicised <b>four</b> bicycles reunited "
               "via a marking database; one Leicestershire station runs recovered property "
               "under UV in a dedicated room. Both are case reports without denominators."))

d.box("insight", "You already have the decisive data point from earlier research",
      "<p>Indiana University found that <b>36% of stolen bicycles were registered</b> and "
      "<b>10% were recovered</b>. Registration was not the constraint. Nobody checking the "
      "registry was the constraint.</p>"
      "<p>Motor vehicles recover at 56% of value and everything else at about 8% \u2014 not "
      "because cars are better marked, but because a VIN is checked <i>automatically and "
      "routinely</i> at registration, insurance, resale and traffic stop. The mark is the "
      "easy half. The mandatory, habitual check is the half that actually produces "
      "recovery, and it is institutional rather than chemical.</p>"
      + cite("iu"))

# ================================================================== SAFETY ==

d.h2("5. Safety and regulation are not a formality", "safety")
d.ul([
    "<b>\u2018Harmless\u2019 is a regulated claim.</b> Under the US Federal Hazardous "
    "Substances Act, deceptive \u2018safe\u2019 or \u2018harmless\u2019 labelling is "
    "prohibited outright, and any irritant or strong sensitiser triggers mandatory "
    "labelling. In the EU, CLP requires classification and labelling before you may place "
    "a chemical on the market.",
    "<b>The market leader is not harmless.</b> The SmartWater safety data sheet lists "
    "benzisothiazolinone at 0.030% \u2014 a <b>Category 1 skin sensitiser (H317)</b>, with "
    "an EUH208 allergy warning, and recommends gloves and eye protection.",
    "<b>A common UV marker pen is worse.</b> The Sirchie UV700 data sheet classifies it as "
    "highly flammable, harmful if swallowed, a skin irritant, causing <b>serious eye "
    "damage</b>, and causing drowsiness. Solvent-based invisible inks are not benign.",
    "<b>Avoid an aerosol or spray format.</b> NIOSH guidance treats spraying and sonicating "
    "engineered nanomaterials as emission tasks requiring containment and local exhaust; "
    "liquid suspensions applied by pen or dauber have a far lower exposure profile and a "
    "far lighter regulatory burden.",
    "<b>Avoid cadmium quantum dots outright.</b> The EU RoHS general limit is 0.01% by "
    "weight in any homogeneous material, and the quantum-dot exemptions are narrow and "
    "display-specific. The international chemical safety card for cadmium sulfide "
    "classifies it as <b>carcinogenic to humans</b>, warns that harmful airborne "
    "concentrations are reached quickly once the powder is dispersed, and the EU "
    "occupational limit is 0.001 mg/m\u00b3 inhalable. That is not a student-handled "
    "consumer product.",
    "<b>Check your fluorophore, not just your binder.</b> Rhodamine B, a common "
    "fluorescent dye, carries aggregated industry classifications of <b>H318 serious eye "
    "damage</b> (98.2% of 2,557 reports) and long-lasting aquatic toxicity. Fluorescence "
    "and benignity are unrelated properties.",
    "<b>UV torches carry their own risk.</b> The FDA measured some handheld UV-C wands "
    "emitting up to 3,000 times the ICNIRP exposure limit at two inches. Specify 365 nm "
    "UV-A, never UV-C, and say so in your documentation.",
])
d.raw(f'<p class="srcnote">{cite("cpsc", "sw_sds", "sirchie", "niosh", "rohs", "cdicsc", "rhod", "fda")}</p>')

# ================================================================ EXISTING ==

d.h2("6. What already exists, and what it costs", "existing")
d.p("Before building, note that the invisible-plus-UV-plus-database product has been on "
    "sale for two decades.")

d.box("caveat", "On the durability claims you will see quoted",
      "<p>Selectamark's products are listed by Secured by Design, the UK police security "
      "accreditation body, as tested to PAS 820:2012 with artificial weathering rated "
      "Grade A (over five years) under a UKAS-accredited laboratory certificate. That is a "
      "real accreditation and worth more than a marketing page.</p>"
      "<p>Two caveats before you treat it as settled. It is <b>commissioned artificial "
      "weathering</b>, not independent field testing against deliberate removal by someone "
      "who knows the mark is there. And a security-product accreditation is not a "
      "toxicological clearance \u2014 the two say nothing about each other. "
      f"{cite('sbd')}</p>")

d.table(
    ["Product", "Mechanism", "How it is read", "Price", "Identifier"],
    [["<b>SmartWater</b>", "Aqueous polymer emulsion carrying a combination of trace "
      "elements or nucleic acids, plus a UV indicator",
      "UV torch screens; laboratory analysis confirms the chemical code",
      "\u00a359.50 for 3 ml, marks 80\u2013100 items (~\u00a30.60\u20130.74 each)",
      "Code tied to the <b>owner</b>, not the item"],
     ["<b>SelectaDNA</b>", "Water-based UV adhesive containing synthetic DNA plus hundreds "
      "of 1 mm microdots",
      "UV torch locates; microscope reads the dot; DNA needs a laboratory",
      "\u00a359.50 for up to 50 items (~\u00a31.19 each); \u00a3765 for 1,000",
      "Customer registration code, not per-item"],
     ["<b>DataDot</b>", "Thousands of coded polymer microdots in UV adhesive",
      "UV torch plus magnifier", "AU$69.95 for 3,000 dots",
      "Coded to a database record"],
     ["<b>Microtaggant</b>", "Layered colour-coded particles, 20\u20131200 \u00b5m, "
      "optionally UV, infrared or magnetic",
      "100\u00d7 pocket microscope reads the colour sequence",
      "Historic 1996 USDA trial: $145 per 8 oz, $15 microscope",
      "Scheme or batch level"],
     ["<b>Ordinary UV pen</b>", "Solvent-based fluorescent dye",
      "UV torch", "A few pounds",
      "<b>None</b> \u2014 proves a mark exists, proves no ownership"]],
    title="The incumbent products",
    sub="Note the last column. None of these gives a genuinely unique per-item identifier "
        "verifiable in the field; they establish membership of a scheme and then rely on a "
        "database lookup or a laboratory.",
    source=cite("sw_shop", "sdna", "sdna_kit", "datadot", "microtrace", "usda", "sirchie",
                extra="Prices and durability claims are vendor-published. No independent "
                      "wash, abrasion or solvent testing of any of these products could be "
                      "located."))

# ============================================================== ALTERNATIVE =

d.h2("7. What to build", "instead")
d.p("The research is not telling you the idea is bad. It is telling you that the "
    "chemistry half is already solved and commoditised, and that the mechanism you should "
    "be aiming at is not forensic identification but <b>resale devaluation</b> \u2014 the "
    "one lever that has worked every time it has been tried.")

d.box("insight", "Aim at disposability, because that is what actually works",
      "<p>Three independent natural experiments from the earlier research in this project "
      "share one mechanism, and none of them is forensic:</p>"
      "<ul>"
      "<li>Apple made stolen iPhones <b>unusable</b> \u2192 iPhone robberies fell 38% in "
      "San Francisco while Samsung thefts rose 12%.</li>"
      "<li>UW-Madison made stolen textbooks <b>hard to sell</b> \u2192 textbook theft fell "
      "86%.</li>"
      "<li>The UK made stolen metal <b>hard to sell for cash</b> \u2192 metal theft roughly "
      "halved.</li>"
      "</ul>"
      "<p>None prevented a theft attempt. All three removed the buyer. A mark the offender "
      "<i>can</i> see does exactly this: a permanent, visibly institution-owned item is "
      "worth less to a buyer, and the offender knows it before taking it. A mark the "
      "offender cannot see does none of it. <b>Your clarification moves the product from "
      "the mechanism that fails to the mechanism that works.</b></p>")

d.table(
    ["Keep", "Change", "Because"],
    [["The insight that identity enables recovery",
      "Treat the <b>check</b> as the product, not the mark",
      "Vehicles recover at 56% of value and everything else at 8%; the difference is "
      "routine checking, not superior marking. Indiana: 36% registered, 10% recovered."],
     ["Marking as the identity layer",
      "Add an <b>overt, tamper-evident</b> indication that the item is marked",
      "The only measured effects in the literature come from visible warnings, and the "
      "retail-tagging review found conspicuous beats inconspicuous. You are now allowed "
      "this."],
     ["Permanence as a goal",
      "Reframe permanence as <b>devaluing resale</b> rather than enabling forensics",
      "Forensic identification has never been shown to recover property. Killing resale "
      "value has worked in three separate natural experiments."],
     ["Campus as the deployment context",
      "Exploit the <b>mandatory identity system and physical chokepoints</b> a campus "
      "already has",
      "Every student has an ID; every bike compound, gym, library and residence has a "
      "door. A campus can make checking habitual in a way a city cannot."],
     ["UV fluorescence",
      "Encapsulate the dye rather than dissolving it, and read it with a phone",
      "Encapsulation cut photobleaching from 73% to 13.5% and held 92% fluorescence after "
      "240 hours in water. Cheap, measurable, and defensible as an engineering result."],
     ["The hackathon timeframe",
      "Build the <b>registry and the scanning workflow</b>; buy the chemistry",
      "You cannot validate wash and abrasion durability across four substrates in a "
      "weekend, and a &pound;59.50 kit already marks 80\u2013100 items."]],
    title="A build plan that matches the evidence",
    source=cite("iu", "cop_tag", "ptsa", "nz"))

d.box("win", "The strongest version of your idea",
      "<p>Make the <b>check</b> free and automatic at the points where stolen campus "
      "property surfaces, and use marking only as the identity layer that makes the check "
      "possible.</p>"
      "<p>Concretely: mark items at enrolment with something cheap and covert; then put "
      "readers where recovered and resold property actually appears \u2014 the campus lost "
      "property office, the bike compound, the second-hand marketplace the students "
      "themselves use, campus security's found-property intake. The evidence in this memo "
      "says the mark alone changes nothing. A mark plus a habitual check is precisely the "
      "arrangement that makes stolen cars recover at 56%.</p>"
      "<p>That is also the honest pitch: <i>everyone builds the tag; nobody builds the "
      "scanner network, which is why 90% of stolen property is never returned.</i></p>")

# ============================================================== LIMITATIONS =

d.h2("Limitations of this memo", "limits")
d.ul([
    "<b>No independent durability testing exists</b> for any commercial forensic marking "
    "product that could be located. Vendor claims of five-year persistence and resistance "
    "to removal are unverified, in both directions \u2014 they may well be true.",
    "<b>The evaluation literature is about burglary</b>, mostly domestic, mostly in "
    "Denmark and the UK. No trial of property marking against campus opportunistic theft "
    "was found. It is possible marking performs differently there, though nothing suggests "
    "it would.",
    "<b>The Danish RCTs suffered low compliance</b> \u2014 29% and 32% posted stickers as "
    "instructed. A trial with full compliance might detect an effect the authors could not.",
    "<b>Absence of evidence on checking rates is not evidence of absence.</b> Police may "
    "check recovered property far more often than the published record shows; the point is "
    "that nobody has measured it, so a business case cannot assume it.",
    "<b>Chemistry figures are laboratory values.</b> The photobleaching and quantum-yield "
    "numbers come from controlled studies on paper or in dispersion, not from marked "
    "laptops or bicycles exposed to weather and handling.",
])

d.h2("Sources", "sources")
rows = []
for k, (t, org, url, kind, yr) in sorted(S.items(), key=lambda x: x[1][1]):
    tick = " &#10003;" if k in LEAD else ""
    rows.append([f"{org}{tick}", f'<a href="{url}">{t}</a>', yr, chip(kind)])
d.table(["Organisation", "Publication", "Year", "Type"], rows,
        title="Sources", sub=f"{len(S)} sources, all opened. A tick marks those the author "
                             "read personally to verify a load-bearing figure.",
        source="<b>Rebuild:</b> <code>python3 research/build_marking_memo.py</code>")

_m = (MASTHEAD.replace("__NSRC__", str(len(S))))
OUT.write_text(d.html("Covert property marking: feasibility assessment", _m),
               encoding="utf-8")
print(f"wrote {OUT} ({OUT.stat().st_size:,} bytes, {d.fig_n} figures, "
      f"{d.tab_n} tables, {len(S)} sources)")
