"""NIH grants for the Top scientists page, from NIH RePORTER (https://api.reporter.nih.gov, a public API).

A scientist is matched by the RePORTER investigator profile ids stored in data/scientists.json ("nih": {"profile_ids": [...]}),
not by name, so that people with similar names are never mixed up. A grant counts when the scientist is listed as a
principal investigator on the award itself: sole PI, contact PI or one of multiple PIs (MPI). Not counted: co-investigator
roles (RePORTER does not list them), and subprojects of center or program grants (their "PI" is the subproject leader).
One grant = one core project number, so renewals and supplements of an award are counted once.
NIH intramural research projects (activity codes starting with Z) are not grants and are reported separately.
RePORTER starts in fiscal year 1985 and NIH mostly funds US institutions, so earlier awards and scientists based
abroad will show few or none.
"""
import time
import requests

API = "https://api.reporter.nih.gov/v2/projects/search"
FIELDS = ["CoreProjectNum", "ProjectNum", "FiscalYear", "PrincipalInvestigators", "ProjectTitle", "SubprojectId", "ActivityCode", "IsActive"]


def fetch(profile_ids, user_agent):
    """All project-year records on which any of these investigator profiles is a PI."""
    out, offset, total = [], 0, 1
    while offset < total:
        r = requests.post(API, json={"criteria": {"pi_profile_ids": profile_ids}, "offset": offset, "limit": 500, "include_fields": FIELDS},
                          headers={"User-Agent": user_agent}, timeout=60)
        r.raise_for_status()
        j = r.json()
        total = j["meta"]["total"]
        out += j["results"]
        offset += 500
        time.sleep(1.1)   # RePORTER asks for no more than one request a second
    return out


def tidy(title):
    t = " ".join((title or "").split()).rstrip(":")
    return t.capitalize() if t.isupper() else t


def summarize(results, profile_ids, today):
    """Collapse project-year records into one entry per grant and count them."""
    cores = {}
    for p in results:
        if p.get("subproject_id"):
            continue
        if not any(pi.get("profile_id") in profile_ids for pi in p.get("principal_investigators") or []):
            continue
        core = p.get("core_project_num") or p.get("project_num")
        g = cores.setdefault(core, {"core": core, "activity": p.get("activity_code") or "", "fy": [], "active": False, "npi": 0, "title": ""})
        if not g["fy"] or p["fiscal_year"] >= max(g["fy"]):
            g["title"] = tidy(p.get("project_title"))
        g["fy"].append(p["fiscal_year"])
        g["active"] = g["active"] or bool(p.get("is_active"))
        g["npi"] = max(g["npi"], len(p.get("principal_investigators") or []))
    return build([[g["core"], g["activity"], min(g["fy"]), max(g["fy"]), int(g["active"]), "MPI" if g["npi"] > 1 else "PI", g["title"]] for g in cores.values()], profile_ids, today)


def build(rows, profile_ids, today):
    """rows: [core, activity, first fiscal year, last fiscal year, active 0/1, "PI"|"MPI", title]"""
    grants = [{"core": c, "activity": a, "fy_start": s, "fy_end": e, "active": bool(act), "role": role, "title": tidy(t)} for c, a, s, e, act, role, t in rows]
    extramural = sorted((g for g in grants if not g["activity"].startswith("Z")), key=lambda g: (-g["fy_start"], g["core"]))
    # intramural projects were renumbered from Z01 to ZIA in 2009: count each project serial once
    intramural = {g["core"][-6:] for g in grants if g["activity"].startswith("Z")}
    return {"profile_ids": profile_ids, "grants": len(extramural), "r01": sum(g["activity"] == "R01" for g in extramural),
            "active": sum(g["active"] for g in extramural), "mpi": sum(g["role"] == "MPI" for g in extramural),
            "intramural_projects": len(intramural), "list": extramural, "as_of": today}
