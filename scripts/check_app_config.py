#!/usr/bin/env python3
"""Checks app.json (the minimum app version and announcements) before the
Sujuda app can download it.

The app applies the same rules (AppConfig.parse in the app) and ignores the
whole file if any rule is broken, keeping its last good copy - this check
shows the problem on GitHub straight away instead.

Usage: python3 scripts/check_app_config.py app.json
"""
import datetime
import json
import re
import sys
from urllib.parse import urlparse

ALLOWED_LINK_HOSTS = {"sujuda.github.io", "play.google.com"}
MAX_BYTES = 64 * 1024
MAX_TITLE, MAX_MESSAGE, MAX_LINK_LABEL, MAX_DAYS = 60, 300, 30, 14


def check(raw):
    if len(raw) > MAX_BYTES:
        return ["The file is larger than 64 KB."]
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        return [f"Not valid JSON (line {e.lineno}): check for a missing comma or quote."]
    if not isinstance(data, dict):
        return ["The file must be an object { ... }."]
    errors = []
    if data.get("version") != 1:
        errors.append('"version" must be 1.')
    mb = data.get("minBuild", 0)
    if not isinstance(mb, int) or isinstance(mb, bool) or mb < 0:
        errors.append('"minBuild" must be a whole number, 0 or more.')
    items = data.get("announcements", [])
    if not isinstance(items, list):
        return errors + ['"announcements" must be a list [ ... ].']
    ids = set()
    for i, a in enumerate(items, 1):
        where = f"Announcement {i}"
        if not isinstance(a, dict):
            errors.append(f"{where}: must be an object {{ ... }}.")
            continue

        def text(key, limit, required=True):
            v = a.get(key)
            if v is None and not required:
                return None
            if not isinstance(v, str) or not v.strip():
                errors.append(f'{where}: "{key}" is missing.')
                return None
            if len(v) > limit:
                errors.append(f'{where}: "{key}" is longer than {limit} characters ({len(v)}).')
            if "<" in v or ">" in v:
                errors.append(f'{where}: "{key}" may not contain < or >.')
            return v

        def date(key):
            v = a.get(key)
            if not isinstance(v, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", v):
                errors.append(f'{where}: "{key}" must be a date like 2027-03-20.')
                return None
            try:
                return datetime.date.fromisoformat(v)
            except ValueError:
                errors.append(f'{where}: "{key}" is not a real date.')
                return None

        aid = text("id", 60)
        if aid is not None:
            if not re.fullmatch(r"[a-z0-9-]+", aid):
                errors.append(f'{where}: "id" may only use lowercase letters, digits and dashes.')
            if aid in ids:
                errors.append(f'{where}: "id" is used twice.')
            ids.add(aid)
        text("title", MAX_TITLE)
        text("message", MAX_MESSAGE)
        text("linkLabel", MAX_LINK_LABEL, required=False)
        start, end = date("start"), date("end")
        if start and end:
            if end < start:
                errors.append(f'{where}: "end" is before "start".')
            elif (end - start).days + 1 > MAX_DAYS:
                errors.append(f"{where}: shown for more than {MAX_DAYS} days.")
        link = a.get("link")
        if link is not None:
            u = urlparse(link) if isinstance(link, str) else None
            if not u or u.scheme != "https" or u.hostname not in ALLOWED_LINK_HOSTS or u.username:
                errors.append(f'{where}: "link" must start with https:// and be on {" or ".join(sorted(ALLOWED_LINK_HOSTS))}.')
    return errors


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "app.json"
    problems = check(open(path, encoding="utf-8").read())
    for p in problems:
        print(f"::error title=app.json::{p}")
        print(p)
    if problems:
        print("The app will ignore this version of app.json and keep the last good one.")
        sys.exit(1)
    print("OK: app.json is fine.")
