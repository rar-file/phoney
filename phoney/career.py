from __future__ import annotations

import json
import random
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

DATA_DIR = Path(__file__).parent / "data" / "career"


def _load_json(path: Path) -> Optional[dict]:
    try:
        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return None


def _load_lines(path: Path) -> List[str]:
    try:
        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                return [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith("#")]
    except Exception:
        pass
    return []


DEFAULT_JOB_FAMILIES: Dict[str, List[str]] = {
    "software_engineer": [
        "Software Engineer", "Backend Engineer", "Frontend Engineer", "Full-Stack Engineer",
        "Platform Engineer", "Systems Engineer", "Mobile Engineer", "Data Engineer",
        "Embedded Engineer", "Site Reliability Engineer", "DevOps Engineer",
    ],
    "data_scientist": ["Data Scientist", "ML Engineer", "Data Analyst", "Research Scientist"],
    "product_manager": ["Product Manager", "Technical Product Manager"],
    "devops_engineer": ["DevOps Engineer", "Site Reliability Engineer", "Cloud Engineer"],
    "designer": ["Product Designer", "UX Designer", "UI Designer", "UX Researcher"],
    "qa_engineer": ["QA Engineer", "SDET", "Test Engineer"],
    "security_engineer": ["Security Engineer", "Application Security Engineer", "Security Analyst"],
    "it_support": ["IT Support Specialist", "Help Desk Technician"],
    "sales": ["Sales Representative", "Account Executive", "Sales Engineer"],
    "marketing": ["Marketing Specialist", "Growth Marketer", "SEO Specialist", "Content Marketer"],
    "hr": ["HR Specialist", "Recruiter", "People Operations"],
    "finance": ["Financial Analyst", "Accountant", "Controller"],
    "operations": ["Operations Analyst", "Operations Manager"],
    "business_analyst": ["Business Analyst"],
    "project_manager": ["Project Manager", "Program Manager"],
    "customer_success": ["Customer Success Manager", "Customer Support Specialist"],
    "technical_writer": ["Technical Writer", "Documentation Specialist"],
    "network_engineer": ["Network Engineer", "Network Administrator"],
}

LEVELS_ORDERED = [
    "Intern", "Junior", "Mid", "Senior", "Lead", "Staff", "Principal", "Manager", "Director", "VP", "C-level"
]

DEFAULT_SALARY_RANGES: Dict[str, Dict[str, Dict[str, Tuple[int, int, str]]]] = {
    "en_US": {
        "software_engineer": {
            "Intern": (20000, 45000, "USD"),
            "Junior": (70000, 100000, "USD"),
            "Mid": (100000, 140000, "USD"),
            "Senior": (140000, 190000, "USD"),
            "Lead": (170000, 220000, "USD"),
            "Staff": (180000, 240000, "USD"),
            "Principal": (200000, 280000, "USD"),
            "Manager": (160000, 220000, "USD"),
            "Director": (200000, 280000, "USD"),
            "VP": (250000, 350000, "USD"),
            "C-level": (300000, 600000, "USD"),
        },
        "data_scientist": {
            "Intern": (20000, 45000, "USD"),
            "Junior": (65000, 95000, "USD"),
            "Mid": (95000, 135000, "USD"),
            "Senior": (130000, 180000, "USD"),
            "Lead": (160000, 210000, "USD"),
            "Staff": (170000, 230000, "USD"),
            "Principal": (190000, 260000, "USD"),
            "Manager": (150000, 210000, "USD"),
            "Director": (190000, 260000, "USD"),
            "VP": (230000, 330000, "USD"),
            "C-level": (280000, 550000, "USD"),
        },
        "product_manager": {
            "Intern": (20000, 45000, "USD"),
            "Junior": (70000, 105000, "USD"),
            "Mid": (105000, 145000, "USD"),
            "Senior": (140000, 190000, "USD"),
            "Lead": (170000, 220000, "USD"),
            "Manager": (150000, 210000, "USD"),
            "Director": (190000, 260000, "USD"),
            "VP": (230000, 330000, "USD"),
            "C-level": (280000, 550000, "USD"),
        },
        "devops_engineer": {
            "Junior": (70000, 100000, "USD"),
            "Mid": (100000, 140000, "USD"),
            "Senior": (140000, 185000, "USD"),
            "Lead": (160000, 210000, "USD"),
            "Manager": (150000, 200000, "USD"),
        },
        "designer": {
            "Junior": (60000, 90000, "USD"),
            "Mid": (90000, 125000, "USD"),
            "Senior": (120000, 160000, "USD"),
            "Lead": (140000, 185000, "USD"),
        },
        "qa_engineer": {
            "Junior": (60000, 90000, "USD"),
            "Mid": (90000, 120000, "USD"),
            "Senior": (115000, 150000, "USD"),
        },
        "security_engineer": {
            "Junior": (80000, 110000, "USD"),
            "Mid": (110000, 150000, "USD"),
            "Senior": (145000, 195000, "USD"),
        },
        "it_support": {
            "Junior": (40000, 60000, "USD"),
            "Mid": (60000, 80000, "USD"),
            "Senior": (80000, 100000, "USD"),
        },
        "sales": {
            "Junior": (50000, 80000, "USD"),
            "Mid": (80000, 120000, "USD"),
            "Senior": (120000, 180000, "USD"),
            "Manager": (130000, 200000, "USD"),
        },
        "marketing": {
            "Junior": (50000, 80000, "USD"),
            "Mid": (80000, 115000, "USD"),
            "Senior": (110000, 150000, "USD"),
            "Manager": (120000, 170000, "USD"),
        },
        "hr": {
            "Junior": (50000, 75000, "USD"),
            "Mid": (75000, 100000, "USD"),
            "Senior": (95000, 130000, "USD"),
            "Manager": (110000, 150000, "USD"),
        },
        "finance": {
            "Junior": (60000, 90000, "USD"),
            "Mid": (90000, 125000, "USD"),
            "Senior": (120000, 160000, "USD"),
            "Manager": (140000, 190000, "USD"),
        },
        "operations": {
            "Junior": (50000, 80000, "USD"),
            "Mid": (80000, 110000, "USD"),
            "Senior": (105000, 140000, "USD"),
            "Manager": (120000, 170000, "USD"),
        },
        "business_analyst": {
            "Junior": (60000, 90000, "USD"),
            "Mid": (90000, 120000, "USD"),
            "Senior": (115000, 150000, "USD"),
        },
        "project_manager": {
            "Junior": (65000, 95000, "USD"),
            "Mid": (95000, 125000, "USD"),
            "Senior": (120000, 160000, "USD"),
            "Manager": (130000, 180000, "USD"),
        },
        "customer_success": {
            "Junior": (45000, 70000, "USD"),
            "Mid": (70000, 100000, "USD"),
            "Senior": (95000, 130000, "USD"),
            "Manager": (110000, 150000, "USD"),
        },
        "technical_writer": {
            "Junior": (60000, 85000, "USD"),
            "Mid": (85000, 110000, "USD"),
            "Senior": (105000, 135000, "USD"),
        },
        "network_engineer": {
            "Junior": (65000, 90000, "USD"),
            "Mid": (90000, 120000, "USD"),
            "Senior": (115000, 150000, "USD"),
        },
    },
    "en_GB": {
        "software_engineer": {
            "Intern": (18000, 25000, "GBP"),
            "Junior": (30000, 45000, "GBP"),
            "Mid": (45000, 65000, "GBP"),
            "Senior": (65000, 90000, "GBP"),
            "Lead": (80000, 105000, "GBP"),
            "Manager": (70000, 100000, "GBP"),
            "Director": (100000, 140000, "GBP"),
        },
        "data_scientist": {
            "Intern": (18000, 25000, "GBP"),
            "Junior": (30000, 45000, "GBP"),
            "Mid": (45000, 65000, "GBP"),
            "Senior": (65000, 90000, "GBP"),
            "Lead": (80000, 105000, "GBP"),
            "Manager": (70000, 100000, "GBP"),
        },
        "product_manager": {
            "Junior": (35000, 50000, "GBP"),
            "Mid": (50000, 75000, "GBP"),
            "Senior": (75000, 100000, "GBP"),
            "Manager": (80000, 110000, "GBP"),
        },
    },
    "de_DE": {
        "software_engineer": {
            "Intern": (18000, 30000, "EUR"),
            "Junior": (45000, 60000, "EUR"),
            "Mid": (60000, 80000, "EUR"),
            "Senior": (80000, 105000, "EUR"),
            "Lead": (95000, 125000, "EUR"),
            "Manager": (90000, 120000, "EUR"),
            "Director": (110000, 150000, "EUR"),
        },
        "data_scientist": {
            "Junior": (42000, 60000, "EUR"),
            "Mid": (60000, 80000, "EUR"),
            "Senior": (80000, 110000, "EUR"),
        },
    },
}

DEFAULT_SKILLS: Dict[str, List[str]] = {
    "software_engineer": [
        "Python", "JavaScript", "TypeScript", "Java", "C#", "Go", "C++", "SQL",
        "REST", "GraphQL", "Docker", "Kubernetes", "AWS", "Azure", "GCP",
        "Microservices", "CI/CD", "Unit Testing", "TDD", "Linux", "Git",
    ],
    "data_scientist": [
        "Python", "R", "Pandas", "NumPy", "scikit-learn", "TensorFlow",
        "PyTorch", "SQL", "Statistics", "A/B Testing", "Feature Engineering", "Data Visualization",
    ],
    "product_manager": [
        "Roadmapping", "User Research", "A/B Testing", "Analytics",
        "Backlog Management", "Stakeholder Management", "PRD Writing", "KPIs",
    ],
    "devops_engineer": [
        "CI/CD", "Kubernetes", "Docker", "Terraform", "Ansible", "Prometheus",
        "Grafana", "Linux", "SRE", "AWS", "Azure", "GCP", "IaC",
    ],
    "designer": ["Figma", "Sketch", "Wireframing", "Prototyping", "UX Research", "UI Design", "Design Systems"],
    "qa_engineer": ["Test Automation", "Selenium", "Cypress", "API Testing", "Performance Testing", "Unit Testing", "Playwright"],
    "security_engineer": ["Threat Modeling", "AppSec", "IAM", "SIEM", "Vulnerability Management", "Penetration Testing", "OWASP Top 10"],
    "it_support": ["Windows", "macOS", "Networking", "Active Directory", "Ticketing Systems", "Scripting", "M365"],
    "sales": ["Prospecting", "CRM", "Negotiation", "Presentation", "Lead Qualification", "Forecasting", "Discovery"],
    "marketing": ["SEO", "SEM", "Content Marketing", "Email Marketing", "Analytics", "Copywriting", "Social Media"],
    "hr": ["Recruiting", "Onboarding", "Employee Relations", "HRIS", "Compensation & Benefits", "Performance Management"],
    "finance": ["Financial Modeling", "Accounting", "Budgeting", "Forecasting", "Excel", "GAAP"],
    "operations": ["Process Improvement", "Project Management", "Logistics", "KPI Tracking", "SOPs"],
    "business_analyst": ["Requirements Gathering", "Process Mapping", "SQL", "Reporting", "Stakeholder Management"],
    "project_manager": ["Project Planning", "Risk Management", "Scheduling", "Agile", "Scrum", "PMBOK"],
    "customer_success": ["Onboarding", "Account Management", "Renewals", "Escalation Management", "NPS"],
    "technical_writer": ["Documentation", "API Writing", "DITA", "Editing", "Information Architecture"],
    "network_engineer": ["Routing", "Switching", "Firewalls", "VPN", "BGP", "OSPF", "Wi-Fi"],
}

DEFAULT_COMPANIES: Dict[str, List[str]] = {
    "en_US": [
        "Acme Corp", "Globex Corporation", "Initech", "Umbrella Corp", "Hooli",
        "Stark Industries", "Wayne Enterprises", "Vandelay Industries", "Wonka Industries",
        "Blue Pine Labs", "Silverline Systems", "Quantum Apex", "Nimbus Dynamics",
        "Sapphire Solutions", "Vertex Analytics", "Orion Ventures", "Pioneer Tech",
        "Crescent Networks", "Redwood Robotics", "Evergreen Softworks", "SummitForge",
        "Ironclad Security", "Nebula Cloud", "Harbor Financial", "Atlas Operations",
    ],
    "en_GB": [
        "Acme Ltd", "Globex UK", "Initech UK", "Hooli Europe", "Wonka UK",
        "Silverline UK", "Orion UK", "Harbor UK", "Vertex UK", "SummitForge UK",
    ],
    "de_DE": [
        "Acme GmbH", "Globex GmbH", "Initech GmbH", "Hooli GmbH",
        "Orion GmbH", "Vertex GmbH", "Harbor GmbH", "SummitForge GmbH",
    ],
}


def _job_families() -> Dict[str, List[str]]:
    data = _load_json(DATA_DIR / "job_families.json")
    return data if isinstance(data, dict) and data else DEFAULT_JOB_FAMILIES


def _skills_map() -> Dict[str, List[str]]:
    data = _load_json(DATA_DIR / "skills.json")
    return data if isinstance(data, dict) and data else DEFAULT_SKILLS


def _salary_ranges(locale: str) -> Dict[str, Dict[str, Tuple[int, int, str]]]:
    data = _load_json(DATA_DIR / f"salary_ranges.{locale}.json")
    if isinstance(data, dict) and data:
        normalized: Dict[str, Dict[str, Tuple[int, int, str]]] = {}
        for fam, levels in data.items():
            normalized[fam] = {}
            for lvl, payload in levels.items():
                if isinstance(payload, dict):
                    lo, hi = int(payload["min"]), int(payload["max"])
                    cur = payload.get("currency", "USD")
                else:
                    lo, hi, cur = payload
                normalized[fam][lvl] = (lo, hi, cur)
        return normalized
    return DEFAULT_SALARY_RANGES.get(locale, DEFAULT_SALARY_RANGES.get("en_US", {}))


def _companies_for_locale(locale: str) -> List[str]:
    lines = _load_lines(DATA_DIR / f"companies.{locale}.txt")
    if lines:
        return lines
    return DEFAULT_COMPANIES.get(locale, DEFAULT_COMPANIES.get("en_US", ["Acme Corp"]))


def _pick_family(family: Optional[str]) -> str:
    families = _job_families()
    return family if family in families else random.choice(list(families.keys()))


def _pick_level(level: Optional[str]) -> str:
    if level in LEVELS_ORDERED:
        return level
    return random.choice(["Junior", "Mid", "Senior", "Lead"])


def _title_from_family_and_level(family: str, level: str) -> str:
    families = _job_families()
    base = random.choice(families[family])
    if level in {"Manager", "Director", "VP", "C-level"}:
        core = base.replace(" Engineer", "").replace(" Designer", "").replace(" Scientist", "")
        if level == "Manager":
            if family in {"software_engineer", "devops_engineer", "security_engineer", "qa_engineer"}:
                return "Engineering Manager"
            if family == "product_manager":
                return "Product Manager"
            return f"{core} Manager"
        if level == "Director":
            return f"Director of {core}"
        if level == "VP":
            return f"VP of {core}"
        if level == "C-level":
            if "Product" in base:
                return "Chief Product Officer"
            if "Security" in base:
                return "Chief Information Security Officer"
            if "Data" in base:
                return "Chief Data Officer"
            return "Chief Technology Officer"
    if level == "Intern":
        return f"{base} Intern"
    return f"{level} {base}"


def generate_job_title(locale: str = "en_US", family: Optional[str] = None, level: Optional[str] = None) -> Dict[str, str]:
    fam = _pick_family(family)
    lvl = _pick_level(level)
    title = _title_from_family_and_level(fam, lvl)
    return {"title": title, "family": fam, "level": lvl, "locale": locale}


def _salary_for(locale: str, family: str, level: str) -> Optional[Tuple[int, int, str]]:
    fams = _salary_ranges(locale)
    fam = fams.get(family)
    if not fam:
        return None
    if level in fam:
        return fam[level]
    for fb in ["Senior", "Mid", "Junior"]:
        if fb in fam:
            return fam[fb]
    return None


def generate_salary(locale: str = "en_US", family: Optional[str] = None, level: Optional[str] = None, title: Optional[str] = None) -> Dict[str, object]:
    fam = _pick_family(family)
    lvl = _pick_level(level)
    rng = _salary_for(locale, fam, lvl)
    if not rng:
        rng = (50000, 100000, "USD")
    lo, hi, currency = rng
    return {
        "family": fam,
        "level": lvl,
        "min": int(lo),
        "max": int(hi),
        "currency": currency,
        "period": "year",
        "locale": locale,
        "title": title,
    }


def _random_date_between(start: date, end: date) -> date:
    days = (end - start).days
    return start if days <= 0 else start + timedelta(days=random.randint(0, days))


def generate_employment_history(
    years: int = 10,
    locale: str = "en_US",
    family: Optional[str] = None,
    min_jobs: int = 1,
    max_jobs: int = 5,
) -> List[Dict[str, object]]:
    fam = _pick_family(family)
    today = date.today()
    window_start = today - timedelta(days=int(years * 365.25))
    num_jobs = max(min_jobs, min(max_jobs, random.randint(min_jobs, max_jobs)))

    companies = _companies_for_locale(locale)
    entries: List[Dict[str, object]] = []
    current_end = today
    for _ in range(num_jobs):
        duration_days = random.randint(365, 365 * 4)
        start_dt = max(window_start, current_end - timedelta(days=duration_days))
        if start_dt >= current_end:
            break
        job = generate_job_title(locale=locale, family=fam)
        sal = generate_salary(locale=locale, family=fam, level=job["level"], title=job["title"])
        entries.append({
            "company": random.choice(companies),
            "title": job["title"],
            "family": fam,
            "level": job["level"],
            "start_date": start_dt.isoformat(),
            "end_date": current_end.isoformat(),
            "salary": sal,
            "locale": locale,
        })
        current_end = start_dt - timedelta(days=random.randint(14, 120))
        if current_end <= window_start:
            break

    entries.reverse()
    return entries


def generate_skills(family: str, level: Optional[str] = None, count: Optional[int] = None) -> List[str]:
    skills_map = _skills_map()
    skills = skills_map.get(family, [])
    if not skills:
        return []
    random.shuffle(skills)
    lvl = level if level in LEVELS_ORDERED else None
    base_n = 8
    if lvl in {"Senior", "Lead", "Staff", "Principal"}:
        base_n += 2
    if lvl in {"Manager", "Director", "VP", "C-level"}:
        base_n = max(6, base_n - 2)
    n = count if count is not None else min(len(skills), base_n)
    return skills[:max(1, n)]


def experience_level_from_years(years: float) -> str:
    if years < 1:
        return "Intern"
    if years < 3:
        return "Junior"
    if years < 6:
        return "Mid"
    if years < 10:
        return "Senior"
    if years < 14:
        return "Lead"
    if years < 18:
        return "Staff"
    return "Principal"


__all__ = [
    "generate_job_title",
    "generate_salary",
    "generate_employment_history",
    "generate_skills",
    "experience_level_from_years",
]
