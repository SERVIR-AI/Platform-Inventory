#!/usr/bin/env python3
"""Refresh the mechanical parts of the SERVIR Platform Inventory.

Two things go stale fastest and are purely factual, so they are the two things
worth automating:

  1. The SERVIR GitHub org repository inventory (six orgs).
  2. The SERVIR Global App Center, which is the only source that carries an
     explicit status badge per service.

Everything else in this register — the build matrices, the NASA asset mapping,
the use cases — involves judgement and is deliberately left to a human.

Writes data/servir-repos.json, data/appcenter.json and data/CHANGES.md.
Exits 0 always; the workflow decides what to do with the diff.

Stdlib only. No requirements file.
"""
import html, json, os, re, sys, time, urllib.request, urllib.error
from datetime import datetime, timezone

ORGS = ["SERVIR-AI", "SERVIR", "Servir-Mekong", "SERVIR-Amazonia", "SERVIRSEA", "pyregence"]
DATA = os.path.join(os.path.dirname(__file__), "..", "data")
UA = "SERVIR-Platform-Inventory-sweep/1.0 (+https://github.com/SERVIR-AI/Platform-Inventory)"


def get(url, token=None, accept=None, tries=3):
    for attempt in range(tries):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        if accept:
            req.add_header("Accept", accept)
        if token:
            req.add_header("Authorization", f"Bearer {token}")
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (403, 429) and attempt < tries - 1:
                time.sleep(5 * (attempt + 1))       # secondary rate limit
                continue
            return e.code, ""
        except Exception:
            if attempt < tries - 1:
                time.sleep(2)
                continue
            return 0, ""
    return 0, ""


def fetch_repos(token):
    """Org repo inventory. Inside Actions the GITHUB_TOKEN makes this the easy path —
    the org endpoint that is blocked from a sandbox works fine here."""
    out, errors = {}, []
    for org in ORGS:
        repos, page = [], 1
        while True:
            status, body = get(
                f"https://api.github.com/orgs/{org}/repos?per_page=100&page={page}&type=public",
                token, "application/vnd.github+json")
            if status != 200:
                errors.append(f"{org}: HTTP {status}")
                break
            batch = json.loads(body)
            if not batch:
                break
            for r in batch:
                repos.append({
                    "name": r["name"],
                    "description": r.get("description") or "",
                    "language": r.get("language") or "",
                    "updated_at": (r.get("pushed_at") or "")[:10],
                    "archived": bool(r.get("archived")),
                    "license": ((r.get("license") or {}).get("spdx_id") or ""),
                    "stars": r.get("stargazers_count", 0),
                })
            if len(batch) < 100:
                break
            page += 1
        out[org] = sorted(repos, key=lambda x: x["updated_at"], reverse=True)
    return out, errors


# The App Center's status lives ONLY on the listing page, as a CSS class on each
# card — detail pages carry no status at all, and their <title> is boilerplate
# ("SAMS - Detail") identical for every app. An earlier version of this script
# walked 95 detail pages looking for status words in the text; it found none, and
# would have reported silence forever. Verified against the live DOM on
# 9 September 2026: this pattern parses 79/79 cards and all 5 inactive entries.
CARD_RE = re.compile(
    r'<div class="inner img-wrapper\s*([^"]*)"'      # 1: trailing classes, may contain "inactive"
    r'[\s\S]*?href="/detail/(\d+)"'                  # 2: app id
    r'[\s\S]*?<p class="app-title">([\s\S]*?)</p>'   # 3: app name
)
APPCENTER_MIN = 20      # a real listing has ~79; far fewer means the markup moved


def fetch_appcenter():
    """One request to the listing page. Status is the `inactive` class or its absence —
    a binary, which is all this source actually publishes."""
    status_code, body = get("https://appcenter.servirglobal.net/")
    if status_code != 200 or not body.strip():
        return {}, [f"listing page returned HTTP {status_code}"]
    apps, notes = {}, []
    for extra, num, name in CARD_RE.findall(body):
        apps[num] = {
            "title": html.unescape(re.sub(r"\s+", " ", name)).strip(),
            "status": "Inactive" if re.search(r"\binactive\b", extra) else "Active",
        }
    if len(apps) < APPCENTER_MIN:
        notes.append(f"listing parsed only {len(apps)} cards — markup has probably changed")
    return apps, notes


def load(name):
    try:
        with open(os.path.join(DATA, name), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def save(name, obj):
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, name), "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, sort_keys=True, ensure_ascii=False)
        f.write("\n")


def diff_repos(old, new):
    lines = []
    if not old:
        return ["Baseline snapshot created — no prior data to compare."]
    for org in ORGS:
        o = {r["name"]: r for r in (old.get(org) or [])}
        n = {r["name"]: r for r in (new.get(org) or [])}
        for name in sorted(set(n) - set(o)):
            lines.append(f"- **NEW REPO** `{org}/{name}` — {n[name]['description'] or 'no description'}")
        for name in sorted(set(o) - set(n)):
            lines.append(f"- **REPO GONE** `{org}/{name}` (made private, renamed or deleted)")
        for name in sorted(set(o) & set(n)):
            if o[name]["updated_at"] != n[name]["updated_at"]:
                lines.append(f"- activity: `{org}/{name}` last push {o[name]['updated_at']} → {n[name]['updated_at']}")
            if o[name]["archived"] != n[name]["archived"]:
                state = "archived" if n[name]["archived"] else "un-archived"
                lines.append(f"- **{state.upper()}** `{org}/{name}`")
    return lines


def diff_apps(old, new):
    lines = []
    if not old:
        return ["Baseline snapshot created — no prior data to compare."]
    for k in sorted(set(new) - set(old), key=int):
        lines.append(f"- **NEW SERVICE** App Center /detail/{k} — {new[k]['title']}")
    for k in sorted(set(old) - set(new), key=int):
        lines.append(f"- **SERVICE GONE** App Center /detail/{k} — {old[k]['title']}")
    for k in sorted(set(old) & set(new), key=int):
        if old[k]["status"] != new[k]["status"]:
            a = old[k]["status"] or "(none)"
            b = new[k]["status"] or "(none)"
            lines.append(f"- **STATUS CHANGE** {new[k]['title']}: {a} → {b}")
    return lines


def main():
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    old_repos, old_apps = load("servir-repos.json"), load("appcenter.json")
    repos, repo_errors = fetch_repos(token)
    apps, app_notes = fetch_appcenter()

    # Guard against a bad run wiping a good baseline. If a fetch comes back
    # empty because the far end blocked us or changed shape, keep the previous
    # snapshot and say so — otherwise the next sweep reports every service as
    # brand new, which is worse than no data.
    stale_notes = []
    if not any(repos.values()) and old_repos:
        stale_notes.append("Repository fetch returned nothing for every org — "
                           "keeping the previous snapshot rather than overwriting it. "
                           "Check whether the API or the token changed.")
        repos = old_repos
    if not apps and old_apps:
        stale_notes.append("App Center crawl returned nothing — keeping the previous "
                           "snapshot. The site may have changed shape or blocked the crawler.")
        apps = old_apps

    # Second failure mode, subtler than an empty response: the page loads but the
    # card markup has moved, so the parser matches only a handful. Status itself is
    # Active/Inactive by construction now, so card COUNT is the signal to watch — a
    # thin parse must not be allowed to read as "74 services disappeared this week".
    if app_notes:
        stale_notes += [f"App Center: {n}." for n in app_notes]
        if old_apps:
            apps = old_apps

    first_run = old_repos is None and old_apps is None
    if first_run:
        changes = ["Baseline snapshot created — no prior data to compare."]
    else:
        changes = diff_repos(old_repos, repos) + diff_apps(old_apps, apps)
        changes = [c for c in changes if "Baseline snapshot" not in c]

    save("servir-repos.json", repos)
    save("appcenter.json", apps)

    total_repos = sum(len(v) for v in repos.values())
    body = [f"# Inventory sweep — {stamp}", ""]
    body.append(f"**{total_repos}** public repositories across {len(ORGS)} organizations · "
                f"**{len(apps)}** App Center services reachable.")
    body.append("")
    if stale_notes:
        body.append("## Attention")
        body += [f"- {n}" for n in stale_notes] + [""]
    if repo_errors:
        body.append("Fetch problems (reported, not silently swallowed):")
        body += [f"- {e}" for e in repo_errors] + [""]
    if changes:
        body.append("## Changes since last sweep")
        body += changes
    else:
        body.append("## No changes since last sweep")
        body.append("")
        body.append("Repository inventory and App Center statuses are unchanged. "
                    "A quiet week is a legitimate result — nothing here is padded to look busy.")
    body.append("")
    body.append("---")
    body.append("")
    body.append("**What this sweep does and does not cover.** It refreshes the two things that are "
                "purely factual and go stale fastest: the org repository inventory and the App Center "
                "status badges. It does **not** touch the build matrices, the NASA asset mapping, or the "
                "use cases — those involve judgement and stay human-edited.")
    body.append("")
    body.append("**Two standing rules for anyone reading a diff here.** A website is evidence about "
                "*publishing*, never about *operations* — do not infer from a stale page that a hub or "
                "service has stopped. And *retired is not excluded*: a service moving to No Longer Active "
                "belongs in the reactivation table, not the bin.")

    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, "CHANGES.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(body) + "\n")

    print("\n".join(body))
    # surface a machine-readable flag for the workflow
    gh_out = os.environ.get("GITHUB_OUTPUT")
    if gh_out:
        with open(gh_out, "a") as f:
            # A stale subsystem has already had its snapshot substituted back in,
            # so its own diff is empty by construction — there is no need to also
            # gate on stale_notes, and doing so was actively wrong: a blocked repo
            # fetch would suppress a real App Center status change in the same run.
            f.write(f"changed={'true' if changes else 'false'}\n")


if __name__ == "__main__":
    main()
