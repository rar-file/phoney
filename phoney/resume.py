from __future__ import annotations

import random
from datetime import date
from typing import Dict, List, Optional, Tuple, Union

from .person import generate_person
from .phone import generate_phone
from .emailgen import generate_email
from .username import generate_online_presence
from .career import (
    generate_job_title,
    generate_salary,
    generate_employment_history,
    generate_skills,
    experience_level_from_years,
)
from .data_loader import load_cities, load_states, load_countries, load_streets


__all__ = ["generate_resume"]


def _country_from_locale(locale: Optional[str]) -> Tuple[str, str]:
    if not locale:
        return ("US", "United States")
    loc = locale.replace("-", "_")
    cc = loc.split("_")[-1].upper() if "_" in loc else (loc.upper() if len(loc) == 2 else "US")
    countries = load_countries()
    return (cc, countries.get(cc, cc))


def _location_for(locale: Optional[str]) -> Dict[str, str]:
    loc = locale or "en_US"
    cities = load_cities()
    states = load_states()
    city_list = cities.get(loc) or cities.get("default", ["Metropolis"]) 
    state_list = states.get(loc) or states.get("default", ["State"]) 
    city = random.choice(city_list) if city_list else "Metropolis"
    state = random.choice(state_list) if state_list else "State"
    cc, country_name = _country_from_locale(loc)
    return {"city": city, "state": state, "country_code": cc, "country": country_name, "locale": loc}


def _postal_code_for(locale: str) -> str:
    cc, _ = _country_from_locale(locale)
    if cc == "US":
        base = f"{random.randint(10000, 99999)}"
        return base if random.random() < 0.7 else f"{base}-{random.randint(1000,9999):04d}"
    if cc == "GB":
        # Roughly shaped like UK postcodes; not guaranteed valid but looks realistic
        outcode = f"{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(1,9)}{random.choice(['',''+random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')])}"
        incode = f"{random.randint(1,9)}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}"
        return f"{outcode} {incode}"
    if cc == "DE" or cc == "FR":
        return f"{random.randint(10000, 99999)}"
    if cc == "JP":
        return f"{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    if cc == "CN":
        return f"{random.randint(100000, 999999)}"
    if cc == "BR":
        return f"{random.randint(10000, 99999)}-{random.randint(100, 999)}"
    return f"{random.randint(10000, 99999)}"


def _address_for(locale: str, location: Dict[str, str]) -> Dict[str, str]:
    streets = load_streets()
    choices = streets.get(locale) or streets.get("default", ["Main Street"]) 
    street_name = random.choice(choices)
    house_no = random.randint(10, 9999)
    unit = f"Apt {random.randint(1, 999)}" if random.random() < 0.25 else ""
    postal = _postal_code_for(locale)
    return {
        "line1": f"{house_no} {street_name}",
        "line2": unit,
        "city": location["city"],
        "state": location["state"],
        "postal_code": postal,
        "country": location["country"],
    }


def _pick_degree_track(family: Optional[str]) -> Tuple[str, List[str]]:
    fam = family or "software_engineer"
    fam_l = fam.lower()
    if "data" in fam_l:
        return (
            "Data Science",
            [
                "BSc in Computer Science",
                "BSc in Statistics",
                "MSc in Data Science",
                "MSc in Machine Learning",
            ],
        )
    if "product" in fam_l:
        return (
            "Product/Business",
            [
                "BBA in Business Administration",
                "BSc in Information Systems",
                "MSc in Product Management",
                "MBA",
            ],
        )
    if any(key in fam_l for key in ["devops", "security", "network", "qa", "software", "engineer"]):
        return (
            "Computer Science",
            [
                "BSc in Computer Science",
                "BEng in Software Engineering",
                "BSc in Information Technology",
                "MSc in Computer Science",
            ],
        )
    if "designer" in fam_l:
        return (
            "Design",
            [
                "BA in Graphic Design",
                "BDes in Interaction Design",
                "MDes in User Experience",
            ],
        )
    if any(key in fam_l for key in ["finance", "operations", "sales", "marketing", "hr"]):
        return (
            "Business",
            [
                "BBA in Business Administration",
                "BSc in Economics",
                "MSc in Management",
                "MBA",
            ],
        )
    return (
        "General",
        ["BSc in Computer Science", "BSc in Information Systems", "BA in Communications"],
    )


INSTITUTIONS = [
    "Northbridge University",
    "Western Valley Institute of Technology",
    "Royal City University",
    "Metropolitan College of Engineering",
    "St. Andrew's College",
    "Lakeview Polytechnic",
    "Greenwich Institute",
    "Nova State University",
]


CERTS_BY_TRACK = {
    "Computer Science": [
        "AWS Certified Solutions Architect",
        "Microsoft Certified: Azure Administrator",
        "Google Professional Cloud Architect",
        "CKA: Certified Kubernetes Administrator",
    ],
    "Data Science": [
        "TensorFlow Developer Certificate",
        "Databricks Lakehouse Fundamentals",
        "AWS Machine Learning Specialty",
    ],
    "Product/Business": [
        "CSPO: Certified Scrum Product Owner",
        "PMP: Project Management Professional",
    ],
    "Design": [
        "NN/g UX Certification",
        "Figma Professional",
    ],
    "Business": [
        "Lean Six Sigma Green Belt",
        "Scrum Master (PSM I)",
    ],
    "General": [
        "Scrum Master (PSM I)",
        "ITIL Foundation",
    ],
}


LANG_BY_LOCALE = {
    "en_US": ["English"],
    "en_GB": ["English"],
    "de_DE": ["German", "English"],
    "fr_FR": ["French", "English"],
    "es_ES": ["Spanish", "English"],
    "it_IT": ["Italian", "English"],
    "ja_JP": ["Japanese", "English"],
    "zh_CN": ["Chinese", "English"],
}


INTERESTS = [
    "open-source", "trail running", "photography", "baking", "reading",
    "board games", "travel", "volunteering", "mentoring", "robotics",
]

SOFT_SKILLS = [
    "Communication", "Collaboration", "Leadership", "Mentorship", "Problem Solving",
    "Ownership", "Product Thinking", "Prioritization", "Time Management", "Adaptability",
]

TOOLS_BY_FAMILY = {
    "software_engineer": ["Git", "Docker", "Kubernetes", "Linux", "PostgreSQL", "Redis", "Jira", "Confluence"],
    "devops_engineer": ["Terraform", "Ansible", "Prometheus", "Grafana", "Git", "Docker", "Kubernetes", "Jira"],
    "data_scientist": ["Jupyter", "Pandas", "Airflow", "Spark", "SQL", "MLflow", "Matplotlib", "Seaborn"],
    "product_manager": ["Jira", "Confluence", "Figma", "Amplitude", "Mixpanel", "Google Analytics"],
    "designer": ["Figma", "Sketch", "Adobe XD", "Illustrator", "Photoshop"],
    "qa_engineer": ["Selenium", "Cypress", "Playwright", "Jira", "Postman"],
    "security_engineer": ["Burp Suite", "Nmap", "Wireshark", "Metasploit", "SIEM"],
}


def _bullets_for_role(family: str, skills: List[str]) -> List[str]:
    verbs = [
        "Led", "Designed", "Implemented", "Optimized", "Automated", "Migrated",
        "Refactored", "Built", "Architected", "Improved", "Reduced",
    ]
    impacts = [
        "performance by {x}%", "latency by {x}%", "costs by {x}%",
        "deployment time by {x}%", "incident rate by {x}%", "defects by {x}%",
        "test coverage to {x}%", "uptime to {x}%",
    ]
    objs = [
        "microservices", "data pipelines", "CI/CD", "monitoring dashboards",
        "APIs", "ETL workflows", "feature flags", "Kubernetes clusters",
        "design systems", "experiments", "risk controls",
    ]
    bullets: List[str] = []
    for _ in range(random.randint(3, 6)):
        v = random.choice(verbs)
        imp = random.choice(impacts).format(x=random.randint(10, 80))
        obj = random.choice(objs)
        tech = random.choice(skills) if skills else "Python"
        bullets.append(f"{v} {obj} using {tech}, improving {imp}.")
    return bullets


def _project_snippets(skills: List[str]) -> List[Dict[str, str]]:
    prefixes = ["Aurora", "Nimbus", "Atlas", "Echo", "Vertex", "Quantum", "Orion", "Harbor"]
    out = []
    for _ in range(random.randint(2, 4)):
        name = f"Project {random.choice(prefixes)}"
        tech_list = random.sample(skills, k=min(len(skills), random.randint(2, 5))) if skills else ["Python"]
        tech = ", ".join(tech_list)
        outcome = random.choice([
            "reduced costs by {x}%",
            "improved performance by {x}%",
            "cut deployment time by {x}%",
            "increased retention by {x}%",
        ]).format(x=random.randint(10, 60))
        desc = f"Built a {random.choice(['scalable','secure','high-availability','real-time'])} system using {tech}; {outcome}."
        out.append({
            "name": name,
            "role": random.choice(["Lead Engineer", "Engineer", "Contributor", "Owner"]),
            "description": desc,
            "technologies": tech_list,
        })
    return out


def _summarize(years: int, title: str, skills: List[str]) -> str:
    key_sk = ", ".join(skills[:5]) if skills else "modern tooling"
    return (
        f"{years}+ years as {title}. Strong in {key_sk}. Passionate about quality, impact, and mentorship."
    )


def _to_text(cv: Dict[str, Union[str, dict, list]]) -> str:
    p = cv["personal"]
    lines: List[str] = []
    lines.append(f"{p['first_name']} {p['last_name']} — {cv['headline']}")
    lines.append(f"{p['email']} | {p['phone']} | {p['location']['city']}, {p['location']['state']} {p['location']['country']}")
    addr = cv.get("address")
    if addr:
        line2 = f", {addr['line2']}" if addr.get('line2') else ""
        lines.append(f"Address: {addr['line1']}{line2}, {addr['city']}, {addr['state']} {addr['postal_code']} {addr['country']}")
    handles = cv.get("online_presence", {})
    if handles.get("linkedin") or handles.get("github"):
        ln = []
        if handles.get("linkedin"): ln.append(f"LinkedIn: {handles['linkedin']}")
        if handles.get("github"): ln.append(f"GitHub: {handles['github']}")
        if handles.get("website"): ln.append(f"Web: {handles['website']}")
        lines.append(" | ".join(ln))
    lines.append("")
    lines.append("Summary")
    lines.append(cv["summary"])
    if cv.get("summary_highlights"):
        for h in cv["summary_highlights"]:
            lines.append(f" - {h}")
    lines.append("")
    lines.append("Skills")
    core = ", ".join(cv["skills"].get("core", []))
    secondary = ", ".join(cv["skills"].get("secondary", []))
    tools = ", ".join(cv["skills"].get("tools", []))
    soft = ", ".join(cv["skills"].get("soft", []))
    if core:
        lines.append(f"Core: {core}")
    if secondary:
        lines.append(f"Secondary: {secondary}")
    if tools:
        lines.append(f"Tools: {tools}")
    if soft:
        lines.append(f"Soft: {soft}")
    lines.append("")
    lines.append("Experience")
    for r in cv["experience"]:
        lines.append(f"{r['title']} — {r['company']} ({r['start_date']} to {r['end_date']})")
        for b in r.get("responsibilities", []):
            lines.append(f" - {b}")
    if cv.get("volunteer"):
        lines.append("")
        lines.append("Volunteer Experience")
        for v in cv["volunteer"]:
            lines.append(f"{v['role']} — {v['organization']} ({v['start_date']} to {v['end_date']})")
            if v.get("highlights"):
                for b in v["highlights"]:
                    lines.append(f" - {b}")
    if cv.get("projects"):
        lines.append("")
        lines.append("Projects")
        for pr in cv["projects"]:
            lines.append(f"{pr['name']} ({pr.get('role','')}) — {', '.join(pr.get('technologies', []))}")
            lines.append(f"  {pr['description']}")
    if cv.get("education"):
        lines.append("")
        lines.append("Education")
        for ed in cv["education"]:
            extra = []
            if ed.get("gpa"):
                extra.append(f"GPA {ed['gpa']}")
            if ed.get("coursework"):
                extra.append("Coursework: " + ", ".join(ed["coursework"]))
            extra_str = f" — {'; '.join(extra)}" if extra else ""
            lines.append(f"{ed['degree']} — {ed['institution']} ({ed['year']}){extra_str}")
    if cv.get("certifications"):
        lines.append("")
        lines.append("Certifications")
        for c in cv["certifications"]:
            issuer = f" ({c['issuer']})" if isinstance(c, dict) and c.get('issuer') else ""
            when = f", {c['year']}" if isinstance(c, dict) and c.get('year') else ""
            name = c["name"] if isinstance(c, dict) else str(c)
            lines.append(f"- {name}{issuer}{when}")
    if cv.get("languages"):
        lines.append("")
        if isinstance(cv["languages"], list) and cv["languages"] and isinstance(cv["languages"][0], dict):
            lines.append("Languages:")
            for lang in cv["languages"]:
                lines.append(f" - {lang['language']} ({lang.get('proficiency','')})")
        else:
            lines.append("Languages: " + ", ".join(cv["languages"]))
    if cv.get("interests"):
        lines.append("Interests: " + ", ".join(cv["interests"]))
    if cv.get("publications"):
        lines.append("")
        lines.append("Publications")
        for pub in cv["publications"]:
            lines.append(f"- {pub['title']} ({pub['venue']}, {pub['year']})")
    if cv.get("awards"):
        lines.append("")
        lines.append("Awards")
        for a in cv["awards"]:
            lines.append(f"- {a['name']} ({a['year']})")
    if cv.get("references"):
        lines.append("")
        lines.append("References")
        for r in cv["references"]:
            lines.append(f"- {r['name']}, {r['title']} at {r['company']} — {r['email']} | {r['phone']}")
    return "\n".join(lines)


def generate_resume(
    locale: Optional[str] = None,
    family: Optional[str] = None,
    years: int = 8,
    format: str = "dict",
) -> Union[Dict[str, Union[str, dict, list]], str]:
    """
    Build a realistic Resume/CV from core generators.

    Args:
        locale: e.g., 'en_US'. Affects names, phone, location hints.
        family: job family bias (e.g., 'software_engineer'). If None, random.
        years: employment history window in years.
        format: 'dict' (default) for structured object, or 'text' for pretty text.

    Returns:
        dict or text string depending on 'format'.
    """
    loc = locale or "en_US"

    # Person & contact
    person = generate_person(loc)
    first_name, last_name = person["first_name"], person["last_name"]
    email = generate_email(first_name, last_name, loc)
    phone = generate_phone(loc)
    location = _location_for(loc)
    address = _address_for(loc, location)
    online = generate_online_presence(first_name, last_name, loc)
    linkedin = online["social_media"].get("linkedin")
    github = online["social_media"].get("github")
    website = f"https://www.{last_name.lower()}-{first_name.lower()}.com"

    # Career details
    # Seed a primary job title to bias skills
    jt = generate_job_title(locale=loc, family=family)
    fam = jt["family"]
    lvl = jt["level"]
    title = jt["title"]
    core_skills = generate_skills(fam, level=lvl)
    # Secondary/related skills from a different random family
    other_fam = generate_job_title(locale=loc, family=None)["family"]
    secondary_skills_set = set(generate_skills(other_fam)) - set(core_skills)
    secondary_skills = list(secondary_skills_set)[:max(3, min(6, len(core_skills)))] if core_skills else []

    # Employment history enriched with responsibilities
    history = generate_employment_history(years=years, locale=loc, family=fam)
    for role in history:
        role["responsibilities"] = _bullets_for_role(fam, core_skills)

    # Education & certifications inferred by track
    track, degrees = _pick_degree_track(fam)
    grad_year = date.today().year - max(3, years - random.randint(0, 3))
    education = [
        {
            "degree": random.choice(degrees),
            "institution": random.choice(INSTITUTIONS),
            "year": grad_year,
            "gpa": round(random.uniform(3.2, 4.0), 2) if random.random() < 0.5 else None,
            "coursework": random.sample(
                [
                    "Algorithms", "Distributed Systems", "Databases", "Operating Systems",
                    "Machine Learning", "Statistics", "Networks", "Cloud Computing",
                ], k=random.randint(2, 5)
            ),
        }
    ]
    cert_names = CERTS_BY_TRACK.get(track, CERTS_BY_TRACK["General"])
    certs = [
        {
            "name": name,
            "issuer": random.choice(["AWS", "Microsoft", "Google", "CNCF", "PMI", "Scrum.org"]),
            "year": date.today().year - random.randint(0, 5),
        }
        for name in random.sample(cert_names, k=random.randint(0, min(3, len(cert_names))))
    ]

    # Projects derived from skills
    projects = _project_snippets(core_skills)

    # Languages with proficiency & interests
    base_langs = LANG_BY_LOCALE.get(loc, ["English"]) 
    profs = ["Native", "Fluent", "Professional", "Intermediate", "Basic"]
    languages = [
        {"language": base_langs[0], "proficiency": random.choice(["Native", "Fluent"])},
    ]
    for lang in base_langs[1:]:
        languages.append({"language": lang, "proficiency": random.choice(profs[2:])})
    interests = random.sample(INTERESTS, k=random.randint(2, 5))

    # Salary expectation aligned with family/level (informational)
    salary = generate_salary(locale=loc, family=fam, level=lvl, title=title)

    # Headline and summary
    headline = f"{lvl} {title}" if lvl not in title else title
    summary = _summarize(years, title, core_skills)
    summary_highlights = [
        f"Delivered {random.randint(3,10)}+ projects from design to production",
        f"Mentored {random.randint(2,8)} engineers across teams",
        f"Partnered with Product/Design to drive roadmap and outcomes",
    ]
    # Skills enrichments
    tools = TOOLS_BY_FAMILY.get(fam, TOOLS_BY_FAMILY.get("software_engineer", []))
    tools = random.sample(tools, k=min(len(tools), random.randint(3, len(tools)))) if tools else []
    soft = random.sample(SOFT_SKILLS, k=random.randint(3, 6))

    # Volunteer
    volunteer = []
    if random.random() < 0.6:
        volunteer.append({
            "organization": random.choice(["Code for Good", "Local Food Bank", "Open Source Collective", "STEM Mentors"]),
            "role": random.choice(["Volunteer Developer", "Mentor", "Organizer", "Contributor"]),
            "start_date": f"{date.today().year - random.randint(1, 4)}-01-01",
            "end_date": "Present",
            "highlights": [
                "Built internal tools to streamline operations",
                "Mentored students on projects and career guidance",
            ],
        })

    # Publications & awards
    publications = []
    if random.random() < 0.4:
        publications.append({
            "title": f"{random.choice(['Scaling','Observability','Reliability','Security'])} in Cloud-Native Systems",
            "venue": random.choice(["TechBlog", "Medium", "Conference Proceedings"]),
            "year": date.today().year - random.randint(0, 3),
            "url": website + "/posts/1",
        })
    awards = []
    if random.random() < 0.4:
        awards.append({
            "name": random.choice(["Employee of the Year", "Innovation Award", "Top Mentor"]),
            "year": date.today().year - random.randint(0, 3),
        })

    # References
    references = []
    if random.random() < 0.7:
        references.append({
            "name": f"{first_name} {random.choice(['Reed','Stone','Parker','Hill'])}",
            "title": random.choice(["Manager", "Director", "Tech Lead"]),
            "company": history[-1]["company"] if history else "",
            "email": f"{first_name.lower()}.{last_name.lower()}@ref.example.com",
            "phone": phone,
        })

    cv: Dict[str, Union[str, dict, list]] = {
        "personal": {
            "first_name": first_name,
            "last_name": last_name,
            "gender": person.get("gender"),
            "email": email,
            "phone": phone,
            "location": location,
        },
        "address": address,
        "headline": headline,
        "summary": summary,
        "summary_highlights": summary_highlights,
        "experience": history,
        "skills": {
            "core": core_skills,
            "secondary": secondary_skills,
            "tools": tools,
            "soft": soft,
        },
        "projects": projects,
        "education": education,
        "certifications": certs,
        "languages": languages,
        "interests": interests,
        "publications": publications,
        "awards": awards,
        "volunteer": volunteer,
        "references": references,
        "online_presence": {
            "username": online.get("username"),
            "github": github,
            "linkedin": linkedin,
            "website": website,
        },
        "salary_expectation": salary,
        "meta": {
            "family": fam,
            "level": lvl,
            "experience_years": years,
            "track": track,
            "current_company": history[-1]["company"] if history else None,
            "current_title": history[-1]["title"] if history else None,
            "availability": random.choice(["Immediate", "2 weeks", "1 month"]),
            "work_authorization": f"Citizen ({location['country']})",
        },
    }

    if format == "text":
        return _to_text(cv)
    return cv
