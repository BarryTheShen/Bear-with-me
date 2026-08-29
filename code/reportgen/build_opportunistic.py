#!/usr/bin/env python3
"""Build the self-contained HTML report on opportunistic (unattended) theft.

    python3 research/build_opportunistic.py

Writes research/opportunistic-theft-report.html — one file, no external assets,
no JavaScript. Companion to theft-and-property-loss-report.html.
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import charts as C  # noqa: E402
import data_opportunistic as D  # noqa: E402
from charts import Bar, Range  # noqa: E402
from shell import REPORTS, Doc  # noqa: E402

OUT = REPORTS / "opportunistic-theft-report.html"


def cite(*keys: str, extra: str = "") -> str:
    bits = []
    for k in keys:
        label, org, url, kind, year = D.SOURCES[k]
        tick = " &#10003;" if k in D.VERIFIED_BY_LEAD else ""
        bits.append(f'<a href="{url}">{org}, <i>{label}</i></a> ({year}){tick}')
    s = "<b>Source:</b> " + "; ".join(bits) + "."
    return f"{s} {extra}" if extra else s


def chip(kind: str) -> str:
    m = {"official": ("c-off", "Official"), "academic": ("c-aca", "Peer-reviewed"),
         "vendor": ("c-ven", "Vendor claim"), "news": ("c-none", "Press"),
         "direct": ("c-strong", "Direct measure"), "proxy": ("c-mod", "Proxy"),
         "est": ("c-weak", "Police estimate"), "qual": ("c-none", "Qualitative")}
    cls, txt = m[kind]
    return f'<span class="chip {cls}">{txt}</span>'


d = Doc()

MASTHEAD = """
<div class="masthead">
  <div class="kicker">Research Report II &middot; Opportunistic Theft</div>
  <h1>Theft of unattended property: how big is it, really?</h1>
  <div class="standfirst">Opportunistic theft is not a category in any crime
  statistic on earth. This report reconstructs its size from the measures that do
  exist &mdash; entry method, physical contact, lock status and campus incident
  coding &mdash; and answers two questions: what share of all theft it represents,
  and what share of campus theft.</div>
  <div class="meta">
    <div><b>Questions</b>Share of all theft; share on campus</div>
    <div><b>Evidence base</b>__NSRC__ primary sources</div>
    <div><b>Figures</b>__NFIG__ charts, __NTAB__ tables</div>
    <div><b>Prepared</b>28 August 2026</div>
  </div>
</div>"""

# ============================================================== SUMMARY ====

d.h2("The answer, up front", "answer")
d.p("Opportunistic theft &mdash; property taken because it was left unattended or "
    "unsecured, with no force and no contact with the owner &mdash; is <b>the "
    "overwhelming majority of theft</b>, and it is even more dominant on campus than "
    "nationally. Two numbers frame it:", "lede")

d.keys([
    (f"{D.STRICT_PCT:.0f}\u2013{D.BROAD_PCT:.0f}%", "of all US property crime is theft "
     "of property left unattended or in an unsecured place. The range is the honest "
     "uncertainty, not a hedge \u2014 the bounds are defined below.",
     "Derived from FBI UCR 2019"),
    (f"{D.CONTACT_PCT:.1f}%", "of US property crime is taken directly off a person "
     "&mdash; pocket-picking and purse-snatching combined. The thing everyone pictures "
     "is a rounding error.", "FBI UCR 2019 \u2713"),
    ("69\u201395%", "is the range campus police and campus studies report for the "
     "unattended share of <b>campus</b> theft specifically. Boston University Police put "
     "it at 90\u201395% of reports they review.", "8 institutions"),
    ("0 of 54", "bystanders in a staged campus library theft intervened when the owner "
     "had not asked anyone to watch their laptop. When asked, 84% did.",
     "University of Twente, 2025"),
])

d.box("insight", "Why the answer has to be a range",
      "<p>No crime statistics agency in the US, UK, Australia, Canada or the Netherlands "
      "records whether stolen property was left unattended. There is no tick-box for it. "
      "This report therefore triangulates from four measures that <i>are</i> collected:</p>"
      "<ol>"
      "<li><b>Physical contact</b> &mdash; whether the item was taken off the victim's "
      "body. Collected by the FBI and by NCVS.</li>"
      "<li><b>Method of entry</b> &mdash; whether force was used. Collected for burglary "
      "by the FBI and for burglary and vehicles by the UK's Crime Survey.</li>"
      "<li><b>Lock status</b> &mdash; whether the vehicle or bicycle was locked. "
      "Collected only by the UK.</li>"
      "<li><b>Offence category definition</b> &mdash; the UK defines an entire offence "
      "category as unattended theft, which makes its incidence count a direct measure.</li>"
      "</ol>"
      "<p>Each is a partial view. They agree, which is the strongest thing that can be "
      "said in the absence of a direct count.</p>")

# ============================================================ SECTION 1 ====

d.h2("1. The measurement problem", "problem")
d.p("Start with the obstacle, because it shapes everything after it. Crime statistics "
    "are built around <i>legal categories</i> &mdash; what offence was committed &mdash; "
    "not around <i>situational circumstances</i>, which is what 'opportunistic' describes. "
    "A theft from an unlocked car and a theft from a car whose window was smashed are both "
    "'theft from a motor vehicle' in the US national count.")

d.p("Our research covered the statistical agencies of five countries. The finding is "
    "consistent and worth stating as a result in its own right:")

d.table(
    ["Collection", "Country", "Does it record unattendedness?", "Best available proxy"],
    [["FBI Uniform Crime Reporting", "US", "No",
      "Burglary type of entry; larceny subcategory implies contact or not"],
     ["FBI NIBRS", "US", "No",
      "Location type of the offence \u2014 place, not guardianship"],
     ["National Crime Victimization Survey", "US", "No, but categories are contact-based",
      "'Other theft' is defined as taking without personal contact"],
     ["Crime Survey for England and Wales", "UK",
      "<b>Partly \u2014 the best in the world</b>",
      "Lock status for vehicles and bicycles; entry method for burglary; an offence "
      "category defined as unattended theft"],
     ["ABS Crime Victimisation", "Australia", "No",
      "Incident location; whether property was taken"],
     ["Statistics Canada UCR", "Canada", "No", "None \u2014 no method-of-entry field"],
     ["CBS Veiligheidsmonitor", "Netherlands", "No", "Offence category prevalence only"]],
    title="No national statistical agency measures unattendedness directly",
    sub="Assessed by opening each agency's published tables. The UK is the only country "
        "whose victim survey asks questions that bear directly on whether property was "
        "left secured.",
    source=cite("fbi_larceny", "nibrs_loc", "bjs", "ons_veh", "abs_theft", "statcan",
                "cbs_nl"))

d.box("caveat", "What this report does and does not claim",
      "<p>It does <b>not</b> claim to have found a hidden official statistic for "
      "opportunistic theft. It claims that four independent partial measures, in two "
      "countries, converge on the same conclusion, and it shows the arithmetic so the "
      "conclusion can be argued with. Every derived figure is computed in "
      "<code>research/data_opportunistic.py</code> from published inputs.</p>")

# ============================================================ SECTION 2 ====

d.h2("2. Question 1: what share of all theft is opportunistic?", "q1")
d.h3("Step one: classify the offence categories by guardianship")
d.p("US larceny-theft breaks into nine published subcategories. Each can be sorted by "
    "where the property was and who was watching it. This classification is the report's "
    "one analytical judgement, so it is set out explicitly rather than buried:")

_cls_rows = []
for name, pctv in sorted(D.LARCENY_MIX.items(), key=lambda x: -x[1]):
    cls = D.GUARDIANSHIP_CLASS[name]
    tone = {"unattended": "c-strong", "retail": "c-mod",
            "contact": "c-weak", "mixed": "c-none"}[cls]
    _cls_rows.append([name, f"<b>{pctv}%</b>",
                      f'<span class="chip {tone}">{D.CLASS_LABEL[cls]}</span>'])
d.table(["Larceny subcategory", "Share of US larceny", "Guardianship class"], _cls_rows,
        title="Sorting US larceny by who was guarding the property",
        sub="Shares are the FBI's published percent distribution of an estimated "
            f"{D.LARCENY_2019:,} larceny-thefts in 2019. The classification column is the "
            "author's, applied consistently and open to challenge.",
        num_cols={1}, source=cite("fbi_larceny"))

d.fig(
    C.segments([
        Bar(f"Unattended ({D.LARC_UNATTENDED:.1f}%)", D.LARC_UNATTENDED, color=C.POSITIVE),
        Bar(f"Residual ({D.LARC_MIXED}%)", D.LARC_MIXED, color="#7a8794"),
        Bar(f"Retail ({D.LARC_RETAIL}%)", D.LARC_RETAIL, color=C.PALETTE[0]),
        Bar("Contact (1.0%)", D.LARC_CONTACT, color=C.NEGATIVE),
    ], height=126),
    "US larceny-theft by guardianship class",
    "The red sliver on the right is pocket-picking plus purse-snatching. It is drawn to "
    "scale.",
    cite("fbi_larceny"))

d.box("warn", "The single cleanest fact in this report",
      f"<p>Pocket-picking is 0.6% of US larceny and purse-snatching is 0.4%. Therefore "
      f"<b>{D.LARC_NOT_CONTACT:.1f}% of US larceny-theft is property that was not in "
      "physical contact with its owner when it was taken.</b> That figure requires no "
      "modelling and no assumptions &mdash; it is one subtraction from the FBI's own "
      "published distribution.</p>"
      "<p>The US victim survey says the same thing from a different direction. NCVS "
      "classifies household property crime into burglary, motor vehicle theft and 'other "
      "theft', where <i>other theft</i> is formally defined as 'unlawful taking of "
      f"property or cash <b>without personal contact</b> with the victim'. That category "
      f"alone is {D.NCVS_OTHER_SHARE:.1f}% of the {D.NCVS_PROPERTY:,} property "
      f"victimisations estimated in 2023. {cite('bjs')}</p>")

d.h3("Step two: burglary confirms it from the entry side")
d.p("Larceny tells you whether the owner was holding the item. Burglary tells you "
    "something better: whether the offender had to break anything. The FBI's burglary "
    "definition explicitly states that <i>'to classify an offense as a burglary, the use "
    "of force to gain entry need not have occurred'</i>, and the count is published split "
    "three ways.")

d.fig(
    C.stacked([
        (y, [D.BURG_ENTRY[y]["Forcible entry"],
             D.BURG_ENTRY[y]["Unlawful entry, no force"],
             D.BURG_ENTRY[y]["Attempted forcible entry"]])
        for y in ("2019", "2018")],
        ["Forcible entry", "Unlawful entry \u2014 no force", "Attempted forcible entry"],
        unit="%", label_w=64),
    "More than a third of US burglaries involve no force at all",
    f"Percent of estimated burglaries. The 2019 base is {D.BURGLARY_2019:,} offences and "
    f"the 2018 base is {D.BURG_ENTRY['2018']['base']:,}. 'Unlawful entry, no force' means "
    "the offender walked in through something that was open or unlocked.",
    cite("fbi_burg19", "fbi_burg18"))

d.p(f"In 2019 that is <b>{D.BURG_ENTRY['2019']['Unlawful entry, no force']}%</b> of "
    f"{D.BURGLARY_2019:,} burglaries, or roughly <b>{D.BURG_NOFORCE_ABS:,.0f} offences</b> "
    "in which nothing was forced. The figure is stable year to year "
    f"({D.BURG_ENTRY['2018']['Unlawful entry, no force']}% in 2018), which is what you "
    "want from a measure you intend to lean on.")

d.h3("Step three: the bounded estimate")
d.p("Combining the two gives a range. The bounds differ in how the residual 'all other "
    "larceny' category (29.9% of larceny, containing everything not separately named) and "
    "motor vehicle theft are treated.")

d.fig(
    C.rangebar([
        Range("Unattended-property theft, strict definition",
              D.STRICT_PCT, D.STRICT_PCT, color=C.POSITIVE),
        Range("Unattended-property theft, broad definition",
              D.STRICT_PCT, D.BROAD_PCT, color=C.POSITIVE),
        Range("Retail theft (shoplifting)", 100 * D.LARCENY_2019 * D.LARC_RETAIL / 100
              / D.PROPERTY_CRIME_2019, 100 * D.LARCENY_2019 * D.LARC_RETAIL / 100
              / D.PROPERTY_CRIME_2019, color=C.PALETTE[0]),
        Range("Taken directly from a person", D.CONTACT_PCT, D.CONTACT_PCT,
              color=C.NEGATIVE),
    ], vmax=80, label_w=270),
    "Opportunistic theft as a share of all US property crime",
    f"Percent of {D.PROPERTY_CRIME_2019:,} estimated property crime offences, 2019.",
    cite("fbi_prop", "fbi_larceny", "fbi_burg19",
         extra="<b>Strict</b> = larceny from vehicles, buildings, bicycles and coin "
               "machines, plus no-force burglaries. <b>Broad</b> additionally counts the "
               "'all other larceny' residual and motor vehicle theft, on the ground that "
               "a parked vehicle is itself unattended property. Arithmetic in "
               "<code>data_opportunistic.py</code>."))

d.table(
    ["Component", "Offences", "% of property crime"],
    [["Strict unattended definition", f"{D.STRICT_ABS:,.0f}", f"<b>{D.STRICT_PCT:.1f}%</b>"],
     ["Broad unattended definition", f"{D.BROAD_ABS:,.0f}", f"<b>{D.BROAD_PCT:.1f}%</b>"],
     ["Shoplifting", f"{D.LARCENY_2019 * D.LARC_RETAIL / 100:,.0f}",
      f"{100 * D.LARCENY_2019 * D.LARC_RETAIL / 100 / D.PROPERTY_CRIME_2019:.1f}%"],
     ["Taken from the person", f"{D.CONTACT_ABS:,.0f}", f"{D.CONTACT_PCT:.2f}%"],
     ["<b>All property crime</b>", f"<b>{D.PROPERTY_CRIME_2019:,}</b>", "<b>100%</b>"]],
    title="The decomposition in absolute numbers",
    sub=f"Unattended-property theft outnumbers theft from the person by between "
        f"<b>{D.RATIO_LO:.0f}:1</b> and <b>{D.RATIO_HI:.0f}:1</b>.",
    num_cols={1, 2}, source=cite("fbi_prop", "fbi_larceny", "fbi_burg19"))

# ============================================================ SECTION 3 ====

d.h2("3. The UK measures it properly, and agrees", "uk")
d.p("England and Wales is the only jurisdiction found that asks victims the questions "
    "that matter. Two kinds of evidence come out of it.")

d.h3("A whole offence category defined as unattended theft")
d.p("The Home Office defines one of its theft categories in exactly the terms this report "
    f"cares about: <b>\u201c{D.UK_DEFINITION}\u201d</b>. That makes its incidence count a "
    "direct measure. Setting it against 'theft from the person' &mdash; which is the "
    "contact category, covering both stealth and snatch &mdash; gives a clean ratio, and "
    "one that has moved sharply.")

d.fig(
    C.line([
        ("Unattended", [o for _, o, _ in D.UK_TREND], C.POSITIVE),
        ("From the person", [t for _, _, t in D.UK_TREND], C.NEGATIVE),
    ], [p for p, _, _ in D.UK_TREND], unit="k", height=300),
    "Unattended theft vs theft from the person, England and Wales",
    "Crime Survey for England and Wales incidence estimates, thousands of incidents. "
    "The survey was suspended during the pandemic, hence the gap after 2019/20.",
    cite("ons_appx", extra="Table A1a. 'Other theft of personal property' is the "
                           "unattended series by Home Office definition."))

_shares = [(p, 100 * o / (o + t)) for p, o, t in D.UK_TREND]
d.p("Expressed as a share, unattended theft was a remarkably stable "
    f"<b>{min(s for _, s in _shares[:5]):.0f}\u2013{max(s for _, s in _shares[:5]):.0f}%</b> "
    "of personal-property theft from 2016/17 through 2022/23 &mdash; and then fell to "
    f"<b>{_shares[-1][1]:.0f}%</b> by 2025/26. That fall is not because unattended theft "
    "became rare; it is because snatch theft surged. Both channels matter, but the "
    "trendline is a warning against treating any single year as the answer.")

d.h3("Direct lock-status measures")
d.p("The CSEW also asks, for vehicles and bicycles, whether the thing was actually locked. "
    "These are the most direct measurements of opportunistic theft that exist anywhere.")

d.fig(
    C.hbar([Bar(lbl, v, color=C.POSITIVE if v > 40 else C.ACCENT)
            for lbl, v, _, _ in D.UK_UNLOCKED], unit="%", dp=1, label_w=282),
    "Thefts where nothing had to be defeated",
    "Percentage of incidents in each category, Crime Survey for England and Wales, "
    "year ending March 2025. Unweighted bases are small (195\u2013475 incidents), so treat "
    "these as indicative magnitudes rather than precise values.",
    cite("ons_veh", "ons_bike", "ons_burg",
         extra="Bases: theft from vehicle 475; all vehicle-related theft 311; bicycle "
               f"195; burglary 245. A further {D.UK_BURG_NOBODY_HOME}% of domestic "
               "burglaries occurred with no one at home."))

d.box("insight", "Over half of thefts from vehicles involve an unlocked door",
      "<p><b>52.8%</b> of thefts from a vehicle in England and Wales involved a door that "
      "was simply not locked, and <b>45.4%</b> of stolen bicycles were not locked at all. "
      "These are not thieves defeating security. They are thieves finding an absence of "
      "security.</p>"
      "<p>The reasons victims gave for leaving a bike unlocked are the most useful lines "
      "in the whole dataset for anyone designing an intervention:</p>")

d.fig(
    C.hbar([Bar(lbl, v) for lbl, v in D.UK_BIKE_UNLOCKED_WHY], unit="%", dp=1,
           label_w=228),
    "Why the bicycle was not locked",
    f"Percentage of the {D.UK_BIKE_UNLOCKED_BASE} incidents where the stolen bicycle was "
    "unlocked. The top two answers are not about cost, effort or equipment.",
    cite("ons_bike", extra="Table 6. Small base; indicative."))

d.p("<b>\u201cNever thought about it\u201d (29.6%) and \u201cthought the area was safe\u201d "
    "(23.9%) together account for over half.</b> Neither is solved by a better lock. Both "
    "are attention and risk-perception failures, which is a different design target "
    "entirely &mdash; and a much cheaper one.")

d.p("The older British Crime Survey went further and asked victims whether they felt "
    f"partly responsible. In {D.BCS_RESPONSIBILITY}% of unattended-property thefts "
    f"(base {D.BCS_RESP_BASE:,} incidents) victims said they were. Among those who did, "
    "the lapses named were: "
    + ", ".join(f"{lbl.lower()} {v}%" for lbl, v in D.BCS_LAPSE)
    + f" (base {D.BCS_LAPSE_BASE}). Those percentages describe only victims who already "
      "accepted some responsibility, and must not be read as shares of all incidents.")
d.raw(f'<p class="srcnote">{cite("bcs0809")}</p>')

# ============================================================ SECTION 4 ====

d.h2("4. Where and when it happens", "where")
d.p("NIBRS records the location type of each offence. It does not record guardianship, so "
    "this is context rather than proof &mdash; but the shape is informative.")

_top = sorted(D.NIBRS_LOCATIONS, key=lambda x: -x[1])[:12]
d.fig(
    C.hbar([Bar(n, 100 * v / D.NIBRS_LARCENY_BASE) for n, v in _top],
           unit="%", dp=1, label_w=250),
    "Where US larceny-theft happens",
    f"Share of {D.NIBRS_LARCENY_BASE:,} larceny-theft offences reported by NIBRS-"
    "participating agencies, 2019. NIBRS covers a subset of US agencies, so this is not a "
    "national estimate.",
    cite("nibrs_loc", extra="Location is a physical place, not a guardianship state: a "
                            "theft at a residence may or may not have been unattended."))

d.p("Residences (32.6%) and parking facilities (11.6%) together are nearly half of all "
    "recorded larceny. Both are places where people routinely leave property and walk "
    "away from it. Retail locations &mdash; department stores, supermarkets, convenience "
    "and specialty stores &mdash; account for another quarter, which is the shoplifting "
    "channel showing up in the location data.")

d.fig(
    C.stacked([
        ("Larceny", [D.NIBRS_TIME["larceny"]["AM"], D.NIBRS_TIME["larceny"]["PM"],
                     D.NIBRS_TIME["larceny"]["Unknown"]]),
        ("Burglary", [D.NIBRS_TIME["burglary"]["AM"], D.NIBRS_TIME["burglary"]["PM"],
                      D.NIBRS_TIME["burglary"]["Unknown"]]),
    ], ["AM", "PM", "Unknown"], unit="", label_w=72),
    "Larceny happens when people are awake and moving",
    f"Incident counts, NIBRS 2019. Larceny base {D.NIBRS_TIME['larceny']['base']:,}; "
    f"burglary base {D.NIBRS_TIME['burglary']['base']:,}. Nearly two-thirds of larceny "
    "occurs in PM hours, consistent with theft during active daily routines rather than "
    "night-time intrusion.",
    cite("nibrs_time"))

d.p("The UK survey agrees: <b>62.3%</b> of unattended-property thefts happened in "
    f"daylight and <b>{D.UK_OTHERTHEFT_TIMING['weekday']}%</b> on a weekday. The most "
    "common single location was <b>inside a workplace</b> "
    f"({D.UK_OTHERTHEFT_LOCATION[1][1]}%). Opportunistic theft is a daytime, working-hours "
    "phenomenon that happens in the places people spend their ordinary lives.")
d.raw(f'<p class="srcnote">{cite("ons_pers", extra=f"Tables 1b and 2b; base {D.UK_OTHERTHEFT_BASE} incidents.")}</p>')

# ============================================================ SECTION 5 ====

d.h2("5. Question 2: the campus picture", "q2")
d.p("On campus the unattended share is <b>higher</b> than nationally, and the reason is "
    "structural. A campus has almost no retail theft and comparatively little "
    "theft-from-vehicle. What it has instead is a dense population of people carrying "
    "expensive, portable electronics between buildings, and putting them down constantly.")

_c_rows = []
for inst, fig_txt, lo, hi, what, key in D.CAMPUS:
    kind = "direct" if lo is not None else "qual"
    _c_rows.append([f"<b>{inst}</b>", f"<b>{fig_txt}</b>", what,
                    chip(kind) + " " + f'<a href="{D.SOURCES[key][2]}">source</a>'])
d.table(["Institution", "Figure", "What it measures", "Type"], _c_rows,
        title="What universities themselves report about unattended theft",
        sub="Eight institutions across the US and UK. Note how many report a qualitative "
            "'majority' rather than a number: campus forces know the pattern but rarely "
            "quantify it, which is itself a finding.",
        source=cite("bu", "kstate", "qmul", "uwpd", "umpd", "utaustin", "caltech",
                    "gatech"))

d.fig(
    C.rangebar([
        Range("Boston University \u2014 theft reports that are 'unattendeds'", 90, 95,
              color=C.POSITIVE),
        Range("Queen Mary London \u2014 burglaries via unforced window or door", 91, 91,
              color=C.POSITIVE),
        Range("UW-Madison \u2014 textbook thefts from unattended bags", 69, 69,
              color=C.POSITIVE),
        Range("US national \u2014 all property crime (this report)",
              D.STRICT_PCT, D.BROAD_PCT, color=C.PALETTE[0]),
        Range("University of Miami \u2014 unattended theft as share of ALL campus crime",
              50, 50, color=C.ACCENT),
    ], vmax=100, label_w=286),
    "Campus unattended-theft shares against the national benchmark",
    "Denominators differ and are not interchangeable \u2014 read the labels. The Miami "
    "figure is a share of all crime, not all theft, so it understates the theft-only "
    "share. Every campus figure sits at or above the national range.",
    cite("bu", "qmul", "uwpd", "umpd"))

d.box("insight", "Answering Q2 directly",
      "<p>Campus sources do not support a single authoritative percentage, and this report "
      "will not invent one. What they support is this: <b>on a university campus, "
      "somewhere between two-thirds and over 90% of theft is theft of property that was "
      "left unattended or unsecured.</b> The lower bound comes from the one study with a "
      "clean denominator over all incidents of a theft type (UW-Madison, 69% of textbook "
      "thefts). The upper comes from a police force describing its whole reviewed caseload "
      "(Boston University, 90\u201395%).</p>"
      "<p>Every additional institution examined \u2014 Miami, UT Austin, Kansas State, "
      "Caltech, Georgia Tech, Queen Mary \u2014 describes the same dominance in the same "
      "terms, without exception. Eight out of eight is not proof of a precise number, but "
      "it is strong evidence about the shape of the problem.</p>")

d.h3("The campus burglary analogue")
d.p("Queen Mary University of London's police analysis is the closest campus equivalent to "
    "the FBI's no-force burglary measure, and the result is more extreme than the national "
    "figure.")

d.fig(
    C.hbar([
        Bar("Burglaries entering via a window", D.QMUL["window"], color=C.ACCENT),
        Bar("Burglaries entering via a door", D.QMUL["door"], color=C.ACCENT),
        Bar("Burglaries targeting laptops", D.QMUL["laptops_targeted"], color=C.PALETTE[0]),
    ], unit="%", label_w=246),
    "Queen Mary University of London campus burglary, July\u2013December 2009",
    "Of the 64% entering by window, only <b>one</b> window had been forced. Of the 27% "
    "entering by door, only <b>one</b> door had been forced. Everything else was open or "
    "unlocked \u2014 roughly 91% of campus burglaries required defeating nothing at all.",
    cite("qmul", extra="The 91% figure is the author's arithmetic on the report's "
                       "published shares and its statement that only one window and one "
                       "door were forced."))

d.p("The intervention that followed is instructive: after a targeted campaign, recorded "
    f"residential burglaries on campus fell from {D.QMUL['burglary_before']} to "
    f"{D.QMUL['burglary_after']}, bike thefts from {D.QMUL['bike_before']} to "
    f"{D.QMUL['bike_after']}, and total offences from {D.QMUL['total_before']} to "
    f"{D.QMUL['total_after']} over comparable September\u2013December windows "
    f"(a {100 * (D.QMUL['total_before'] - D.QMUL['total_after']) / D.QMUL['total_before']:.0f}% "
    "reduction).")

d.h3("What gets left unattended, and what happens when it does")
d.p("Two campus field experiments, both Dutch, measure the two halves of the mechanism: "
    "how often students expose property, and whether anyone protects it when they do.")

d.raw('<div class="two">')
d.fig(
    C.vbar([Bar("Control", D.DELFT["unattended_control"], color=C.NEGATIVE),
            Bar("After warning", D.DELFT["unattended_warning"], color=C.POSITIVE)],
           unit="%", dp=1, width=520, height=250),
    "Students leaving laptops unattended",
    f"Delft University of Technology study hall, n={D.DELFT['n_phase']} per phase. A "
    "warning intervention cut exposure but did not eliminate it.",
    cite("delft"))
d.fig(
    C.vbar([Bar("No request made", D.TWENTE["no_request_intervened"], color=C.NEGATIVE),
            Bar("Owner asked a neighbour", D.TWENTE["request_intervened"],
                color=C.POSITIVE)],
           unit="%", width=520, height=250),
    "Bystanders intervening in a staged theft",
    f"University of Twente library, {D.TWENTE['total_obs']} observations. "
    f"{D.TWENTE['no_request_intervened']} of {D.TWENTE['no_request_n']} intervened "
    "unprompted.",
    cite("twente"))
d.raw("</div>")

d.box("warn", "Zero out of fifty-four",
      "<p>In the Twente experiment a researcher openly removed a laptop from a library "
      f"desk after the owner left. Where the owner had not asked anyone to keep an eye on "
      f"it, <b>not one of {D.TWENTE['no_request_n']} bystanders intervened</b>. Where the "
      f"owner had asked, <b>{D.TWENTE['request_intervened']}%</b> did.</p>"
      "<p>Four thefts were staged in sequence one to two metres apart; none of the "
      "guardians noticed the previous ones. And a Kansas State surveillance recording "
      f"captured a laptop being unplugged and removed in <b>{D.KSTATE_SECONDS} seconds</b>.</p>"
      "<p>The implication is uncomfortable and important: <b>a crowded library provides "
      "essentially no passive protection.</b> Presence is not guardianship. The systematic "
      "review of the guardianship literature reports spontaneous intervention rates in "
      f"staged-crime studies ranging {D.HOLLIS_RANGE[0]}\u2013{D.HOLLIS_RANGE[1]}%, and "
      "notes that high-quality field tests are lacking. "
      + cite("twente", "kstate", "hollis") + "</p>")

d.fig(
    C.hbar([Bar(n, v) for n, v in D.UW_MECHANISM], unit="%", label_w=234),
    "Mechanism of campus theft where it has been coded",
    "Share of UW-Madison campus textbook thefts by mechanism. The only campus dataset "
    "found that codes mechanism across all incidents of a theft type.",
    cite("uwpd"))

# ============================================================ SECTION 6 ====

d.h2("6. What actually gets taken", "items")
d.p("The obvious guess is \u201cphones\u201d. For opportunistic theft the obvious guess is "
    "<b>wrong</b>, and the way in which it is wrong is the most useful thing in this "
    "section. The item profile of unattended theft is almost the mirror image of the item "
    "profile of theft taken off a person.", "lede")

d.h3("The same survey, the same country, two completely different answers")
d.p("Because the UK separates unattended theft from contact theft as distinct offence "
    "categories, and publishes an items-stolen table for each, the two can be set side by "
    "side directly. This is the cleanest available answer to the question.")

d.fig(
    C.pairbar(D.ITEMS_PAIRED, ("Unattended theft", "Taken from the person"),
              label_w=262, vmax=55),
    "What is stolen, by theft channel",
    f"Percentage of incidents in which each item type was taken, England and Wales, "
    f"{D.ITEMS_YEARS} pooled. An incident can involve several item types, so columns sum "
    "to more than 100%.",
    cite("ons_items", extra=f"Tables 3a and 3b, pooled across three survey years and "
                            f"weighted by published unweighted bases "
                            f"({D.ITEMS_BASE_UNATTENDED} unattended incidents, "
                            f"{D.ITEMS_BASE_CONTACT} contact incidents). Pooling by the "
                            "author; single-year bases are 120\u2013204 and too small to "
                            "rank reliably on their own."))

d.box("insight", "Phones are a contact-theft problem, not an unattended-theft problem",
      "<p>Mobile phones are taken in <b>48.2%</b> of thefts from the person and only "
      "<b>9.9%</b> of unattended thefts \u2014 a five-fold difference in the same survey, "
      "in the same years, in the same country. In the latest single year the gap is wider "
      "still: 57.6% versus 5.4%.</p>"
      "<p>The reason is obvious once stated: <b>a phone is almost never the thing you put "
      "down and walk away from.</b> It is in your hand or your pocket, which is precisely "
      "why it has to be snatched. Everything a person actually abandons for a few minutes "
      "\u2014 a coat, a bag, a laptop, a toolbox, a bike \u2014 is what turns up in the "
      "unattended column.</p>"
      "<p>Any product aimed at opportunistic theft that is designed around protecting a "
      "phone is aimed at the wrong 10%.</p>")

d.h3("There is no single \u2018most stolen item\u2019 in unattended theft")
d.p("The second finding is the shape of the distribution rather than its top entry. "
    "Contact theft is <b>concentrated</b>: phones and wallets alone account for most of "
    "it. Unattended theft is <b>flat</b>. The largest named category, clothing, is under a "
    "fifth of incidents, and the residual \u2018other\u2019 category is the biggest single "
    "entry at 31.5% \u2014 which tells you the true distribution is even longer-tailed than "
    "the published one.")

d.table(
    ["Rank", "Unattended theft", "Share", "Theft from the person", "Share"],
    [[str(i + 1), u[0], f"<b>{u[1]}%</b>", c[0], f"<b>{c[1]}%</b>"]
     for i, (u, c) in enumerate(zip(
         sorted([p for p in D.ITEMS_PAIRED if p[0] != "Other"], key=lambda x: -x[1])[:8],
         sorted([(p[0], p[2]) for p in D.ITEMS_PAIRED if p[0] != "Other"],
                key=lambda x: -x[1])[:8]))],
    title="Top named items by channel, ranked",
    sub="Excluding the residual 'other' category. Read the two halves as separate "
        "rankings \u2014 the rows are not paired.",
    num_cols={0, 2, 4}, source=cite("ons_items"))

d.p("Note what sits high in the unattended column and is essentially absent from the "
    "contact column: <b>tools or work materials</b> (8.2% versus 0.1%) and <b>food, "
    "toiletries and cigarettes</b> (7.4% versus 0.3%). Nobody pickpockets a drill. These "
    "categories exist only because things get left in vans, workplaces, lockers and "
    "cloakrooms.")

d.h3("Value: same average, very different shape")
d.p("The cost tables sharpen the picture in a way the item counts do not.")

d.table(
    ["Measure", "Unattended theft", "Theft from the person"],
    [["Mean value of items stolen", f"\u00a3{D.COST['unattended']['mean']:,.2f}",
      f"\u00a3{D.COST['contact']['mean']:,.2f}"],
     ["<b>Median value of items stolen</b>",
      f"<b>\u00a3{D.COST['unattended']['median']}</b>",
      f"<b>\u00a3{D.COST['contact']['median']}</b>"],
     ["Incidents where \u00a31,000 or more was taken",
      f"{D.COST['unattended']['over_1000']}%", f"{D.COST['contact']['over_1000']}%"],
     ["Unweighted base (incidents)", f"{D.COST['unattended']['base']}",
      f"{D.COST['contact']['base']}"]],
    title="Cost of stolen items, year ending March 2025",
    sub="The means are almost identical. The medians differ five-fold.",
    num_cols={1, 2}, source=cite("ons_items", extra="Tables 4a and 4b."))

d.box("insight", "The five-fold median gap is the whole story",
      f"<p>Mean loss is \u00a3{D.COST['unattended']['mean']:,.0f} for unattended theft and "
      f"\u00a3{D.COST['contact']['mean']:,.0f} for contact theft \u2014 statistically "
      "indistinguishable. But the <b>median</b> is "
      f"\u00a3{D.COST['unattended']['median']} versus "
      f"\u00a3{D.COST['contact']['median']}.</p>"
      "<p>That means the two channels have completely different distributions hiding "
      "behind the same average. Contact theft is <b>consistently expensive</b>: the thief "
      "picked the target and picked well. Unattended theft is <b>usually cheap with a fat "
      f"tail</b>: most incidents are a coat or a bag, but {D.COST['unattended']['over_1000']}% "
      "exceed \u00a31,000 and drag the mean up to meet contact theft.</p>"
      "<p>Design consequence: an intervention for opportunistic theft has to be worth "
      "deploying for an \u00a380 loss, because that is the typical case. It cannot be "
      "priced or designed around the laptop-sized tail.</p>")

d.h3("The largest single unattended stream is a parked car")
d.p("Switching from the UK to the US, and from items to offence volume, gives the other "
    "half of the answer. The FBI publishes larceny subtype counts with average values.")

_t23_rows = sorted(D.T23.items(), key=lambda kv: -kv[1][0])
d.fig(
    C.hbar([Bar(k, v[0] / 1000,
                color={"unattended": C.POSITIVE, "retail": C.PALETTE[0],
                       "contact": C.NEGATIVE, "residual": "#7a8794"}[v[2]])
            for k, v in _t23_rows], unit="k", dp=0, label_w=234),
    "US larceny offences by subtype",
    f"Thousands of offences, 2019, {D.T23_AGENCIES:,} reporting agencies covering an "
    f"estimated population of {D.T23_POPULATION:,}. Green is unattended-property theft, "
    "blue retail, red taken-from-the-person, grey the undecomposed residual.",
    cite("fbi_t23", extra="The nine subtype counts sum exactly to the published total of "
                          f"{D.T23_TOTAL_OFFENCES:,}, which confirms the transcription."))

d.p(f"<b>Theft from motor vehicles is the single largest named larceny subtype in the "
    f"United States at {D.T23['Theft from motor vehicles'][0]:,} offences</b> \u2014 more "
    f"than shoplifting, and {D.T23['Theft from motor vehicles'][0] / (D.T23['Pocket-picking'][0] + D.T23['Purse-snatching'][0]):.0f} "
    "times the combined total of pocket-picking and purse-snatching. If you want one "
    "sentence for what opportunistic theft looks like at national scale, it is "
    "<i>somebody's belongings taken out of a parked car</i>.")

d.fig(
    C.hbar([Bar(n, v) for n, v in D.VEHICLE_ITEMS], unit="%", dp=1, label_w=300),
    "What is taken out of vehicles",
    f"Percentage of theft-from-vehicle incidents, England and Wales, year ending March "
    f"2025, unweighted base {D.VEHICLE_ITEMS_BASE} incidents. 'Valuables' is the ONS "
    "grouping and bundles jewellery, bags, purses, wallets, cash, cards, clothes and "
    "documents.",
    cite("ons_vehitems", extra=f"Median loss \u00a3{D.VEHICLE_COST['median']}, mean "
                               f"\u00a3{D.VEHICLE_COST['mean']:,.2f} "
                               f"(base {D.VEHICLE_COST['base']})."))

d.table(
    ["Guardianship class", "Offences", "Share", "Mean value", "Total value"],
    [["Unattended property", f"{D.T23_UNATT_N:,}", f"{D.T23_UNATT_SHARE:.1f}%",
      f"${D.T23_UNATT_AVG:,.0f}", f"${D.T23_UNATT_VAL / 1e9:.2f}bn"],
     ["Retail (shoplifting)", f"{D.T23_RETAIL_N:,}",
      f"{100 * D.T23_RETAIL_N / D.T23_TOTAL_OFFENCES:.1f}%",
      f"${D.T23_RETAIL_AVG:,.0f}", f"${D.T23_RETAIL_VAL / 1e6:.0f}m"],
     ["Taken from the person", f"{D.T23_CONTACT_N:,}",
      f"{100 * D.T23_CONTACT_N / D.T23_TOTAL_OFFENCES:.1f}%",
      f"${D.T23_CONTACT_AVG:,.0f}", f"${D.T23_CONTACT_VAL / 1e6:.0f}m"]],
    title="Volume and value by guardianship class, US larceny 2019",
    sub=f"Unattended-property theft accounts for {D.T23_UNATT_SHARE:.1f}% of larceny "
        f"offences and <b>{D.T23_VALUE_RATIO:.0f} times</b> the stolen value of theft "
        "taken directly from a person. Note the mean values are near-identical "
        f"(${D.T23_UNATT_AVG:,.0f} versus ${D.T23_CONTACT_AVG:,.0f}) \u2014 the same "
        "pattern the UK cost tables show.",
    num_cols={1, 2, 3, 4},
    source=cite("fbi_t23", extra="Class assignment and aggregation by the author, using "
                                 "the same classification as Section 2."))

d.h3("On campus the answer narrows sharply")
d.p("Campus is the exception to the flat distribution, and this matters because campus is "
    "the deployment target. Two institutions publish item-level counts, and they agree.")

d.raw('<div class="two">')
d.fig(
    C.hbar([Bar(n, v, color=C.POSITIVE if n == "Bicycles" else C.PALETTE[0])
            for n, v in D.BU_ITEMS], unit="", dp=0, label_w=180, width=520, row_h=27),
    "Boston University: items stolen",
    f"Counts within {D.BU_LARCENIES} reported campus larcenies, {D.BU_PERIOD}. BU Police "
    "note that most of the stolen computers were left unattended by their owners.",
    cite("bu_items", extra="A further "
                           f"{D.BU_CARDS} credit or debit cards were reported stolen; "
                           "categories are not mutually exclusive and the article does "
                           "not state whether counts are incidents or items."))
d.fig(
    C.hbar([Bar(f"{n} \u2014 bikes", v, color=C.POSITIVE) for n, v in D.UOFT_BIKE_SITES]
           + [Bar(f"{n} \u2014 laptops", v, color=C.PALETTE[0])
              for n, v in D.UOFT_LAPTOP_SITES[:2]],
           unit="", dp=0, label_w=196, width=520, row_h=27),
    "Toronto: where bikes and laptops go",
    f"Theft reports by location, from {D.UOFT_THEFT_REPORTS:,} theft entries in University "
    "of Toronto Campus Safety Activity Reports, 2019\u20132025.",
    cite("uoft", extra="Compiled by a student newspaper from official activity reports. "
                       "The source stresses these count reports, not incidents."))
d.raw("</div>")

d.box("win", "On campus, the answer is bicycles and laptops",
      "<p>Boston University recorded <b>120 bicycle thefts</b> and <b>61 computers, "
      "laptops or tablets</b> against just <b>18 mobile phones</b> in a single academic "
      "year. The University of Toronto, ranking item descriptions across "
      f"{D.UOFT_THEFT_REPORTS:,} theft reports over six years, puts them in the order "
      "<b>bicycles, money, laptops, bags, phones</b> \u2014 phones last.</p>"
      "<p>Both institutions independently reproduce the national pattern in sharper form. "
      "A campus concentrates exactly the two goods that are valuable, portable, and "
      "<i>routinely parked</i>: the bike you lock outside for three hours and the laptop "
      "you leave on a library desk while you get coffee.</p>"
      "<p>The geography confirms the mechanism. Toronto's bike thefts cluster at the "
      "Athletic Centre (49 reports) and its laptop thefts at the Bahen Centre (20) and "
      "Robarts Library (19) \u2014 a gym and two study buildings. These are the places "
      "people must put their things down in order to do the thing they came for.</p>")

d.box("caveat", "So what is the single most stolen thing?",
      "<p>Stated as precisely as the evidence allows:</p>"
      "<ul>"
      "<li><b>By offence volume, nationally:</b> property taken from a <b>parked motor "
      f"vehicle</b> \u2014 {D.T23['Theft from motor vehicles'][0]:,} US offences in 2019, "
      "the largest named larceny subtype.</li>"
      "<li><b>By item, in the tightest available unattended measure:</b> no single item "
      "dominates. <b>Clothing</b> leads the named categories at 16.8% of incidents, ahead "
      "of cash (13.0%), phones (9.9%) and computers (9.5%).</li>"
      "<li><b>On a university campus:</b> <b>bicycles first, laptops second</b>, on the "
      "two institutions publishing counts.</li>"
      "<li><b>What it is <i>not</i>:</b> mobile phones. They dominate theft from the "
      "person and are a minor category in every unattended measure examined.</li>"
      "</ul>")

d.h2("7. Where the stolen things go", "disposal")
d.p("Theft does not end when the item leaves. What happens next determines whether the "
    "theft was worth committing, and therefore whether it happens again. The disposal "
    "side turns out to be the softest point in the whole system \u2014 and the popular "
    "picture of it is wrong in two specific ways.", "lede")

d.box("insight", "Disposal is not the aftermath. It is the motive.",
      "<p>Interviews with 50 prolific offenders in Shropshire found that <b>ease of "
      "disposal was the most commonly reported reason for stealing a particular item</b> "
      "\u2014 ahead of ease of theft and ahead of demand for the product. An Australian "
      "burglar study found the same. Disposability is the D in CRAVED, and offenders "
      "report it as the first consideration, not the last.</p>"
      f"<p>This is why the Activation Lock result in Section 3 worked. The UK Home Office "
      "put it plainly in its own review: Apple's more secure operating system <i>'seems to "
      "have dramatically altered the resale value of iPhones and also caused a marked fall "
      f"in thefts'</i>. {cite('horr81', 'popgoods')}</p>")

d.h3("Correction one: most stolen property is not sold at all any more")
d.p("The best quantitative series on disposal is Australian. The Drug Use Monitoring in "
    f"Australia programme ran a stolen-goods module across <b>{D.DUMA_WAVES} waves between "
    f"2002 and 2017</b>, interviewing <b>{D.DUMA_N:,} arrestees</b> in police custody about "
    "what they usually did with what they stole. The trend is dramatic and runs opposite "
    "to the intuition.")

d.fig(
    C.line([("Kept or used it", [D.DUMA_KEPT_2002, D.DUMA_KEPT_2017], C.POSITIVE),
            ("Sold it", [D.DUMA_SOLD_2002, D.DUMA_SOLD_2017], C.NEGATIVE)],
           ["2002", "2017"], unit="%", height=270),
    "Selling collapsed; keeping took over",
    f"Percentage of police detainee respondents reporting what they <i>usually</i> do with "
    f"stolen goods. Selling fell {D.DUMA_SOLD_2002 - D.DUMA_SOLD_2017} percentage points "
    f"and keeping rose {D.DUMA_KEPT_2017 - D.DUMA_KEPT_2002}. Endpoints of a seven-wave "
    "series are shown; the intermediate waves lie between them.",
    cite("duma", extra=f"N={D.DUMA_N:,} arrestees across {D.DUMA_WAVES} waves. Percentages "
                       "are of respondents, not of offences or items. Arrestee samples are "
                       "not representative of all offenders, and Australia is not the UK "
                       "or US \u2014 but no comparable series exists for either."))

d.p(f"By 2017, <b>{D.DUMA_KEPT_2017}%</b> of these offenders said they usually kept or used "
    f"what they stole and only <b>{D.DUMA_SOLD_2017}%</b> usually sold it. Across the whole "
    f"series, swapping for drugs averaged {D.DUMA_ROUTE_AVG[2][1]}%, consuming the goods "
    f"outright {D.DUMA_ROUTE_AVG[3][1]}%, and 'spending them on other things' fell to "
    f"{D.DUMA_SPEND_2017}% by 2017. The authors link the shift to the collapse in "
    "second-hand value of consumer electronics \u2014 there is simply less point selling a "
    "phone that will not activate or a television worth forty pounds.")

d.h3("Correction two: the buyer is a drug dealer, not a pawnbroker")
d.p("When goods <i>are</i> sold, the stereotype of the shady pawnshop is almost the least "
    "likely destination.")

d.fig(
    C.hbar([Bar(n, v, color=C.NEGATIVE if "Drug" in n else
                (C.ACCENT if "Pawn" in n else C.PALETTE[0]))
            for n, v in D.DUMA_OUTLETS], unit="%", label_w=272),
    "Who buys stolen goods from the thief",
    "Average share of police detainee respondents naming each outlet as where they usually "
    f"sell or swap, 2003 onwards. Drug dealers reached {D.DUMA_DRUG_DEALER_2017}% by 2017. "
    "Pawnbrokers and second-hand dealers \u2014 the channel most heavily regulated in most "
    "countries \u2014 are the smallest named route.",
    cite("duma"))

d.p("The New South Wales prison interviews point the same way. Of "
    f"<b>{D.BOCSAR_N} imprisoned burglars</b>, around <b>{D.BOCSAR['swapped_for_drugs']}%</b> "
    "admitted swapping stolen goods for illegal drugs, roughly half did so <b>within an "
    f"hour</b> of the theft and over <b>{D.BOCSAR['drugs_within_24h']}%</b> within a day. "
    f"About <b>{D.BOCSAR['stole_to_order']}%</b> said they had stolen goods to order.")
d.raw(f'<p class="srcnote">{cite("bocsar")} Imprisoned-offender sample; not representative '
      "of all burglars, and self-reported.</p>")

d.box("warn", "Speed is the reason enforcement loses",
      f"<p>Half of the NSW burglars converted goods to drugs <b>within one hour</b>, and "
      f"over {D.BOCSAR['drugs_within_24h']}% within 24 hours. The Home Office's own "
      "offender interviews found stolen goods were usually sold within a day and were "
      "<i>rarely dumped or given away</i>.</p>"
      "<p>Set that against the recovery funnel in Section 4. By the time a victim has "
      "noticed the loss, decided it is worth reporting, and been recorded, the item has "
      f"typically already changed hands. {cite('bocsar', 'mra')}</p>")

d.h3("What the thief actually gets")
d.p("Stolen goods sell at a steep discount, which is the economic fact that makes "
    "high-volume low-value theft viable only in bulk.")

d.fig(
    C.hbar([Bar(n, v) for n, v in D.DUMA_PRICE], unit="%", label_w=290, vmax=50),
    "Share of retail value the thief receives",
    f"Average across waves. 'About one-third' was the most common answer in every wave "
    f"({D.DUMA_PRICE_THIRD_2002}% in 2002, {D.DUMA_PRICE_THIRD_2017}% in 2017); the share "
    f"reporting 'about half' rose to {D.DUMA_PRICE_HALF_2017}% by 2017.",
    cite("duma"))

d.p("Two consequences follow. First, an item has to be worth roughly three times the "
    "thief's effort threshold before it is worth taking for resale at all \u2014 which is "
    "exactly why so much opportunistic theft is now retention rather than resale. Second, "
    f"in 2017 <b>{D.DUMA_UNKNOWN_FATE[0]} of {D.DUMA_UNKNOWN_FATE[1]}</b> respondents who "
    "sold goods <b>did not know what happened to them afterwards</b>. The chain beyond the "
    "first handover is invisible even to the people in it.")

d.h3("Opportunistic theft specifically: much of it never enters a market")
d.p("This is where the general picture and the opportunistic picture separate. The Home "
    "Office's review of stolen-goods value classifies which commonly stolen items would "
    "plausibly be resold at all \u2014 and several of the most frequently stolen are "
    "explicitly <i>not</i> resale goods.")

d.fig(
    C.hbar([Bar(n + ("" if r else "  \u2716"), v,
                color=C.PALETTE[0] if r else C.NEGATIVE)
            for n, v, r in D.HORR81_ITEMS[:14]], unit="%", dp=1, label_w=250),
    "Most stolen items, and whether they can be resold",
    "Percentage of household and personal acquisitive incidents with loss involving each "
    "item, England and Wales 2013/14. Items marked \u2716 in red are ones the Home Office "
    "treats as not entering a resale market. Percentages sum above 100 because incidents "
    "involve multiple items.",
    cite("horr81", extra="Resale classification follows the report's own treatment; the "
                         "report states that wallets and purses are 'collateral damage in "
                         "thefts, i.e. they are stolen for their contents and later "
                         "discarded'."))

d.box("insight", "Cash is the perfect stolen good, and it is the most stolen thing there is",
      f"<p>Cash has been <b>the single most frequently stolen item in every year the survey "
      f"has run since {D.HORR81_CASH_TOP_SINCE}</b>. It needs no fence, no buyer, no "
      "marketplace and no discount. It is not disposed of \u2014 it <i>is</i> the "
      "proceeds.</p>"
      "<p>Around it sit the other non-market items: plastic cards, wallets and purses, "
      "documents and keys. The Home Office treats these as taken for their contents and "
      "then thrown away. Groceries, alcohol and cigarettes are consumed. None of these "
      "generate a resale trail, which means <b>for a large share of opportunistic theft "
      "there is no market to disrupt and no second-hand listing to detect</b>.</p>"
      "<p>That is a hard constraint on any recovery product. The single most stolen thing "
      "in the world is untraceable by construction.</p>")

d.h3("The six markets, for the goods that do get sold")
d.table(
    ["Market type", "How it works"],
    [[f"<b>{n}</b>", desc] for n, desc in D.MARKET_TYPES],
    title="Sutton's typology of stolen goods markets",
    sub="Five were identified in the original Home Office work; 'eSelling' was added later "
        "as online marketplaces matured. The literature is explicit that no one market type "
        "is more important than another.",
    source=cite("popgoods", "mra"))

d.p("The demand side is not marginal. Nationally representative British surveys found "
    f"<b>{D.BCS_OFFERED}%</b> of adults had been offered stolen goods in the previous year "
    f"and <b>{D.BCS_BOUGHT_5Y}%</b> admitted buying some in the previous five; "
    f"<b>{D.BCS_NEIGHBOURS_SOME}%</b> thought at least some of their neighbours bought "
    "stolen goods for the home. A later self-report survey put buying at "
    f"<b>{D.OCJS_BOUGHT}%</b> of adults in a year and selling at <b>{D.OCJS_SOLD}%</b>.")

d.fig(
    C.line([("Offered in past 5 years", [v for _, v, _, _ in D.OFFERED_TREND], C.PALETTE[0]),
            ("Offered in past 12 months", [v for _, _, v, _ in D.OFFERED_TREND], C.ACCENT)],
           [p for p, _, _, _ in D.OFFERED_TREND], unit="%", height=280),
    "Public exposure to stolen-goods markets is declining",
    "Percentage of Crime Survey respondents who reported being offered goods they suspected "
    "were stolen. Unweighted bases vary sharply between years (467 to 11,751), so read the "
    "level cautiously and the direction more confidently.",
    cite("horr81", extra="Annex B. Bases exclude don't-know and refused responses."))

d.h3("Modern channels: online, export, and the drug link")
d.ul([
    f"<b>Online selling is growing from a small base.</b> Australian arrestees reporting "
    f"internet sale rose from {D.DUMA_INTERNET[0][1]}% in {D.DUMA_INTERNET[0][0]} to "
    f"{D.DUMA_INTERNET[1][1]}% in {D.DUMA_INTERNET[1][0]}. In a North American survey of "
    f"{D.BIKE_SURVEY_N:,} bicycle-theft victims, {D.BIKE_RECOVERED}% recovered their bike, "
    f"and <b>{D.BIKE_FOUND_ONLINE}% of those recovered were found being sold online</b> "
    "\u2014 note the denominator is recovered bikes, not all stolen bikes.",
    f"<b>Export defeats domestic blocking.</b> The UK reports that <b>{D.PHONE_BLOCK_48H}%"
    "</b> of handsets reported stolen are blocked across all networks within 48 hours "
    "\u2014 but blocked phones still work abroad. The Metropolitan Police charged a network "
    f"that trafficked up to <b>{D.MET_PHONES['trafficked']:,} stolen phones</b> from the UK "
    f"to China, which it believed accounted for about <b>{D.MET_PHONES['share_london']}% of "
    "all phones stolen in London</b> in the period. Street thieves were paid up to "
    f"\u00a3{D.MET_PHONES['paid_street']} per device; some sold for up to "
    f"${D.MET_PHONES['sold_china']:,} in China. Over "
    f"{D.MET_PHONES['recovered']:,} iPhones were recovered.",
    f"<b>Drugs are the engine.</b> Around <b>{D.DRUG_ACQUISITIVE_SHARE}%</b> of acquisitive "
    f"crime is estimated to be committed by crack or opiate users, and {D.POP_ARRESTED_THIEVES_DRUGS}% "
    "of arrested thieves in the UK are heroin or cocaine users. This is why immediacy beats "
    "price: the goods need to become drugs today, not fetch their best price next week.",
    "<b>Regulation of resale is being attempted.</b> The US INFORM Consumers Act (in force "
    "June 2023) requires online marketplaces to collect and verify bank, identity and "
    "contact details for high-volume sellers, and to publish those details for the largest. "
    "No evaluation of its effect on stolen-goods resale has yet been published.",
])
d.raw(f'<p class="srcnote">{cite("duma", "bikefind", "phoneblock", "metphone", "horr81", "inform")}</p>')

d.box("warn", "A widely quoted figure you should not use",
      "<p>The National Retail Federation's April 2023 report attributed <i>nearly half</i> "
      "of $94.5bn in retail shrink to organised retail crime. <b>NRF withdrew the claim in "
      "December 2023</b> after the underlying source was shown to be a six-year-old "
      "inventory-loss survey that included non-theft causes. In NRF's own corrected "
      "figures, external theft is about 36% of shrink and organised retail crime is only a "
      f"subset of that. Any pitch citing the retracted number is citing a withdrawn "
      f"statistic. {cite('nrf')}</p>")

d.h3("The strongest evidence in this report: close the channel, the theft stops")
d.p("If disposal drives target selection, then removing a disposal channel should remove "
    "the theft. There is a clean natural experiment for exactly that. Between 2012 and 2013 "
    "the UK required scrap metal dealers to verify seller identity and banned cash payment, "
    "then introduced licensing.")

d.fig(
    C.vbar([Bar("Before intervention", D.SCRAP["pre"], color=C.NEGATIVE),
            Bar("After intervention", D.SCRAP["post"], color=C.POSITIVE)],
           unit="", dp=1, height=280),
    "Metal theft before and after the disposal channel was closed",
    "Mean recorded metal-theft incidents per region per month, England and Wales, "
    "January 2010 to December 2013, from an independent Energy Networks Association panel.",
    cite("horr80", extra=f"Raw fall {D.SCRAP['raw_pct']}% (95% CI "
                         f"{D.SCRAP['ci'][0]}\u2013{D.SCRAP['ci'][1]}%). A regression "
                         "controlling for copper price and other acquisitive crime "
                         f"estimated a level effect of {D.SCRAP['adj_level']} incidents per "
                         f"region-month (about {D.SCRAP['adj_pct']}%, p&lt;.001). The "
                         "evaluation cannot separate the Act from the preceding "
                         "cash-ban and identity-check operations, and the ENA panel covers "
                         f"about {D.SCRAP['ena_coverage']}% of metal-theft incidents."))

d.p("Metal theft roughly halved. Scotland, which did not implement the measures over the "
    "same period, saw metal theft rise \u2014 which is consistent with displacement across "
    "the border and, awkwardly for the intervention, is exactly what you would expect if "
    "the mechanism is the market rather than the offender.")

d.box("win", "The pattern that keeps repeating",
      "<p>Three independent cases in this report share one mechanism. Apple made stolen "
      "iPhones unusable and iPhone robberies fell 38% in San Francisco. UW-Madison made "
      "stolen textbooks hard to sell and textbook theft fell 86%. The UK made stolen metal "
      "hard to sell for cash and metal theft roughly halved.</p>"
      "<p>None of the three prevented a single theft attempt directly. All three removed "
      "the buyer. <b>For property crime, the disposal channel is a more reliable "
      "intervention point than the offender, the victim or the object.</b></p>"
      "<p>The caution for opportunistic theft specifically: the items most often taken "
      "opportunistically \u2014 cash, cards, wallets, food, clothing \u2014 largely have no "
      "channel to close. Channel-closing works brilliantly for phones, metal, textbooks and "
      "bicycles, and not at all for the single most stolen thing there is.</p>")

d.h2("8. Why this changes what you should build", "implications")
d.p("If opportunistic theft were a minority of theft, the rational response would be "
    "detection and enforcement. It is not a minority. It is the overwhelming majority, and "
    "its defining feature is that <b>no security was defeated</b>. That changes the target.")

d.table(
    ["Because the evidence says…", "…the design implication is"],
    [["Between half and three-quarters of property crime is unattended-property theft, "
      "and under 1% is taken from a person",
      "Optimise for the moment a person puts something down and walks away. Anti-"
      "pickpocket features address a rounding error."],
     ["52.8% of vehicle thefts and 45.4% of bike thefts involved no lock at all",
      "The marginal return on <i>better</i> locks is low. The return on <i>getting the "
      "existing lock used</i> is high."],
     ["The top reasons for not locking are 'never thought about it' and 'thought the area "
      "was safe'",
      "This is an attention and risk-calibration problem, not an equipment problem. "
      "Prompting at the right moment beats hardware."],
     ["0 of 54 bystanders intervened unprompted, but 84% did when asked",
      "Guardianship is <b>activated by request</b>, not by presence. A mechanism that lets "
      "someone cheaply ask a neighbour to watch their desk converts a null into an 84%."],
     ["Larceny peaks in PM hours, in daylight, on weekdays, inside workplaces and "
      "study buildings",
      "Interventions belong in ordinary daytime routine spaces, not in dark corners at "
      "night."],
     ["Campus unattended share (69\u201395%) exceeds the national share",
      "A campus is the highest-yield deployment context for exactly this intervention, "
      "which validates starting there."],
     ["A laptop was removed in 6 seconds; guardians 1\u20132 metres away noticed nothing",
      "Any alerting mechanism must fire in single-digit seconds. Anything slower is "
      "forensic, not preventive."]],
    title="From evidence to design",
    source=cite("fbi_larceny", "ons_veh", "ons_bike", "twente", "nibrs_time", "bu",
                "kstate"))

d.box("win", "The one intervention the evidence most directly supports",
      "<p>The Twente result is the strongest actionable finding in this report, because it "
      "is a controlled campus experiment with an enormous effect size and a trivially "
      "cheap mechanism. Asking a stranger to watch your things moves bystander "
      f"intervention from <b>0%</b> to <b>{D.TWENTE['request_intervened']}%</b>.</p>"
      "<p>Almost nobody does it, because asking is socially awkward and you have to pick "
      "someone, catch their eye and interrupt them. That awkwardness is the entire "
      "addressable problem, and it is a user-experience problem rather than a security "
      "one. A system that brokers the request &mdash; so the asker does not have to be "
      "socially brave and the watcher is explicitly, briefly accountable &mdash; is "
      "targeting the largest measured effect available, in the setting where the "
      "unattended share of theft is highest.</p>")

# ============================================================ SECTION 7 ====

d.h2("9. International: the measurement gap is global", "intl")
d.p("Five national statistical systems were checked for circumstance data. The table below "
    "is what could be extracted. The absence of a single directly comparable international "
    "figure is a genuine result, not a research failure.")

d.table(["Country", "Measure", "Figure", "Base"],
        [[c, m, f"<b>{v}</b>", b] for c, m, v, b, _ in D.INTL],
        title="International measures that bear on unattendedness",
        sub="None of these is a direct measure. The Australian and ICVS figures are the "
            "closest, and both stop short of asking whether the property was left "
            "unattended.",
        source=cite("abs_break", "abs_theft", "cbs_nl", "icvs", "statcan"))

d.p("The ICVS is the nearest thing to an international circumstance measure: across 17 "
    "industrialised countries, only about <b>one in three</b> personal-property thefts "
    "involved the victim carrying the item at the time. The remaining two-thirds is "
    "consistent with this report's central finding, though the residual includes contexts "
    "beyond unattended property and cannot be claimed as a clean measure.")

# ============================================================ SECTION 8 ====

d.h2("10. Limitations", "limits")
d.ul([
    "<b>The central US estimate is a reconstruction, not a count.</b> It depends on "
    "classifying larceny subcategories by guardianship, which is a judgement. The "
    "classification is published in full above and in <code>data_opportunistic.py</code> "
    "so that a reader who disagrees can recompute it.",
    "<b>The strict/broad gap is wide</b> "
    f"({D.STRICT_PCT:.0f}% to {D.BROAD_PCT:.0f}%) because the 'all other larceny' residual "
    "is 29.9% of larceny and the FBI does not decompose it. Narrowing that gap would "
    "require NIBRS microdata analysis beyond this report's scope.",
    "<b>US category data is from 2019.</b> The UCR-to-NIBRS transition broke the "
    "comparable national series; 2019 is the last clean year for the full subcategory "
    "distribution and for the burglary entry split.",
    "<b>UK nature-of-crime bases are small.</b> The lock-status figures rest on unweighted "
    "bases of 195\u2013475 incidents. They are indicative magnitudes, not precise values, "
    "and single-year movements should not be over-read.",
    "<b>The current ONS workbooks no longer ask directly about unattendedness.</b> The "
    "explicit 'was the property left unattended' framing survives only in the offence-"
    "category definition and in the older 2008/09 British Crime Survey questions.",
    "<b>Campus figures have incompatible denominators.</b> Boston University's 90\u201395% "
    "is of reviewed theft reports; UW-Madison's 69% is of textbook thefts; Miami's 'over "
    "half' is of all campus crime. They are not averageable and no average is offered.",
    "<b>Several campus sources are police estimates or prevention messaging</b>, not "
    "audited counts. They are labelled as such in the table and should carry less weight "
    "than the two with real denominators.",
    "<b>The campus field experiments measure exposure and intervention, not theft.</b> "
    "Twente staged thefts; nothing was actually stolen. A 0% intervention rate is not a "
    "100% theft rate \u2014 it is an absence of guardianship, which is a necessary but not "
    "sufficient condition for theft.",
    "<b>Both field experiments are Dutch university libraries.</b> Generalisation to other "
    "countries and campus cultures is untested.",
    "<b>Reporting bias runs underneath everything.</b> Unattended-property theft is the "
    "least-reported theft type, so if anything these figures understate its share.",
    "<b>The item percentages are shares of incidents, not counts of objects.</b> An "
    "incident can involve several item types, so the columns sum above 100% and no "
    "'number of phones stolen' can be derived from them.",
    "<b>The 'other' category is the largest single entry in unattended theft (31.5%)</b>, "
    "so the true item distribution is longer-tailed than the published one and the "
    "clothing ranking is less secure than it looks.",
    "<b>Item bases are small.</b> Even pooled over three years the unattended items table "
    "rests on 539 unweighted incidents; single years are 164\u2013204. Rankings below the "
    "top three or four should not be treated as ordered.",
    "<b>Campus item counts come from two institutions.</b> Boston University and Toronto "
    "agree, but two campuses in two countries is a pattern, not a population estimate, and "
    "the Toronto figures count report entries rather than incidents.",
    "<b>No US item-level distribution for unattended theft exists.</b> FBI Table 23 gives "
    "larceny subtypes, not items; the NIBRS 2019 static tables contain no property-"
    "description-by-offence table, and a live Crime Data Explorer query for a "
    "property-stolen variable returned demographic dimensions instead. This gap was "
    "confirmed rather than assumed.",
])

# ============================================================== SOURCES ====

d.h2("Appendix: sources", "sources")
_rows = []
for k, (label, org, url, kind, year) in sorted(D.SOURCES.items(), key=lambda x: x[1][1]):
    tick = " &#10003;" if k in D.VERIFIED_BY_LEAD else ""
    _rows.append([f"{org}{tick}", f'<a href="{url}">{label}</a>', year, chip(kind)])
d.table(["Organisation", "Publication", "Period", "Type"], _rows,
        title="Primary sources", sub=f"{len(D.SOURCES)} sources, all opened during "
                                     "preparation. A tick marks those the author read "
                                     "personally to verify a load-bearing figure.",
        source="<b>Reproducibility:</b> figures in <code>research/data_opportunistic.py</code>; "
               "charts in <code>research/charts.py</code>; assembled by "
               "<code>research/build_opportunistic.py</code>.")

d.raw('<div class="footer"><p><b>Method.</b> Five parallel research streams: US entry-'
      "method and location statistics, UK nature-of-crime microdata, campus-specific "
      "evidence, criminological theory and field experiments, and international "
      "comparison. Each was required to open primary sources and label every figure "
      "verified or unverified. The author independently verified the FBI burglary entry "
      "split, the larceny distribution, the property-crime base, the NCVS contact "
      "definition, the Home Office unattended-theft definition, and the CSEW incidence "
      "series read directly from the ONS appendix workbook.</p>"
      "<p><b>Rebuild:</b> <code>python3 research/build_opportunistic.py</code>. "
      "<b>Revert:</b> delete <code>research/opportunistic-theft-report.html</code>, "
      "<code>research/data_opportunistic.py</code> and "
      "<code>research/build_opportunistic.py</code>.</p></div>")

_mast = (MASTHEAD.replace("__NSRC__", str(len(D.SOURCES)))
         .replace("__NFIG__", str(d.fig_n)).replace("__NTAB__", str(d.tab_n)))
OUT.write_text(d.html("Theft of unattended property: how big is it, really?", _mast),
               encoding="utf-8")
print(f"wrote {OUT} ({OUT.stat().st_size:,} bytes, {d.fig_n} figures, "
      f"{d.tab_n} tables, {len(D.SOURCES)} sources)")
