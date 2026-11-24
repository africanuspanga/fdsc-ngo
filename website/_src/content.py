"""FDSC - every fact used by the website AND the company profile lives here.

Sources: the client's two profiles (FDSC_Company_Profile.pdf, Oct 2026; Frontline Profile April 2026.pdf).
Both lists of assignments were merged; where they disagreed, the newer Word profile wins.
Edit here, then run  python3 website/_src/build.py  and  python3 company-profile/build_profile.py
"""

FIRM = {
    "name": "Frontline Development Services Consulting Limited",
    "short": "FDSC",
    "name_mid": "Frontline Development Services Consulting",
    "tagline": "Pragmatic, innovative and sustainable development consulting",
    "founded": 2014,
    "registration": "Registered in 2014 under the Companies Act, 2002",
    "domain": "fdsc.co.tz",
    "url": "https://www.fdsc.co.tz",
    "email": "info@fdsc.co.tz",
    "email_alt": "fdscltd@gmail.com",
    "phone": "+255 786 266 441",
    "phone_href": "+255786266441",
    "whatsapp": "255786266441",
    "po_box": "P.O. Box 105471, Dar es Salaam, Tanzania",
    "office": "Victoria Noble Centre, Plot No. 89, Block 45B, Kinondoni, Dar es Salaam",
    "office_short": "Victoria Noble Centre, Kinondoni",
    "maps": "https://www.google.com/maps/search/?api=1&query=Victoria+Noble+Centre+Kinondoni+Dar+es+Salaam",
    "hours": "Monday to Friday, 08:30 - 17:00 EAT",
}

HEADLINE = "Turning strategy into measurable results."
INTRO = ("FDSC is a Tanzanian development and management consultancy. Since 2014 we have helped "
         "government, development partners, foundations, NGOs and businesses find out what works, "
         "strengthen the people and systems behind it, and prove the results.")

ABOUT = [
    "Frontline Development Services Consulting Limited (FDSC) is a Tanzanian firm providing development "
    "and management consulting services. We were established and registered in 2014 under the Companies "
    "Act, 2002, with one ambition: to be the consulting firm that public and private organisations trust "
    "for pragmatic, innovative and sustainable solutions.",
    "We work where research, evaluation, policy, capacity building and organisational strengthening meet. "
    "That mix lets us do more than report on a programme: we help our clients turn strategy into results "
    "they can measure, and keep improving after we leave.",
    "Our consultants are qualified and experienced in monitoring and evaluation, gender, governance, "
    "agribusiness and organisational development. Many of our clients come back to us again and again, "
    "for support that runs well beyond the contract period.",
]

VISION = ("To be the premier consulting firm in Tanzania and the wider East African region, trusted for "
          "pragmatic, innovative and sustainable solutions that transform institutions and communities.")
MISSION = ("To empower ministries, departments and agencies, companies, foundations, international and local "
           "NGOs and SMEs through high-quality, results-oriented and client-centred consulting that builds "
           "capacity and delivers measurable, lasting impact.")

VALUES = [
    ("Quality", "We hold every assignment to the highest professional and technical standards."),
    ("Results", "We focus on outcomes that matter, and on showing them with evidence."),
    ("Client focus", "We listen first, then shape each solution around the client's real needs."),
    ("Innovation", "We bring fresh, practical thinking to long-standing development problems."),
    ("Timeliness", "We deliver on schedule, because our clients' time and plans depend on it."),
]

WHY = [
    ("A decade of proven work", "More than ten years and 28 assignments across Tanzania and Zanzibar since 2014."),
    ("Trusted by leading institutions", "International development partners, government, foundations and the private sector."),
    ("Multidisciplinary team", "Consultants in M&E, gender, governance, agribusiness and organisational development."),
    ("Deep sector knowledge", "Coffee, tea and horticulture value chains, governance, gender, human rights and youth."),
    ("Tailor-made solutions", "Context-specific, practical designs instead of one-size-fits-all approaches."),
    ("Nationwide reach", "Fieldwork from Kigoma to Kilimanjaro, the Southern Highlands, Unguja and Pemba."),
    ("Clients who return", "Solidaridad, the Ministry of Finance and Planning, Rikolto and HELVETAS have hired us repeatedly."),
]

AUDIENCES = ["Ministries, departments and agencies", "Development partners", "Foundations and philanthropy",
             "International and local NGOs", "Companies and CSR programmes", "Cooperatives and SMEs"]

# icon = key into ICONS (inline SVG line icons, defined in build.py / build_profile.py)
SERVICES = [
    {"slug": "programme-management", "nav": "Programme management", "icon": "compass", "title": "Programme and project management",
     "short": "End-to-end design, planning and delivery support for development programmes and projects.",
     "points": ["Programme design and theory of change", "Work planning, budgeting and risk management",
                "Technical assistance to implementing units", "Donor reporting and compliance"]},
    {"slug": "research-mel", "nav": "Research, M&amp;E and learning", "icon": "chart", "title": "Research, monitoring, evaluation and learning",
     "short": "Baseline studies, mid-term and final evaluations, and learning systems that drive evidence-based decisions.",
     "points": ["Baseline, mid-term and end-of-project evaluations", "Rapid appraisals and sector studies",
                "M&E frameworks, indicators and tools", "Learning reviews and evidence briefs"]},
    {"slug": "gender", "nav": "Gender analysis", "icon": "people", "title": "Gender analysis and mainstreaming",
     "short": "Gender-responsive approaches built into policies, programmes and organisational practice.",
     "points": ["Gender analyses and audits", "Women's leadership and economic empowerment",
                "Gender-responsive M&E", "Youth and girls' empowerment programmes"]},
    {"slug": "organisational-development", "nav": "Organisational development", "icon": "building", "title": "Organisational development and sustainability",
     "short": "Stronger institutional systems, governance and long-term sustainability.",
     "points": ["Strategic and corporate plans", "Governance and leadership reviews",
                "Resource mobilisation plans", "Institutional capacity assessments"]},
    {"slug": "training", "nav": "Training and coaching", "icon": "spark", "title": "Training, mentoring and coaching",
     "short": "Practical capacity building for staff, boards, cooperatives and community groups.",
     "points": ["Results-based M&E training for MDAs", "Cooperative (AMCOS) governance and leadership",
                "Farmer and outgrower training", "Mentoring and on-the-job coaching"]},
    {"slug": "data", "nav": "Data and analytics", "icon": "data", "title": "Data management and analytics",
     "short": "Robust data systems and analysis that turn information into actionable insight.",
     "points": ["Survey design and digital data collection", "Quantitative and qualitative analysis",
                "Databases and dashboards", "Data quality assessments"]},
    {"slug": "performance", "nav": "Performance management", "icon": "target", "title": "Performance management and development",
     "short": "Frameworks and tools that align staff and organisational performance with strategic goals.",
     "points": ["Performance frameworks and KPIs", "Results-based management",
                "Staff appraisal systems", "Strategic plan monitoring"]},
    {"slug": "business", "nav": "Business and entrepreneurship", "icon": "briefcase", "title": "Business management and entrepreneurship",
     "short": "Advisory and training support that helps MSMEs and entrepreneurs grow sustainably.",
     "points": ["Business development training", "Entrepreneurship for CSR programme beneficiaries",
                "Business planning and record keeping", "Access to finance and investment"]},
    {"slug": "agribusiness", "nav": "Agribusiness value chains", "icon": "leaf", "title": "Agribusiness value chain management",
     "short": "Stronger value chains, from smallholder production to market access.",
     "points": ["Coffee, tea, horticulture, rice and sugar value chains", "Certification and market access",
                "Soil fertility and climate-resilient farming", "Farmer organisation and outgrower schemes"]},
]

SECTORS = [
    {"title": "Agriculture and agribusiness", "img": "coffee-harvest",
     "text": "Coffee, tea, horticulture, rice and sugar value chains: from smallholder farms and cooperatives to certification and export markets."},
    {"title": "Governance and public sector", "img": "office-meeting",
     "text": "Results-based M&E for ministries and agencies, EU-Tanzania cooperation, corporate plans and institutional strengthening."},
    {"title": "Gender, youth and rights", "img": "schoolgirls",
     "text": "Women's leadership, girls' empowerment, youth programmes and support to human rights defenders."},
    {"title": "Climate and natural resources", "img": "kilimanjaro",
     "text": "Water-resilient food systems, sustainable soil fertility and environmental conservation with farming communities."},
]

APPROACH = [
    ("Listen", "We start with the client's questions, context and constraints, and agree what success looks like."),
    ("Design", "We tailor the method: sampling, tools, analysis plan and team, built for the assignment, not copied."),
    ("Deliver", "Experienced consultants in the field and on the data, with regular check-ins and no surprises."),
    ("Learn", "Clear findings, practical recommendations and validation with stakeholders, so results get used."),
]

TYPES = {
    "eval": "Evaluation",
    "base": "Baseline and appraisal",
    "mel": "M&E systems",
    "cap": "Capacity building",
    "ta": "Advisory and technical assistance",
}

TYPES_SHORT = {"eval": "Evaluation", "base": "Baseline / appraisal", "mel": "M&amp;E systems",
               "cap": "Capacity building", "ta": "Advisory &amp; TA"}

ZONES = [
    {"name": "Southern Highlands", "regions": "Mbeya, Songwe, Njombe, Iringa, Ruvuma, Katavi",
     "text": "Coffee export readiness, horticulture businesses, certification and market access, water-resilient food systems."},
    {"name": "Northern zone", "regions": "Arusha, Kilimanjaro, Manyara",
     "text": "Coffee cooperative governance, the Include programme with Trias, climate-resilient communities."},
    {"name": "Lake and Western zone", "regions": "Mwanza, Kagera, Kigoma, Geita, Shinyanga, Simiyu",
     "text": "Girls' empowerment, sugarcane outgrowers, sustainable soil fertility, women's economic empowerment."},
    {"name": "Coast and Zanzibar", "regions": "Dar es Salaam, Pwani, Tanga, Lindi, Mtwara, Unguja, Pemba",
     "text": "Zanzibar sector appraisal, coffee, tea and horticulture market access, CSR entrepreneurship training."},
]

# Newest first. regions = map regions (Songwe is drawn inside Mbeya; "Unguja"/"Pemba" = Zanzibar).
ASSIGNMENTS = [
    {"period": "Aug - Sep 2025", "year": 2025, "client": "Rikolto", "type": "eval", "sector": "Climate",
     "title": "Mid-term evaluation of the Water for Resilient Communities and Food Systems (FICAP) project",
     "where": "Arusha, Kilimanjaro, Mbeya and Songwe", "regions": ["Arusha", "Kilimanjaro", "Mbeya"]},
    {"period": "Feb - Mar 2025", "year": 2025, "client": "HELVETAS Swiss Intercooperation", "type": "base", "sector": "Agriculture",
     "title": "Rapid appraisal of the agriculture, fisheries, forestry and eco-tourism sectors in Zanzibar",
     "where": "Zanzibar", "regions": ["Unguja", "Pemba"]},
    {"period": "Jan - Mar 2025", "year": 2025, "client": "Solidaridad East and Central Africa", "type": "eval", "sector": "Agriculture",
     "title": "End-of-project evaluation of the Passport to Coffee Export (PACE) project",
     "where": "Ruvuma, Mbeya and Songwe", "regions": ["Ruvuma", "Mbeya"], "donor": "EU"},
    {"period": "Nov - Dec 2024", "year": 2024, "client": "Rikolto", "type": "eval", "sector": "Agriculture",
     "title": "Final evaluation of the Building Inclusive and Competitive Horticulture Businesses in the Southern Highlands (BICHOBS) project",
     "where": "Iringa, Mbeya, Njombe, Songwe and Katavi", "regions": ["Iringa", "Mbeya", "Njombe", "Katavi"], "donor": "EU"},
    {"period": "Jun - Oct 2024", "year": 2024, "client": "Trias", "type": "eval", "sector": "Agriculture",
     "title": "Mid-term evaluation of the DGD Include Programme 2022-2026",
     "where": "Arusha and Manyara", "regions": ["Arusha", "Manyara"]},
    {"period": "Jun - Jul 2024", "year": 2024, "client": "Solidaridad East and Central Africa", "type": "eval", "sector": "Agriculture",
     "title": "Final evaluation of Certification and Beyond: Market Access for Sustainable Coffee, Horticulture and Tea",
     "where": "Ruvuma, Njombe, Mbeya, Songwe, Unguja and Pemba", "regions": ["Ruvuma", "Njombe", "Mbeya", "Unguja", "Pemba"]},
    {"period": "Dec 2019 - Dec 2024", "year": 2024, "client": "Ministry of Finance and Planning (EDF Programme Support Unit)", "type": "ta", "sector": "Governance",
     "title": "Consortium partner, with FCG Sweden (now Cowater), providing technical assistance to the AGRI-CONNECT programme on sector enablers and the business environment for tea, coffee and horticulture",
     "where": "National", "regions": [], "donor": "EU"},
    {"period": "Mar - Apr 2023", "year": 2023, "client": "Solidaridad East and Central Africa", "type": "eval", "sector": "Agriculture",
     "title": "Mid-term evaluation of the Passport to Coffee Export (PACE) project",
     "where": "Mbeya, Ruvuma and Songwe", "regions": ["Mbeya", "Ruvuma"], "donor": "EU"},
    {"period": "Mar 2022", "year": 2022, "client": "Agricultural Markets Development Trust (AMDT)", "type": "ta", "sector": "Agriculture",
     "title": "Evaluation of proposals to strengthen two local radio stations, and of quotations for radio station equipment",
     "where": "National", "regions": []},
    {"period": "Nov 2021 - Mar 2022", "year": 2022, "client": "The Nature Conservancy (TNC)", "type": "cap", "sector": "Climate",
     "title": "Capacity building of smallholder farmers on sustainable soil fertility",
     "where": "Buhingu Ward, Uvinza District, Kigoma", "regions": ["Kigoma"]},
    {"period": "Sep - Nov 2021", "year": 2021, "client": "Ministry of Finance and Planning", "type": "ta", "sector": "Governance",
     "title": "Comprehensive report on EU-Tanzania cooperation under the 10th and 11th European Development Fund (EDF)",
     "where": "National", "regions": [], "donor": "EU"},
    {"period": "Oct 2020 - Jan 2021", "year": 2021, "client": "Solidaridad East and Central Africa", "type": "base", "sector": "Agriculture",
     "title": "Baseline study for Certification and Beyond: Market Access for Sustainable Coffee, Horticulture and Tea",
     "where": "Ruvuma, Njombe, Mbeya, Songwe, Unguja and Pemba", "regions": ["Ruvuma", "Njombe", "Mbeya", "Unguja", "Pemba"]},
    {"period": "Sep - Nov 2020", "year": 2020, "client": "Rikolto", "type": "base", "sector": "Agriculture",
     "title": "Baseline study of the Building Inclusive and Competitive Horticulture Businesses in the Southern Highlands (BICHOBS) project",
     "where": "Iringa, Mbeya, Njombe, Songwe and Katavi", "regions": ["Iringa", "Mbeya", "Njombe", "Katavi"], "donor": "EU"},
    {"period": "Feb - Aug 2020", "year": 2020, "client": "Solidaridad East and Central Africa", "type": "cap", "sector": "Agriculture",
     "title": "Training and mentoring of coffee cooperatives (AMCOS) on governance, leadership and access to investment",
     "where": "Kilimanjaro", "regions": ["Kilimanjaro"]},
    {"period": "Jan - Mar 2020", "year": 2020, "client": "Hanns Seidel Foundation", "type": "eval", "sector": "Gender",
     "title": "Final evaluation of the “Women Leaders – Power of Change” project",
     "where": "National", "regions": [], "donor": "EU"},
    {"period": "Nov 2019 - Jan 2020", "year": 2020, "client": "FEMINA Hip / Irish Aid", "type": "base", "sector": "Gender",
     "title": "Baseline survey of the Girls Power project (Nguvu ya Binti), phase II",
     "where": "Misungwi and Sengerema, Mwanza", "regions": ["Mwanza"]},
    {"period": "Jul - Aug 2019", "year": 2019, "client": "Ministry of Finance and Planning (EDF Programme Support Unit)", "type": "mel", "sector": "Governance",
     "title": "Monitoring and evaluation technical support to the Programme Support Unit for the European Development Fund",
     "where": "National", "regions": [], "donor": "EU"},
    {"period": "Dec 2018 - Jan 2019", "year": 2019, "client": "Tanzania Coffee Research Institute (TaCRI)", "type": "mel", "sector": "Agriculture",
     "title": "Monitoring and evaluation framework and tools for the institute's Strategic Action Plan",
     "where": "National", "regions": []},
    {"period": "Sep - Oct 2018", "year": 2018, "client": "Tanzania Human Rights Defenders Coalition (THRDC)", "type": "ta", "sector": "Gender",
     "title": "Resource mobilisation plan for the coalition",
     "where": "National", "regions": []},
    {"period": "Aug - Sep 2018", "year": 2018, "client": "Sugar Board of Tanzania (SBT)", "type": "eval", "sector": "Agriculture",
     "title": "Project review and final report for the Accompanying Measures for Sugar Protocol (AMSP) project",
     "where": "National", "regions": [], "donor": "EU"},
    {"period": "Aug - Sep 2018", "year": 2018, "client": "Restless Development", "type": "eval", "sector": "Gender",
     "title": "End-of-project evaluation of the Mwanamke Tunu programme",
     "where": "Dar es Salaam, Dodoma, Pwani, Lindi, Mtwara, Shinyanga, Geita, Simiyu and Tanga",
     "regions": ["Dar es Salaam", "Dodoma", "Pwani", "Lindi", "Mtwara", "Shinyanga", "Geita", "Simiyu", "Tanga"]},
    {"period": "Apr 2018", "year": 2018, "client": "Ministry of Finance and Planning (EDF Programme Support Unit)", "type": "cap", "sector": "Governance",
     "title": "Training of ministries, departments and agencies on results-based M&E and upgraded monitoring tools for EU-funded projects",
     "where": "National", "regions": [], "donor": "EU"},
    {"period": "Oct - Dec 2017", "year": 2017, "client": "HELVETAS Swiss Intercooperation", "type": "base", "sector": "Agriculture",
     "title": "Baseline survey of the Rice Post-harvest Management and Marketing (RIPOMA) project",
     "where": "Morogoro", "regions": ["Morogoro"]},
    {"period": "Jan - Feb 2017", "year": 2017, "client": "Songas", "type": "cap", "sector": "Private sector",
     "title": "Business development and entrepreneurship training for CSR programme beneficiaries",
     "where": "Kibiti, Mkuranga and Rufiji, Pwani", "regions": ["Pwani"]},
    {"period": "Feb - Mar 2016", "year": 2016, "client": "Sugar Board of Tanzania (SBT)", "type": "cap", "sector": "Agriculture",
     "title": "Training of sugarcane outgrowers on business management, gender, environmental conservation, lobbying and advocacy",
     "where": "Kagera, Kilombero and Mtibwa", "regions": ["Kagera", "Morogoro"]},
    {"period": "May - Jul 2015", "year": 2015, "client": "HELVETAS Swiss Intercooperation", "type": "base", "sector": "Agriculture",
     "title": "Baseline survey of the vegetable producers' project (UWAKI)",
     "where": "Singida", "regions": ["Singida"], "donor": "EU"},
    {"period": "Oct 2014 - Apr 2015", "year": 2015, "client": "Tanzania Bureau of Standards (TBS)", "type": "mel", "sector": "Governance",
     "title": "Institutionalising monitoring and evaluation for the TBS Corporate Plan 2011/12-2015/16",
     "where": "National", "regions": []},
    {"period": "Sep - Nov 2014", "year": 2014, "client": "Tea Research Institute of Tanzania (TRIT)", "type": "mel", "sector": "Agriculture",
     "title": "M&E framework for the Tanzania Agriculture Support Programme (TASP II)",
     "where": "National", "regions": [], "donor": "EU"},
]

# Selected work shown as illustrated cards (index into ASSIGNMENTS by matching title start)
FEATURED = [
    {"key": "Mid-term evaluation of the Water", "img": "kilimanjaro", "label": "Climate resilience",
     "headline": "Water and food systems that hold up in a changing climate",
     "summary": "Mid-term evaluation of Rikolto's FICAP project across the Northern and Southern Highlands."},
    {"key": "End-of-project evaluation of the Passport", "img": "coffee", "label": "Coffee value chain",
     "headline": "Getting Tanzanian coffee ready for export",
     "summary": "Mid-term (2023) and end-of-project (2025) evaluations of Solidaridad's EU-funded PACE project."},
    {"key": "Consortium partner", "img": "tea-farmer", "label": "Technical assistance",
     "headline": "Five years inside the EU's AGRI-CONNECT programme",
     "summary": "With FCG Sweden (now Cowater): tea, coffee and horticulture sector enablers, 2019-2024."},
    {"key": "Final evaluation of the Building", "img": "vegetables", "label": "Horticulture",
     "headline": "Horticulture businesses in the Southern Highlands",
     "summary": "Baseline (2020) and final evaluation (2024) of Rikolto's EU-funded BICHOBS project."},
    {"key": "Baseline survey of the Girls Power", "img": "schoolgirls", "label": "Gender and youth",
     "headline": "Measuring change for girls in Mwanza",
     "summary": "Baseline survey for FEMINA Hip's Irish Aid-funded Nguvu ya Binti project, phase II."},
    {"key": "Capacity building of smallholder", "img": "seedling", "label": "Soil and livelihoods",
     "headline": "Healthier soils for Kigoma's smallholders",
     "summary": "Training farmers in Uvinza District on sustainable soil fertility with The Nature Conservancy."},
]

# Partner / client logos (files in website/assets/partners/, made by _tools/prepare_assets.py)
CLIENTS = [
    ("solidaridad", "Solidaridad East and Central Africa"), ("rikolto", "Rikolto"),
    ("helvetas", "HELVETAS Swiss Intercooperation"), ("govt-tanzania", "Ministry of Finance and Planning"),
    ("tnc", "The Nature Conservancy"), ("trias", "Trias"), ("hanns-seidel", "Hanns Seidel Foundation"),
    ("femina", "FEMINA Hip"), ("restless", "Restless Development"), ("amdt", "Agricultural Markets Development Trust"),
    ("tacri", "Tanzania Coffee Research Institute"), ("trit", "Tea Research Institute of Tanzania"),
    ("tbs", "Tanzania Bureau of Standards"), ("sbt", "Sugar Board of Tanzania"),
    ("thrdc", "Tanzania Human Rights Defenders Coalition"), ("songas", "Songas"),
    ("irdp", "Institute of Rural Development Planning"),
]

# Map: region names as in _src/tz_map.json (2015 boundaries)
ZANZIBAR = {"Unguja": ["Zanzibar North", "Zanzibar South & Central", "Zanzibar Urban/West"],
            "Pemba": ["North Pemba", "South Pemba"]}


def worked_regions():
    """Region names (map polygons) where FDSC has delivered at least one assignment."""
    names = set()
    for a in ASSIGNMENTS:
        for r in a["regions"]:
            names.update(ZANZIBAR.get(r, [r]))
    return names


def mainland_count():
    """Mainland regions worked in, counting Songwe (inside the Mbeya polygon) separately."""
    mainland = {r for a in ASSIGNMENTS for r in a["regions"] if r not in ZANZIBAR}
    songwe = any("Songwe" in a["where"] for a in ASSIGNMENTS)
    return len(mainland) + (1 if songwe else 0)


def clients_count():
    base = {a["client"].split(" (")[0].replace("Ministry of Finance and Planning", "MoFP") for a in ASSIGNMENTS}
    return len(base)


def repeat_clients():
    from collections import Counter
    def norm(c):
        c = c.split(" (")[0]
        return "Ministry of Finance and Planning" if c.startswith("Ministry of Finance") else c
    return [(c, n) for c, n in Counter(norm(a["client"]) for a in ASSIGNMENTS).most_common() if n > 1]


def by_type():
    from collections import Counter
    c = Counter(a["type"] for a in ASSIGNMENTS)
    return [(TYPES[k], c[k]) for k in TYPES]


def featured():
    out = []
    for f in FEATURED:
        a = next(x for x in ASSIGNMENTS if x["title"].startswith(f["key"]))
        out.append({**f, "a": a})
    return out


STATS = {
    "years": 2026 - FIRM["founded"],
    "assignments": len(ASSIGNMENTS),
    "clients": None,       # filled below
    "mainland": None,
}
STATS["clients"] = clients_count()
STATS["mainland"] = mainland_count()

if __name__ == "__main__":
    print("assignments", len(ASSIGNMENTS), "clients", STATS["clients"], "mainland regions", STATS["mainland"])
    print("by type", by_type())
    print("repeat", repeat_clients())
    print("map regions on", len(worked_regions()))
