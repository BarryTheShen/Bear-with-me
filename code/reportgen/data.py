"""Verified source data for the property-loss and theft research report.

Every figure below was read out of the cited primary source. `VERIFIED_BY_LEAD`
marks figures the lead agent opened personally rather than accepting from a
research subagent. Derived values are computed here, never hand-typed, so the
arithmetic in the report is reproducible.
"""

from __future__ import annotations

# --------------------------------------------------------------- sources ---
# key -> (short label, organisation, url, type, year)
SOURCES: dict[str, tuple[str, str, str, str, str]] = {
    "fbi_larceny": (
        "Crime in the US 2019 — Larceny-theft", "FBI Uniform Crime Reporting",
        "https://ucr.fbi.gov/crime-in-the-u.s/2019/crime-in-the-u.s.-2019/topic-pages/larceny-theft",
        "official", "2019"),
    "fbi_clear": (
        "Crime in the US 2019 — Clearances", "FBI Uniform Crime Reporting",
        "https://ucr.fbi.gov/crime-in-the-u.s/2019/crime-in-the-u.s.-2019/topic-pages/clearances",
        "official", "2019"),
    "fbi_t24": (
        "Crime in the US 2019 — Table 24, Property Stolen and Recovered",
        "FBI Uniform Crime Reporting",
        "https://ucr.fbi.gov/crime-in-the-u.s/2019/crime-in-the-u.s.-2019/tables/table-24",
        "official", "2019"),
    "bjs": (
        "Criminal Victimization, 2023 (NCJ 309235)",
        "US Bureau of Justice Statistics, National Crime Victimization Survey",
        "https://bjs.ojp.gov/document/cv23.pdf", "official", "2023"),
    "ons": (
        "Crime in England and Wales, year ending March 2024",
        "UK Office for National Statistics",
        "https://www.ons.gov.uk/peoplepopulationandcommunity/crimeandjustice/bulletins/"
        "crimeinenglandandwales/yearendingmarch2024", "official", "2024"),
    "ons_d10": (
        "Annual trend and demographic tables, Table D10 (reporting rates)",
        "UK Office for National Statistics",
        "https://www.ons.gov.uk/file?uri=/peoplepopulationandcommunity/crimeandjustice/"
        "datasets/crimeinenglandandwalesannualtrendanddemographictables/current/"
        "annualtrendanddemographictablesmarch24final.xlsx", "official", "2024"),
    "eurostat": (
        "Crime statistics — police-recorded offences", "Eurostat",
        "https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Crime_statistics",
        "official", "2024"),
    "tfl": (
        "Lost Property Office transparency data FY2017-18-19", "Transport for London",
        "https://foi.tfl.gov.uk/FOI-1592-2223/lost-property-office-transparency-data-FY2017-18-19.pdf",
        "official", "2018/19"),
    "mta_mnr": (
        "Lost and Found — Metro-North Railroad FAQs", "Metropolitan Transportation Authority",
        "https://www.mta.info/lost-and-found/metro-north-railroad/faqs", "official", "2025"),
    "cohn": (
        "Civic honesty around the globe, Science 365(6448):70-73",
        "Cohn, Marechal, Tannenbaum & Zund",
        "https://davetannenbaum.github.io/documents/Cohn2019.pdf", "academic", "2019"),
    "sita": (
        "Baggage IT Insights press release (WorldTracer data)", "SITA",
        "https://www.sita.aero/about-us/pressroom/news-releases/more-air-passengers-than-ever-"
        "with-one-of-the-lowest-rates-of-mishandled-baggage-thanks-to-tech-investments/",
        "vendor", "2024"),
    "nces": (
        "Criminal Incidents at Postsecondary Institutions (Condition of Education)",
        "US Dept of Education, NCES",
        "https://nces.ed.gov/programs/coe/indicator/a21/postsecondary-criminal-incidents",
        "official", "2021"),
    "fsa": (
        "FSA Handbook 2024-25, Appendix E — Institutional Reporting and Disclosure",
        "US Dept of Education, Federal Student Aid",
        "https://fsapartners.ed.gov/knowledge-center/fsa-handbook/2024-2025/appendices/"
        "appx-e-institutional-reporting-and-disclosure-requirements", "official", "2024"),
    "gtpd": (
        "2023 Annual Report", "Georgia Institute of Technology Police Department",
        "https://police.gatech.edu/sites/default/files/2025-02/GTPD%202023%20AR.PRINT-pages%20%282%29.pdf",
        "official", "2023"),
    "usc": (
        "Annual Security and Fire Safety Report 2023",
        "University of Southern California Dept of Public Safety",
        "https://dps.usc.edu/wp-content/uploads/2023/09/USC-ASR-2023-ADA-Upated-9.25_Reduced-Size.pdf",
        "official", "2022"),
    "umpd": (
        "Common Types of Crime — Theft", "University of Miami Police Department",
        "https://umpd.miami.edu/campus-safety/common-types-of-crime/theft/index.html",
        "official", "2026"),
    "uwpd": (
        "Textbook Theft Project (Goldstein Award submission)",
        "UW-Madison Police Dept / ASU Center for Problem-Oriented Policing",
        "https://popcenter.asu.edu/sites/g/files/litvpz3631/files/library/awards/goldstein/2008/08-50.pdf",
        "academic", "2008"),
    "iu": (
        "Bike theft survey results",
        "Indiana University Transportation Demand Management / Center for Survey Research",
        "https://transportation.indiana.edu/about-us/news/bike-theft-survey.html",
        "academic", "2024"),
    "piza": (
        "CCTV surveillance for crime prevention: a 40-year systematic review with "
        "meta-analysis, Criminology & Public Policy 18(1):135-159",
        "Piza, Welsh, Farrington & Thomas",
        "https://prohic.nl/wp-content/uploads/2020/11/2020-04-01-CCTVReviewPizaetal.2019pdf.pdf",
        "academic", "2019"),
    "lighting": (
        "Effectiveness of Street Lighting in Preventing Crime in Public Places",
        "Welsh, Farrington & Douglas (Bra, Swedish National Council for Crime Prevention)",
        "https://bra.se/download/18.47bb43da192711ebb374ea5/1729505968738/"
        "2022_Effectiveness_of_Street_Lighting_in_Preventing_Crime_in_Public_Places.pdf",
        "academic", "2022"),
    "sos": (
        "Secure Our Smartphones Initiative — One Year Later",
        "New York State Office of the Attorney General",
        "https://ag.ny.gov/sites/default/files/reports/SOS_1_YEAR_REPORT.pdf", "official", "2014"),
    "guerette": (
        "Assessing the extent of crime displacement and diffusion of benefits, "
        "Criminology 47(4):1331-1368", "Guerette & Bowers",
        "https://popcenter.asu.edu/sites/g/files/litvpz3631/files/displacement.pdf",
        "academic", "2009"),
    "unodc": (
        "Twenty-five techniques of situational prevention (Cornish & Clarke 2003)",
        "UNODC Education for Justice, Module 2",
        "https://www.unodc.org/documents/e4j/CPCJ/CPCJ_Module_2_Crime_Prevention_-_"
        "table_25_opportunity_reducing_techniques.pdf", "academic", "2003"),
    "craved": (
        "Hot Products: understanding, anticipating and reducing demand for stolen goods",
        "Clarke (Home Office Police Research Series 112)",
        "https://popcenter.asu.edu/sites/g/files/litvpz3631/files/understanding_theft_of_hot_products.pdf",
        "academic", "1999"),
    "findmy": (
        "Who Can Find My Devices? Security and Privacy of Apple's Crowd-Sourced "
        "Bluetooth Location Tracking System, PoPETs 2021(3)",
        "Heinrich, Stute, Kornhuber & Hollick",
        "https://petsymposium.org/popets/2021/popets-2021-0045.pdf", "academic", "2021"),
    "sendmy": (
        "Send My: arbitrary data transmission via Apple's Find My network",
        "Positive Security", "https://positive.security/blog/send-my", "academic", "2021"),
    "ietf": (
        "Detecting Unwanted Location Trackers (draft-ledvina-apple-google-unwanted-trackers-03)",
        "Apple & Google, IETF Internet-Draft (work in progress)",
        "https://www.ietf.org/archive/id/draft-ledvina-apple-google-unwanted-trackers-03.txt",
        "academic", "2026"),
    "pets2006": (
        "Detecting Abandoned Luggage Items in a Public Space (PETS 2006)",
        "Smith, Quelhas & Gatica-Perez",
        "https://publications.idiap.ch/downloads/papers/2006/smith-PETS-2006.pdf",
        "academic", "2006"),
    "apple_sdp": (
        "Use Stolen Device Protection on iPhone", "Apple",
        "https://support.apple.com/guide/iphone/use-stolen-device-protection-iph17105538b/ios",
        "official", "2026"),
    "immobilise": (
        "Celebrating 20 years of Immobilise, the national property register",
        "Secured by Design / Police Crime Prevention Initiatives",
        "https://www.securedbydesign.com/about-us/news/celebrating-20-years-of-immobilise-"
        "the-national-property-register", "official", "2023"),
    "cwru": (
        "Richard's new package room at Wade Commons poses security questions",
        "The Observer (Case Western Reserve University student newspaper)",
        "https://observer.case.edu/richards-new-package-room-at-wade-commons-poses-security-questions/",
        "news", "2017"),
    "homeoffice_cvs": (
        "Crime against businesses: findings from the 2023 Commercial Victimisation Survey",
        "UK Home Office",
        "https://www.gov.uk/government/statistics/crime-against-businesses-findings-from-the-"
        "2023-commercial-victimisation-survey/crime-against-businesses-findings-from-the-2023-"
        "commercial-victimisation-survey", "official", "2023"),
}

VERIFIED_BY_LEAD = {"fbi_larceny", "fbi_clear", "fbi_t24", "bjs", "piza"}

# ---------------------------------------------------- 1. US larceny mix ----
# FBI 2019 larceny-theft figure, percent distribution. Verified by lead.
LARCENY_TOTAL = 5_086_096
LARCENY_RATE_100K = 1549.5
LARCENY_SHARE_OF_PROPERTY = 73.4
LARCENY_MIX = [
    ("All other larceny", 29.9),
    ("Theft from motor vehicle (not accessories)", 27.0),
    ("Shoplifting", 22.2),
    ("Theft from building", 10.0),
    ("Motor vehicle parts & accessories", 6.5),
    ("Bicycle theft", 3.1),
    ("Pocket-picking", 0.6),
    ("Purse-snatching", 0.4),
    ("Theft from coin-operated machine", 0.2),
]

# ------------------------------------------- 2. Clearance / recovery -------
CLEARANCE = [
    ("Murder & non-negligent manslaughter", 61.4),
    ("Aggravated assault", 52.3),
    ("All violent crime", 45.5),
    ("Rape", 32.9),
    ("Robbery", 30.5),
    ("Arson", 23.8),
    ("Larceny-theft", 18.4),
    ("All property crime", 17.2),
    ("Burglary", 14.1),
    ("Motor vehicle theft", 13.8),
]

# FBI Table 24, 2019: 14,165 agencies, estimated population 285,731,352.
T24_AGENCIES = 14_165
T24_POPULATION = 285_731_352
T24 = [  # (property type, stolen $, recovered $, published % recovered)
    ("Locally stolen motor vehicles", 5_752_240_315, 3_228_870_193, 56.1),
    ("Miscellaneous", 3_502_095_818, 453_402_855, 12.9),
    ("Firearms", 116_159_390, 13_495_262, 11.6),
    ("Livestock", 14_350_714, 1_570_468, 10.9),
    ("Consumable goods", 160_368_125, 13_380_144, 8.3),
    ("Clothing and furs", 383_191_187, 31_171_004, 8.1),
    ("Office equipment", 420_417_080, 23_237_884, 5.5),
    ("Household goods", 186_264_170, 8_179_579, 4.4),
    ("Televisions, radios, stereos", 323_393_740, 14_009_033, 4.3),
    ("Jewelry and precious metals", 1_057_763_740, 36_890_088, 3.5),
    ("Currency, notes, etc.", 1_423_559_757, 36_980_933, 2.6),
]
T24_TOTAL_STOLEN = 13_339_804_036
T24_TOTAL_RECOVERED = 3_861_187_443
T24_TOTAL_PCT = 28.9

_veh_s, _veh_r = 5_752_240_315, 3_228_870_193
NONVEHICLE_STOLEN = T24_TOTAL_STOLEN - _veh_s
NONVEHICLE_RECOVERED = T24_TOTAL_RECOVERED - _veh_r
NONVEHICLE_PCT = 100 * NONVEHICLE_RECOVERED / NONVEHICLE_STOLEN
VEHICLE_SHARE_OF_RECOVERED = 100 * _veh_r / T24_TOTAL_RECOVERED

# ------------------------------------------------- 3. NCVS 2023 (BJS) ------
NCVS_2023 = [  # (crime, victimizations, rate per 1,000 households, % reported)
    ("Other theft", 11_081_650, 83.1, 24.8),
    ("Burglary/trespassing", 1_746_980, 13.1, 42.7),
    ("Burglary", 1_202_830, 9.0, 42.2),
    ("Motor vehicle theft", 808_830, 6.1, 72.4),
]
NCVS_TOTAL = 13_637_450
NCVS_TOTAL_RATE = 102.2
NCVS_TOTAL_REPORTED = 29.9
NCVS_TOTAL_REPORTED_2022 = 31.8
NCVS_VIOLENT_REPORTED = 44.7

# ----------------------------------------------------- 4. UK / Europe ------
ONS = {
    "csew_theft_person": 347_000,
    "csew_theft_person_prev": 247_000,
    "police_theft_person": 131_453,
    "police_theft_total": 1_800_000,
    "police_shoplifting": 443_995,
    "police_theft_vehicle": 193_023,
}
ONS_REPORTING = [  # Table D10, year ending March 2024
    ("Domestic burglary", 57.7),
    ("Stealth theft from the person (pickpocketing)", 42.1),
    ("Bicycle theft", 41.8),
    ("All theft offences", 34.1),
    ("Theft from the person (all)", 25.9),
    ("Other theft of personal property", 25.2),
]
EUROSTAT_EU_THEFTS_2024 = 5_261_267
EUROSTAT_RATES = [("France", 1956.01), ("Germany", 1410.44)]

# -------------------------------------------- 5. TfL lost property ---------
TFL_YEAR = "2018/19"
TFL_FOUND = 333_921
TFL_RECLAIMED = 79_861
TFL_ITEMS = [  # (category, found, reclaimed)
    ("Books, documents & cards", 83_230, 12_404),
    ("Clothing", 50_034, 4_828),
    ("Bags", 49_077, 20_544),
    ("Valuables", 38_752, 16_839),
    ("Telephones", 36_742, 17_754),
    ("Miscellaneous", 32_588, 4_314),
    ("Eyewear", 16_125, 1_217),
    ("Keys", 14_069, 1_588),
    ("Umbrellas", 7_646, 178),
    ("Jewellery", 5_658, 195),
]
TFL_SERVICES = [  # (service, found, reclaimed %)
    ("London Buses", 187_446, 22.8),
    ("Underground", 127_963, 25.2),
    ("TfL Rail", 5_229, 16.7),
    ("Overground", 4_331, 27.9),
    ("DLR", 3_215, 38.0),
    ("Taxi", 2_962, 41.9),
    ("Victoria Coach Station", 1_372, 25.1),
]
TFL_PRIOR_YEARS = [("2016/17", 332_077, 72_062), ("2017/18", 340_288, 76_365),
                   ("2018/19", 333_921, 79_861)]
TFL_HOLD_MONTHS = 3
TFL_CASH_HOLD_MONTHS = 12

# ------------------------------------------------ 6. Civic honesty ---------
COHN_N = 17_303
COHN_CITIES, COHN_COUNTRIES = 355, 40
COHN_GLOBAL = [("No money", 40), ("Money (US$13.45)", 51)]
COHN_BIGMONEY = [("No money", 46), ("Money (US$13.45)", 61), ("Big money (US$94.15)", 72)]
COHN_KEY_EFFECT = 9.2       # percentage points, adding a key (no extra cash value)
COHN_COUNTRY_RANGE = (14, 76)

# ------------------------------------------------------- 7. Campus --------
NCES_TOTAL_2021 = 23_400
NCES_MIX = [("Forcible sex offenses", 10_400, 44), ("Burglary", 6_500, 28),
            ("Motor vehicle theft", 3_500, 15), ("Aggravated assault", 2_100, 9),
            ("Robbery", 500, 2), ("Arson", 400, 2)]
NCES_RATE_TREND = [("2011", 20.0), ("2019", 18.8), ("2020", 15.0), ("2021", 16.9)]

GT_2023 = {"larceny": 222, "motor_vehicle_theft": 102, "burglary": 28, "arson": 3}
GT_2022 = {"larceny": 245, "motor_vehicle_theft": 69, "burglary": 18, "arson": 3}
GT_PROPERTY_2023 = sum(GT_2023.values())            # 355
GT_PROPERTY_2022 = sum(GT_2022.values())            # 335
GT_VIOLENT_2023 = 8
GT_PARTI_2023 = GT_PROPERTY_2023 + GT_VIOLENT_2023  # 363
GT_LARCENY_SHARE_PROPERTY = 100 * GT_2023["larceny"] / GT_PROPERTY_2023
GT_LARCENY_SHARE_PARTI = 100 * GT_2023["larceny"] / GT_PARTI_2023
GT_LARCENY_SHARE_2022 = 100 * GT_2022["larceny"] / GT_PROPERTY_2022

UW_TEXTBOOK = [("Unattended backpacks / books", 69), ("Locker theft", 21),
               ("Bookstore theft", 6), ("Theft from vehicle", 4)]
UW_LOCATIONS = [("Other locations", 41), ("Grainger Hall", 23),
                ("Student Memorial Union", 17), ("Chemistry Building", 11),
                ("Libraries", 4), ("Bookstores", 4)]
UW_ORDINANCE = {"incidents": -86, "books": -91}

IU_BIKE = {
    "respondents": 590, "owners": 387, "incidents": 97,
    "student_involved": 70, "locked_outdoors": 90, "u_lock": 20,
    "reported": 58, "not_reported": 36, "recovered": 10, "registered": 36,
}
IU_SEASON = [("August", 22), ("September", 20), ("October", 16)]

USC_TREND = [("2020", 23, 13), ("2021", 20, 48), ("2022", 22, 268)]  # yr, burglary, MVT

# --------------------------------------------------- 8. Interventions -----
# (label, point % change in crime, lo, hi, n studies, evidence grade, note)
EFFECTS = [
    ("CCTV + multiple other measures", -33.9, -18.0, -46.7, 14, "strong",
     "OR 1.513, 95% CI 1.220-1.877, p<.001"),
    ("CCTV in car parks", -37.0, -5.1, -58.2, 8, "strong",
     "OR 1.588, 95% CI 1.054-2.394, p=.027"),
    ("Street lighting (night + day studies)", -18.0, -8.3, -27.0, 12, "strong",
     "RES 1.22, 90% CI 1.09-1.37, p=.002"),
    ("CCTV, actively monitored", -14.7, -7.4, -21.4, 54, "strong",
     "OR 1.172, 95% CI 1.080-1.272, p<.001"),
    ("Street lighting (pooled)", -13.8, -5.7, -21.3, 17, "strong",
     "RES 1.16, 90% CI 1.06-1.27, p=.003"),
    ("CCTV on property crime", -13.9, -2.2, -24.1, 22, "strong",
     "OR 1.161, 95% CI 1.023-1.317, p=.021"),
    ("CCTV, pooled all settings", -12.4, -6.7, -17.7, 76, "strong",
     "OR 1.141, 95% CI 1.072-1.215, p<.001"),
    ("Street lighting on property crime", -12.3, -2.9, -21.3, 15, "strong",
     "RES 1.14, 90% CI 1.03-1.27, p=.018"),
    ("CCTV in residential areas", -11.7, -3.0, -19.7, 16, "strong",
     "OR 1.133, 95% CI 1.031-1.245, p=.009"),
    ("CCTV in city / town centres", -6.2, 1.4, -13.3, 33, "none",
     "OR 1.066, 95% CI .986-1.153, p=.107 (not significant)"),
    ("CCTV, passively monitored", -1.5, 4.6, -7.5, 11, "none",
     "OR 1.015, 95% CI .954-1.081, p=.633 (not significant)"),
    ("Street lighting (night-only studies)", -2.9, 5.3, -9.9, 5, "none",
     "RES 1.03, 90% CI .95-1.11 (not significant)"),
    ("CCTV on violent crime", -4.8, 4.8, -13.4, 29, "none",
     "OR 1.050, 95% CI .954-1.155, p=.320 (not significant)"),
]

# Activation Lock natural experiment: uncontrolled administrative trends.
SOS = [
    ("New York City", "Apple-involved robberies", -19),
    ("New York City", "Apple grand larcenies from the person", -29),
    ("San Francisco", "iPhone robberies", -38),
    ("London", "Apple device thefts", -24),
]
SOS_SAMSUNG = [("New York City", 40), ("San Francisco", 12), ("London", 3)]
SOS_DATE = "18 September 2013"

GUERETTE = {"studies": 102, "examinations": 572,
            "displacement": 146, "diffusion": 152,
            "spatial_n": 272, "spatial_disp": 62, "spatial_diff": 100}
PIZA_DISPLACEMENT = {"tested": 50, "displacement": 6, "diffusion": 15, "both": 3}

# ------------------------------------------------------- 9. Frontier ------
FINDMY = {"adv_interval_s": 2, "key_rotation_min": 15, "upload_median_min": 26,
          "walk_raw_m": 81.4, "walk_smoothed_m": 25.9, "walk_reports": 489,
          "train_raw_m": 440.7, "car_raw_m": 580.7, "car_reports": 25}
PETS = {"sequences": 7, "correct_alarms": 6, "localisation_lo": 0.13, "localisation_hi": 0.40}
IETF_THRESHOLDS = {"one_dim_cm": 30, "two_dim": "18 x 13 cm", "volume_cm3": 250}
IMMOBILISE = {"users_m": 25, "items_m": 35, "since": 2003}
SITA_2024 = {"rate_per_1000": 6.3, "total_m": 33.4, "resolved_48h_pct": 66,
             "delayed": 74, "lost_stolen": 8, "damaged_pilfered": 18,
             "cause_transfer": 41, "cause_tagging": 17, "cause_loading": 16}
