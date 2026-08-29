"""Verified source data for the opportunistic (unattended-property) theft report.

Same discipline as data.py: figures are transcribed from primary sources, and
every share that this report *derives* is computed here rather than typed, so
the arithmetic is checkable. `VERIFIED_BY_LEAD` marks sources the lead agent
opened personally.
"""

from __future__ import annotations

SOURCES: dict[str, tuple[str, str, str, str, str]] = {
    "fbi_prop": (
        "Crime in the US 2019 — Property Crime", "FBI Uniform Crime Reporting",
        "https://ucr.fbi.gov/crime-in-the-u.s/2019/crime-in-the-u.s.-2019/topic-pages/property-crime",
        "official", "2019"),
    "fbi_larceny": (
        "Crime in the US 2019 — Larceny-theft", "FBI Uniform Crime Reporting",
        "https://ucr.fbi.gov/crime-in-the-u.s/2019/crime-in-the-u.s.-2019/topic-pages/larceny-theft",
        "official", "2019"),
    "fbi_burg19": (
        "Crime in the US 2019 — Burglary", "FBI Uniform Crime Reporting",
        "https://ucr.fbi.gov/crime-in-the-u.s/2019/crime-in-the-u.s.-2019/topic-pages/burglary",
        "official", "2019"),
    "fbi_burg18": (
        "Crime in the US 2018 — Burglary", "FBI Uniform Crime Reporting",
        "https://ucr.fbi.gov/crime-in-the-u.s/2018/crime-in-the-u.s.-2018/topic-pages/burglary",
        "official", "2018"),
    "nibrs_loc": (
        "NIBRS 2019 — Crimes Against Property Offenses by Location",
        "FBI Uniform Crime Reporting",
        "https://ucr.fbi.gov/nibrs/2019/tables/pdfs/"
        "crimes_against_property_offenses_offense_category_by_location_2019.pdf",
        "official", "2019"),
    "nibrs_time": (
        "NIBRS 2019 — Crimes Against Property Incidents by Time of Day",
        "FBI Uniform Crime Reporting",
        "https://ucr.fbi.gov/nibrs/2019/tables/pdfs/"
        "crimes_against_property_incidents_offense_category_by_time_of_day_2019.pdf",
        "official", "2019"),
    "bjs": (
        "Criminal Victimization, 2023", "US Bureau of Justice Statistics (NCVS)",
        "https://bjs.ojp.gov/document/cv23.pdf", "official", "2023"),
    "ons_appx": (
        "Crime in England and Wales: Appendix tables, Table A1a",
        "UK Office for National Statistics",
        "https://www.ons.gov.uk/file?uri=/peoplepopulationandcommunity/crimeandjustice/"
        "datasets/crimeinenglandandwalesappendixtables/yearendingmarch2026/"
        "appendixtablesyemar2026.xlsx", "official", "2026"),
    "bcs0809": (
        "Crime in England and Wales 2008/09, Volume 1 (HOSB 11/09)",
        "UK Home Office / British Crime Survey",
        "https://www.cl.cam.ac.uk/archive/rja14/Papers/hosb0810.pdf", "official", "2009"),
    "ons_veh": (
        "Nature of crime: vehicle-related theft, Tables 3a & 3c",
        "UK Office for National Statistics",
        "https://www.ons.gov.uk/file?uri=/peoplepopulationandcommunity/crimeandjustice/"
        "datasets/natureofcrimevehiclerelatedtheft/yearendingmarch2025/"
        "nocvehiclethefttables202425.xlsx", "official", "2024/25"),
    "ons_bike": (
        "Nature of crime: bicycle theft, Tables 2 & 6",
        "UK Office for National Statistics",
        "https://www.ons.gov.uk/file?uri=/peoplepopulationandcommunity/crimeandjustice/"
        "datasets/natureofcrimebicycletheft/yearendingmarch2025/nocbicyclethefttables202425.xlsx",
        "official", "2024/25"),
    "ons_burg": (
        "Nature of crime: burglary, Tables 3a & 10a", "UK Office for National Statistics",
        "https://www.ons.gov.uk/file?uri=/peoplepopulationandcommunity/crimeandjustice/"
        "datasets/natureofcrimeburglary/yearending2025/nocburglarytables202425.xlsx",
        "official", "2024/25"),
    "ons_pers": (
        "Nature of crime: personal and other theft, Tables 1b & 2b",
        "UK Office for National Statistics",
        "https://www.ons.gov.uk/file?uri=/peoplepopulationandcommunity/crimeandjustice/"
        "datasets/natureofcrimepersonalandothertheft/yearendingmarch2025/"
        "nocpersonalandotherthefttables202425.xlsx", "official", "2024/25"),
    "felson": (
        "Opportunity Makes the Thief (Police Research Series Paper 98)",
        "Felson & Clarke, UK Home Office",
        "https://popcenter.asu.edu/sites/g/files/litvpz3631/files/library/reading/PDFs/Thief-2.pdf",
        "official", "1998"),
    "cromwell": (
        "Residential Burglary: An Ethnographic Analysis", "Cromwell, Olson & Avary (NIJ)",
        "https://www.ojp.gov/pdffiles1/Digitization/126684NCJRS.pdf", "official", "1990"),
    "hollis": (
        "Guardianship for crime prevention: a critical review",
        "Hollis-Peel, Reynald, van Bavel, Elffers & Welsh",
        "https://research.vu.nl/ws/portalfiles/portal/3089597/285039.pdf", "academic", "2011"),
    "delft": (
        "Laptop Theft in a University Setting can be Avoided with Warnings",
        "Nadeem & Junger, Delft University of Technology",
        "https://arxiv.org/pdf/1907.08083v1", "academic", "2019"),
    "twente": (
        "Stolen in Plain Sight: Laptop Larceny in Academic Libraries",
        "van Dijk, University of Twente",
        "https://essay.utwente.nl/fileshare/file/109788/Thesis%28Final%29.pdf",
        "academic", "2025"),
    "umpd": (
        "Common Types of Crime — Theft", "University of Miami Police Department",
        "https://umpd.miami.edu/campus-safety/common-types-of-crime/theft/index.html",
        "official", "2026"),
    "bu": (
        "Two Students Robbed of Cell Phones (BU Police interview)",
        "Boston University / BU Today",
        "https://www.bu.edu/articles/2010/two-students-robbed-of-cell-phones/",
        "official", "2010"),
    "uwpd": (
        "Textbook Theft Project (Goldstein Award submission)",
        "UW-Madison Police Dept / ASU Center for Problem-Oriented Policing",
        "https://popcenter.asu.edu/sites/g/files/litvpz3631/files/library/awards/goldstein/2008/08-50.pdf",
        "academic", "2008"),
    "qmul": (
        "Safer Campus Project (Goldstein Award submission)",
        "Metropolitan Police Safer Neighbourhood Team / Queen Mary University of London",
        "https://popcenter.asu.edu/sites/g/files/litvpz3631/files/library/awards/goldstein/2011/11-64.pdf",
        "academic", "2011"),
    "utaustin": (
        "Campus Watch report, 21 January 2019",
        "University of Texas at Austin Police Department",
        "https://utdirect.utexas.edu/apps/fasweb/utpd/campuswatch/nlogon/report/8941/",
        "official", "2019"),
    "kstate": (
        "Increased laptop thefts on campus are wake-up call", "Kansas State University IT News",
        "https://blogs.k-state.edu/it-news/2010/07/13/increased-laptop-thefts-on-campus-are-wake-up-call/",
        "official", "2010"),
    "caltech": (
        "Bicycle theft announcement, 7 October 2021", "Caltech Campus Security",
        "https://security.caltech.edu/announcements-listing/66805", "official", "2021"),
    "arizona": (
        "Arrest made in Rec Center thefts", "University of Arizona Police Department",
        "https://uapd.arizona.edu/media-releases/arrest-made-rec-center-thefts",
        "official", "2024"),
    "gatech": (
        "Police discuss crime trends, campus operations",
        "Georgia Institute of Technology Police Department",
        "https://police.gatech.edu/2017-05/police-discuss-crime-trends-campus-operations-inform",
        "official", "2017"),
    "vcu": (
        "Four easy steps to prevent thieves from taking your stuff",
        "Virginia Commonwealth University Police / VCU News",
        "https://news.vcu.edu/article/four-easy-steps-to-prevent-thieves-from-taking-your-stuff",
        "official", "2026"),
    "abs_theft": (
        "Crime Victimisation Australia 2017-18 — Other theft",
        "Australian Bureau of Statistics",
        "https://www.abs.gov.au/ausstats/abs@.nsf/Lookup/by%20Subject/4530.0~2017-18~"
        "Main%20Features~Other%20theft~12", "official", "2017/18"),
    "abs_break": (
        "Crime Victimisation Australia 2017-18 — Break-in",
        "Australian Bureau of Statistics",
        "https://www.abs.gov.au/ausstats/abs@.nsf/Lookup/by%20Subject/4530.0~2017-18~"
        "Main%20Features~Break-in%20and%20Attempted%20break-in~9", "official", "2017/18"),
    "cbs_nl": (
        "Veiligheidsmonitor 2023, hoofdstuk 4 — traditionele criminaliteit",
        "Statistics Netherlands (CBS)",
        "https://www.cbs.nl/nl-nl/longread/rapportages/2024/veiligheidsmonitor-2023/"
        "4-traditionele-criminaliteit", "official", "2023"),
    "statcan": (
        "Police-reported crime statistics in Canada, Table 1", "Statistics Canada",
        "https://www150.statcan.gc.ca/n1/pub/85-002-x/2025001/article/00005/tbl/tbl01-eng.htm",
        "official", "2023"),
    "icvs": (
        "Criminal Victimisation in Seventeen Industrialised Countries (ICVS)",
        "Van Kesteren, Mayhew & Nieuwbeerta, WODC",
        "https://static.prisonpolicy.org/scans/crimvictin17indcountries.pdf",
        "academic", "2000"),
}

VERIFIED_BY_LEAD = {"fbi_prop", "fbi_larceny", "fbi_burg19", "bjs", "ons_appx", "bcs0809"}

# ============================================== US: the core decomposition ==
PROPERTY_CRIME_2019 = 6_925_677
LARCENY_2019 = 5_086_096
BURGLARY_2019 = 1_117_696
MVT_2019 = PROPERTY_CRIME_2019 - LARCENY_2019 - BURGLARY_2019   # 721,885

LARCENY_MIX = {
    "Theft from motor vehicle (not accessories)": 27.0,
    "Shoplifting": 22.2,
    "Theft from building": 10.0,
    "Motor vehicle parts & accessories": 6.5,
    "Bicycle theft": 3.1,
    "Pocket-picking": 0.6,
    "Purse-snatching": 0.4,
    "Theft from coin-operated machine": 0.2,
    "All other larceny": 29.9,
}

# Guardianship classification of each larceny subcategory. This is the report's
# one analytical judgement and it is stated openly rather than buried.
GUARDIANSHIP_CLASS = {
    "Theft from motor vehicle (not accessories)": "unattended",
    "Motor vehicle parts & accessories": "unattended",
    "Theft from building": "unattended",
    "Bicycle theft": "unattended",
    "Theft from coin-operated machine": "unattended",
    "Shoplifting": "retail",
    "Pocket-picking": "contact",
    "Purse-snatching": "contact",
    "All other larceny": "mixed",
}
CLASS_LABEL = {
    "unattended": "Property left in a place, owner absent",
    "retail": "Retail stock, staff present",
    "contact": "Taken from the person's body",
    "mixed": "Unclassifiable residual ('all other larceny')",
}

_g = lambda cls: sum(v for k, v in LARCENY_MIX.items() if GUARDIANSHIP_CLASS[k] == cls)  # noqa: E731
LARC_UNATTENDED = _g("unattended")   # 46.8
LARC_RETAIL = _g("retail")           # 22.2
LARC_CONTACT = _g("contact")         # 1.0
LARC_MIXED = _g("mixed")             # 29.9
LARC_NOT_CONTACT = 100.0 - LARC_CONTACT

# Burglary by type of entry (percent of estimated burglaries).
BURG_ENTRY = {
    "2019": {"Forcible entry": 55.7, "Unlawful entry, no force": 37.8,
             "Attempted forcible entry": 6.5, "base": BURGLARY_2019},
    "2018": {"Forcible entry": 56.7, "Unlawful entry, no force": 36.7,
             "Attempted forcible entry": 6.6, "base": 1_230_149},
}
BURG_RESIDENTIAL_2019 = 62.8
BURG_NOFORCE_ABS = BURGLARY_2019 * BURG_ENTRY["2019"]["Unlawful entry, no force"] / 100

# Bounded estimate of unattended-property theft as a share of all property crime.
STRICT_ABS = LARCENY_2019 * LARC_UNATTENDED / 100 + BURG_NOFORCE_ABS
BROAD_ABS = (LARCENY_2019 * (LARC_UNATTENDED + LARC_MIXED) / 100
             + BURG_NOFORCE_ABS + MVT_2019)
CONTACT_ABS = LARCENY_2019 * LARC_CONTACT / 100
STRICT_PCT = 100 * STRICT_ABS / PROPERTY_CRIME_2019
BROAD_PCT = 100 * BROAD_ABS / PROPERTY_CRIME_2019
CONTACT_PCT = 100 * CONTACT_ABS / PROPERTY_CRIME_2019
RATIO_LO = STRICT_ABS / CONTACT_ABS
RATIO_HI = BROAD_ABS / CONTACT_ABS

# NCVS 2023: "other theft" is defined as taking WITHOUT personal contact.
NCVS_PROPERTY = 13_637_450
NCVS_OTHER_THEFT = 11_081_650
NCVS_OTHER_SHARE = 100 * NCVS_OTHER_THEFT / NCVS_PROPERTY

# ==================================================== NIBRS location & time ==
NIBRS_LARCENY_BASE = 2_193_678
NIBRS_LOCATIONS = [
    ("Residence / home", 714_568), ("Department or discount store", 277_713),
    ("Parking lot, drop lot or garage", 253_640),
    ("Highway, road, alley, street, sidewalk", 150_028),
    ("Grocery or supermarket", 119_834), ("Other / unknown", 109_767),
    ("Convenience store", 85_544), ("Specialty store", 76_633),
    ("Commercial or office building", 55_462), ("Service or gas station", 41_795),
    ("Restaurant", 40_641), ("Hotel or motel", 31_300),
    ("Drug store, doctor's office, hospital", 26_220), ("Construction site", 18_629),
    ("School — elementary or secondary", 18_292),
    ("School — college or university", 13_888), ("Park or playground", 13_123),
    ("Field or woods", 11_801),
]
NIBRS_TIME = {"larceny": {"AM": 756_139, "PM": 1_401_287, "Unknown": 36_252,
                          "base": 2_193_678},
              "burglary": {"AM": 213_632, "PM": 252_451, "Unknown": 10_466,
                           "base": 476_549}}

# ============================================================= UK evidence ==
# Home Office definition, verified verbatim in the 2008/09 BCS report:
UK_DEFINITION = ("Other theft of personal property covers thefts of unattended "
                 "property where no force is used")

# CSEW incidence, thousands of incidents (Table A1a).
UK_TREND = [
    ("2016/17", 640, 370), ("2017/18", 655, 425), ("2018/19", 739, 447),
    ("2019/20", 612, 367), ("2022/23", 425, 247), ("2023/24", 446, 347),
    ("2024/25", 432, 467), ("2025/26", 344, 361),
]  # (period, other theft of personal property [unattended], theft from the person)

UK_UNLOCKED = [
    ("Theft from a vehicle — door was not locked", 52.8, 475, "ons_veh"),
    ("All vehicle-related theft — door was not locked", 46.4, 311, "ons_veh"),
    ("Stolen bicycles that were not locked", 45.4, 195, "ons_bike"),
    ("Domestic burglary — door was not locked", 14.2, 245, "ons_burg"),
    ("Domestic burglary — window open or pushable", 4.2, 245, "ons_burg"),
]
UK_BURG_NOBODY_HOME = 36.7
UK_BIKE_UNLOCKED_WHY = [
    ("Never thought about it", 29.6), ("Thought the area was safe", 23.9),
    ("Forgot", 15.9), ("Had no lock", 11.1), ("Nowhere to lock it", 8.8),
    ("It was in a locked building", 8.7),
]
UK_BIKE_UNLOCKED_BASE = 89
UK_OTHERTHEFT_LOCATION = [
    ("Other", 40.0), ("Inside a workplace", 16.6), ("Inside another building", 9.5),
    ("In or around public entertainment", 9.2), ("Street", 7.9), ("Inside a pub", 6.2),
    ("In or around public transport", 4.5),
    ("Inside a school, college or university", 2.6), ("Inside a shop", 2.3),
]
UK_OTHERTHEFT_BASE = 210
UK_OTHERTHEFT_TIMING = {"weekday": 74.9, "weekend": 25.1,
                        "daylight": 62.3, "dark": 36.4, "dawn_dusk": 1.3}
BCS_RESPONSIBILITY = 26      # % of other-theft incidents where victim took some responsibility
BCS_RESP_BASE = 888
BCS_LAPSE = [("Failed to lock property away", 48), ("Left it open or visible", 43),
             ("Failed to lock or bolt a door or window", 15),
             ("Left a door or window open", 2)]
BCS_LAPSE_BASE = 261

# ======================================================= campus (Q2) =======
# (institution, figure text, numeric low, numeric high or None, what it measures, source key)
CAMPUS = [
    ("Boston University", "90–95%", 90, 95,
     "Share of theft reports reviewed by BU Police that are 'unattendeds' — a laptop or "
     "phone left at a desk, or a room or office left unlocked", "bu"),
    ("Kansas State University", "\u201cVirtually every theft\u201d", None, None,
     "University IT/security assessment of a laptop theft wave: unsecured laptops in "
     "offices, labs, classrooms and residence halls with open doors", "kstate"),
    ("Queen Mary University of London", "~91%", None, None,
     "Campus burglaries entering via windows (64%) or doors (27%); of these only one "
     "window and one door were forced, the rest were unlocked or open", "qmul"),
    ("UW-Madison", "69%", 69, None,
     "Share of all campus textbook thefts taken from unattended backpacks or books",
     "uwpd"),
    ("University of Miami", "over half", None, None,
     "Theft of unattended or unsecured property as a share of ALL crime on the Coral "
     "Gables campus (not just theft)", "umpd"),
    ("UT Austin", "\u201cthe majority\u201d", None, None,
     "Campus Watch: 'The majority of these crimes have a common factor: property was "
     "left unattended'", "utaustin"),
    ("Caltech", "\u201cvast majority\u201d", None, None,
     "Of eight bicycles stolen in a three-week series, the vast majority were unlocked, "
     "improperly locked or inadequately locked", "caltech"),
    ("Georgia Tech", "7 bikes", None, None,
     "Bicycles stolen in a reported series that were 'not locked at all'", "gatech"),
]
QMUL = {"window": 64, "door": 27, "laptops_targeted": 90,
        "burglary_before": 12, "burglary_after": 0,
        "bike_before": 7, "bike_after": 0,
        "total_before": 45, "total_after": 16}
UW_MECHANISM = [("Unattended backpacks or books", 69), ("Locker theft", 21),
                ("Bookstore theft", 6), ("Theft from a vehicle", 4)]

# Field experiments on campus.
DELFT = {"n_total": 220, "n_phase": 110, "unattended_control": 75.5,
         "unattended_warning": 59.1, "unattended_overall": 67.3,
         "insecure_control": 44.6, "insecure_warning": 46.2}
TWENTE = {"no_request_n": 54, "no_request_intervened": 0,
          "request_n": 43, "request_intervened": 84,
          "total_obs": 97, "peer_thief": 33, "authority_thief": 42,
          "by_time": [("09:00–11:00", 41), ("11:01–13:00", 16),
                      ("13:01–15:00", 58), ("15:01–17:00", 33)]}
KSTATE_SECONDS = 6
HOLLIS_RANGE = (0, 40)

# ==================================================== international ========
INTL = [
    ("Australia", "Break-ins where property was stolen", "73%",
     "of 231,100 households experiencing a break-in", "abs_break"),
    ("Australia", "Other-theft incidents occurring at the home", "60%",
     "of 236,500 households experiencing other theft", "abs_theft"),
    ("Netherlands", "Bicycle-theft victims in a year", "5.0%",
     "of 182,000 surveyed residents aged 15+", "cbs_nl"),
    ("Netherlands", "Bicycles stolen in a year", "928,000",
     "national estimate from the Safety Monitor", "cbs_nl"),
    ("17 countries", "Personal-property thefts where the victim was carrying the item",
     "~1 in 3", "of personal-property thefts across ICVS countries", "icvs"),
    ("Canada", "Police-reported breaking and entering", "105,442",
     "incidents; no method-of-entry field published", "statcan"),
]

# ============================================ WHAT GETS TAKEN (items) ======
# CSEW "items stolen" tables. Percentages are of INCIDENTS and an incident can
# involve several item types, so columns sum above 100. Pooled over the three
# most recent survey years to stabilise small annual bases; weights are the
# published unweighted bases.
ITEMS_PAIRED = [
    ("Mobile phone", 9.9, 48.2), ("Clothing", 16.8, 1.6),
    ("Cash / foreign currency", 13.0, 16.0),
    ("Computers & other electrical goods", 9.5, 2.8),
    ("Purse or wallet", 8.6, 26.5), ("Credit, debit or store cards", 8.5, 18.1),
    ("Tools or work materials", 8.2, 0.1),
    ("Food, toiletries, cigarettes", 7.4, 0.3),
    ("Briefcase, handbag or shopping bag", 6.4, 6.2),
    ("Documents", 4.3, 2.2), ("Jewellery or watches", 2.8, 1.1),
    ("House keys", 2.4, 0.7), ("Car keys", 1.0, 0.8),
    ("Other", 31.5, 6.2),
]
ITEMS_BASE_UNATTENDED = 539     # pooled unweighted incidents, 2022/23-2024/25
ITEMS_BASE_CONTACT = 302
ITEMS_YEARS = "2022/23 to 2024/25"

# Single latest year, for readers who want an unpooled cut (base 164 / 120).
ITEMS_LATEST_UNATTENDED = [
    ("Clothing", 19.6), ("Cash / foreign currency", 12.3),
    ("Computers & other electrical goods", 12.1),
    ("Briefcase, handbag or shopping bag", 7.5),
    ("Credit, debit or store cards", 7.4), ("Tools or work materials", 6.8),
    ("Documents", 6.6), ("Purse or wallet", 6.5),
    ("Food, toiletries, cigarettes", 6.0), ("Mobile phone", 5.4),
]
ITEMS_LATEST_BASE = 164

# Cost of stolen items, year ending March 2025.
COST = {"unattended": {"mean": 486.76, "median": 80, "base": 160,
                       "over_1000": 17.3, "under_50": 32.4},
        "contact": {"mean": 498.54, "median": 400, "base": 121,
                    "over_1000": 26.0, "under_50": 18.6}}

# Items taken in thefts FROM vehicles (the largest single unattended stream).
VEHICLE_ITEMS = [
    ("Valuables (jewellery, bags, cash, cards, clothes, documents)", 42.9),
    ("Exterior fittings", 19.7), ("Glasses or sunglasses", 10.9),
    ("Tools", 10.7), ("Household items and gadgets", 7.3),
    ("Other vehicle parts", 5.3), ("Electrical equipment", 4.9),
    ("Food, toiletries, cigarettes", 4.8), ("Car radio", 1.2),
    ("Mobile phone", 0.6),
]
VEHICLE_ITEMS_BASE = 451
VEHICLE_COST = {"mean": 467.85, "median": 90, "base": 438}

# FBI Table 23, Offense Analysis 2019: larceny subtype offences and mean value.
# 13,848 agencies, estimated population 273,654,275. Counts sum exactly to the
# published total, which is a useful internal check on transcription.
T23_AGENCIES = 13_848
T23_POPULATION = 273_654_275
T23_TOTAL_OFFENCES = 4_132_566
T23_AVG_VALUE = 1_162
T23 = {
    "Theft from motor vehicles": (1_121_083, 1_012, "unattended"),
    "Theft from buildings": (404_734, 1_663, "unattended"),
    "Motor vehicle accessories": (264_720, 690, "unattended"),
    "Bicycles": (125_136, 569, "unattended"),
    "Coin-operated machines": (9_204, 829, "unattended"),
    "Shoplifting": (904_975, 338, "retail"),
    "Pocket-picking": (23_954, 1_235, "contact"),
    "Purse-snatching": (15_087, 651, "contact"),
    "All other larceny": (1_263_673, 1_888, "residual"),
}


def t23_class(cls: str) -> tuple[int, int, float]:
    """Return (offences, total value $, mean value $) for a guardianship class."""
    n = sum(v[0] for v in T23.values() if v[2] == cls)
    val = sum(v[0] * v[1] for v in T23.values() if v[2] == cls)
    return n, val, val / n


T23_UNATT_N, T23_UNATT_VAL, T23_UNATT_AVG = t23_class("unattended")
T23_CONTACT_N, T23_CONTACT_VAL, T23_CONTACT_AVG = t23_class("contact")
T23_RETAIL_N, T23_RETAIL_VAL, T23_RETAIL_AVG = t23_class("retail")
T23_UNATT_SHARE = 100 * T23_UNATT_N / T23_TOTAL_OFFENCES
T23_VALUE_RATIO = T23_UNATT_VAL / T23_CONTACT_VAL

# Campus item counts.
BU_ITEMS = [("Bicycles", 120), ("Computers, laptops, tablets", 61),
            ("Mobile phones", 18)]
BU_LARCENIES = 351
BU_CARDS = 152
BU_PERIOD = "1 September 2018 to 31 August 2019"
UOFT_RANK = ["Bicycles", "Money", "Laptops", "Bags", "Phones"]
UOFT_THEFT_REPORTS = 1_606
UOFT_BIKE_SITES = [("Athletic Centre", 49), ("Charles Street housing", 30),
                   ("Bahen Centre", 23), ("Robarts Library", 13)]
UOFT_LAPTOP_SITES = [("Bahen Centre", 20), ("Robarts Library", 19),
                     ("Sidney Smith Hall", 11), ("Gerstein Library", 9)]
UOFT_LOCKER_REPORTS = 27

SOURCES.update({
    "ons_items": (
        "Nature of crime: personal and other theft, Tables 3a, 3b, 4a, 4b",
        "UK Office for National Statistics",
        "https://www.ons.gov.uk/file?uri=/peoplepopulationandcommunity/crimeandjustice/"
        "datasets/natureofcrimepersonalandothertheft/yearendingmarch2025/"
        "nocpersonalandotherthefttables202425.xlsx", "official", "2024/25"),
    "ons_vehitems": (
        "Nature of crime: vehicle-related theft, Tables 6 and 7b",
        "UK Office for National Statistics",
        "https://www.ons.gov.uk/file?uri=/peoplepopulationandcommunity/crimeandjustice/"
        "datasets/natureofcrimevehiclerelatedtheft/yearendingmarch2025/"
        "nocvehiclethefttables202425.xlsx", "official", "2024/25"),
    "fbi_t23": (
        "Crime in the US 2019 — Table 23, Offense Analysis",
        "FBI Uniform Crime Reporting",
        "https://ucr.fbi.gov/crime-in-the-u.s/2019/crime-in-the-u.s.-2019/tables/table-23",
        "official", "2019"),
    "bu_items": (
        "Safety 101: campus crime figures", "Boston University / BU Today",
        "https://www.bu.edu/articles/2019/safety-101/", "official", "2019"),
    "uoft": (
        "Where campus crimes happen, mapped",
        "The Varsity (University of Toronto student newspaper), from Campus Safety "
        "Activity Reports",
        "https://thevarsity.ca/2026/03/23/where-campus-crimes-happen-mapped/",
        "news", "2026"),
})
VERIFIED_BY_LEAD.update({"ons_items", "fbi_t23"})

# ==================================== WHERE STOLEN GOODS GO (disposal) =====
# DUMA (Drug Use Monitoring in Australia) stolen-goods survey addenda, seven
# waves 2002-2017, N=6,079 arrestees. Percentages are of POLICE DETAINEE
# RESPONDENTS reporting what they *usually* do, not of offences or of items.
DUMA_N = 6_079
DUMA_WAVES = 7
DUMA_AGE, DUMA_MALE, DUMA_STOLE_12M = 31, 84, 21
DUMA_ROUTE_TREND = [("2002", 44, 20), ("2017", 11, 64)]   # (year, sold, kept/used)
DUMA_ROUTE_AVG = [("Keeping or using them", None), ("Selling them", None),
                  ("Swapping for drugs", 13), ("Consuming them", 9), ("Other", 10)]
DUMA_SOLD_2002, DUMA_SOLD_2017 = 44, 11
DUMA_KEPT_2002, DUMA_KEPT_2017 = 20, 64
DUMA_SPEND_2017 = 1
DUMA_OUTLETS = [           # average share 2003 onwards
    ("Drug dealer", 44), ("Family member, friend or acquaintance", 22),
    ("Fence", 11), ("Stranger", 10), ("Other business", 6),
    ("Pawnbroker or second-hand dealer", 4), ("Other", 3),
]
DUMA_DRUG_DEALER_2017 = 51
DUMA_INTERNET = [("2012", 2), ("2017", 9)]
DUMA_UNKNOWN_FATE = (21, 35)     # respondents who did not know what happened after sale
DUMA_PRICE = [("About one-third of what they're worth", 43),
              ("About half of what they're worth", 19)]
DUMA_PRICE_THIRD_2002, DUMA_PRICE_THIRD_2017 = 45, 40
DUMA_PRICE_HALF_2017 = 26

# NSW imprisoned-burglar interviews (BOCSAR).
BOCSAR_N = 267
BOCSAR = {"swapped_for_drugs": 70, "stole_to_order": 80,
          "drugs_within_1h": 50, "drugs_within_24h": 90}

# Sutton's six stolen-goods market types, as reproduced by the ASU POP Center.
MARKET_TYPES = [
    ("Commercial fence supplies",
     "Thieves sell to commercial fences operating out of shops \u2014 jewellers, "
     "pawnbrokers, second-hand dealers."),
    ("Residential fence supplies",
     "Thieves sell to fences at the fences' homes, particularly electrical goods."),
    ("Network sales",
     "Goods are passed along a chain, each participant adding a little to the price "
     "until a consumer is found."),
    ("Commercial sales",
     "Commercial fences pose as legitimate business owners and sell on to innocent "
     "consumers."),
    ("Hawking",
     "Thieves sell directly to consumers in pubs and bars or door to door \u2014 "
     "cigarettes, toiletries, clothes, food."),
    ("eSelling",
     "Sale through online marketplaces and auction sites, reaching buyers the thief "
     "could not otherwise access."),
]

# Public exposure to stolen-goods markets (nationally representative surveys).
BCS_OFFERED = 11        # % offered stolen goods in the previous year
BCS_BOUGHT_5Y = 11      # % who bought stolen goods in the previous five years
YLS_HANDLING = 49       # % of 14-25s admitting offending who also admitted handling

# Drug-driven acquisitive crime.
DRUG_ACQUISITIVE_SHARE = 45      # % of acquisitive crime by crack/opiate users
POP_ARRESTED_THIEVES_DRUGS = 29  # % of arrested thieves who are heroin/cocaine users

# Home Office "Crime and the value of stolen goods" (2015), CSEW 2013/14.
# % of household and personal acquisitive incidents with loss involving each item.
# `resale` flags whether the item plausibly enters a resale market at all.
HORR81_ITEMS = [
    ("Cash", 16.7, False), ("Vehicle parts / accessories", 14.6, True),
    ("Mobile phone", 13.1, True), ("Bicycle", 11.9, True),
    ("Garden furniture / equipment", 9.6, True), ("Plastic card", 8.2, False),
    ("Purse or wallet", 7.7, False), ("Clothes", 6.9, True),
    ("Other", 6.5, True), ("Tools", 4.8, True),
    ("Computer equipment", 3.8, True), ("Jewellery / watches", 3.8, True),
    ("Bag or briefcase", 3.1, True), ("Documents", 3.1, False),
    ("Groceries, alcohol, cigarettes", 2.5, False),
    ("Various household items", 2.2, True),
    ("Portable audio or video device", 1.8, True), ("House keys", 1.8, False),
    ("Car or van", 1.6, True), ("Scrap metal", 1.6, True),
]
HORR81_CASH_TOP_SINCE = 1981
SCHNEIDER_N = 50   # prolific offenders, Shropshire; ease of disposal the top reason

# Cutting off a disposal channel: the UK scrap-metal natural experiment.
SCRAP = {"pre": 47.04, "post": 23.70, "raw_pct": 50, "ci": (45, 56),
         "adj_level": -18.21, "adj_pct": 38, "final_level": -14.48,
         "final_pct": 30, "ena_coverage": 6}

# Phones.
PHONE_BLOCK_48H = 90            # % of reported-stolen UK handsets blocked within 48h
MET_PHONES = {"trafficked": 40_000, "share_london": 40, "recovered": 10_000,
              "victims": 1_000, "paid_street": 300, "sold_china": 5_000}

# Bicycles (non-probability North American survey, n=1,823).
BIKE_SURVEY_N = 1_823
BIKE_RECOVERED = 15             # % of stolen bikes recovered
BIKE_FOUND_ONLINE = 27          # % OF RECOVERED bikes found being sold online

SOURCES.update({
    "duma": (
        "Fencing markets and offender target selection (Psychology, Crime & Law)",
        "Clare, Morgan, Lee & Voce, Drug Use Monitoring in Australia",
        "https://prohic.nl/wp-content/uploads/2022/07/"
        "417-FencingMarketOffenderTargetSelectionAUS.May2022.pdf", "academic", "2022"),
    "bocsar": (
        "The stolen goods market in New South Wales (media release r44)",
        "NSW Bureau of Crime Statistics and Research",
        "https://bocsar.nsw.gov.au/media/1998/mr-r44.html", "official", "2001"),
    "mra": (
        "Tackling Theft with the Market Reduction Approach (Crime Reduction Research "
        "Series Paper 8)", "Sutton, Schneider & Hetherington, UK Home Office",
        "https://webdoc.sub.gwdg.de/ebook/serien/n/CRRS/8-fr.pdf", "official", "2001"),
    "popgoods": (
        "Problem-Oriented Guides for Police: Stolen Goods Markets",
        "ASU Center for Problem-Oriented Policing",
        "https://popcenter.asu.edu/content/stolen-goods-markets-0", "academic", "2024"),
    "horr81": (
        "Crime and the value of stolen goods (Research Report 81)", "UK Home Office",
        "https://assets.publishing.service.gov.uk/government/uploads/system/uploads/"
        "attachment_data/file/468003/horr81.pdf", "official", "2015"),
    "horr80": (
        "Reducing metal theft: an evaluation (Research Report 80)", "UK Home Office",
        "https://assets.publishing.service.gov.uk/government/uploads/system/uploads/"
        "attachment_data/file/398511/horr80.pdf", "official", "2015"),
    "metphone": (
        "Three plead guilty following major mobile phone theft investigation",
        "Metropolitan Police",
        "https://news.met.police.uk/pressreleases/three-plead-guilty-following-major-"
        "met-mobile-phone-theft-investigation-3445768", "official", "2026"),
    "phoneblock": (
        "New code of practice to close multi-million pound stolen phones loophole",
        "UK Home Office", "https://www.gov.uk/government/news/new-code-of-practice-to-"
        "close-multi-million-pound-stolen-phones-loop", "official", "2010"),
    "bikefind": (
        "Patterns in bike theft and recovery", "Findings (peer-reviewed)",
        "https://findingspress.org/article/90056-patterns-in-bike-theft-and-recovery",
        "academic", "2023"),
    "nrf": (
        "NRF updates crime report after faulty numbers", "Retail Dive",
        "https://www.retaildive.com/news/nrf-updates-crime-report-faulty-numbers/701396/",
        "news", "2023"),
    "inform": (
        "15 U.S.C. 45f — INFORM Consumers Act", "United States Congress",
        "https://uscode.house.gov/view.xhtml?edition=prelim&num=0&req=granuleid"
        "%3AUSC-prelim-title15-section45f", "official", "2023"),
})
VERIFIED_BY_LEAD.update({"duma", "horr81", "popgoods"})

# Demand side: CSEW respondents offered suspected stolen goods (horr81 Annex B).
# Nationally representative; unweighted bases exclude don't-know/refused.
OFFERED_TREND = [   # (period, past 5 years %, past 12 months %, base)
    ("2001/02", 19.0, 9.9, 2_612), ("2002/03", 20.0, 10.6, 11_751),
    ("2003/04", 20.0, 8.7, 752), ("2005/06", 14.4, 8.0, 6_753),
    ("2006/07", 12.8, 6.1, 467), ("2007/08", 14.3, 7.9, 6_613),
]
OCJS_BOUGHT, OCJS_SOLD = 7, 2.7      # % of adults, prior year (Sutton et al 2008)
BCS_NEIGHBOURS_SOME, BCS_NEIGHBOURS_ALOT = 70, 21
