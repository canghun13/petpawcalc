#!/usr/bin/env python3
"""Build an IndexNow payload from the files changed in the current push.

Usage: indexnow_payload.py <host> <key> <changed-files-file> [out.json]

Pass "--all" as <changed-files-file> to submit every indexable URL on the site
instead of only the changed ones (used for manual workflow_dispatch runs).
Writes nothing and exits 0 when no indexable URL changed.
"""
import json
import os
import re
import sys


def urls_from_changed(host, paths):
    urls = set()
    for f in paths:
        f = f.strip()
        if not f or not os.path.exists(f):
            continue  # deleted files: nothing to submit
        if f.startswith("_posts/") and f.endswith(".md"):
            text = open(f, encoding="utf-8").read()
            m = re.search(r"^slug:\s*(\S+)", text, re.M)
            if m:
                urls.add("https://%s/blog/%s/" % (host, m.group(1).strip('"\'')))
        elif f.startswith(("tools/", "checklists/")) and f.endswith(".html"):
            # Section indexes are served at the directory URL, not index.html
            if f.endswith("/index.html"):
                urls.add("https://%s/%s" % (host, f[: -len("index.html")]))
            else:
                urls.add("https://%s/%s" % (host, f))
        elif f == "index.html":
            urls.add("https://%s/" % host)
    return sorted(urls)


def all_site_files():
    """Every file that maps to a public URL."""
    import glob
    return (
        glob.glob("_posts/*.md")
        + glob.glob("tools/*.html")
        + glob.glob("checklists/*.html")
        + ["index.html"]
    )


def main():
    host, key, changed_file = sys.argv[1], sys.argv[2], sys.argv[3]
    out = sys.argv[4] if len(sys.argv) > 4 else "payload.json"

    if changed_file == "--all":
        paths = all_site_files()
    else:
        with open(changed_file, encoding="utf-8") as fh:
            paths = fh.read().splitlines()

    urls = urls_from_changed(host, paths)
    if not urls:
        print("No indexable URLs changed.")
        return 0

    # IndexNow accepts up to 10,000 URLs per request; we will never approach it.
    payload = {
        "host": host,
        "key": key,
        "keyLocation": "https://%s/%s.txt" % (host, key),
        "urlList": urls,
    }
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    print("Prepared %d URL(s):" % len(urls))
    for u in urls:
        print("  " + u)
    return 0


if __name__ == "__main__":
    sys.exit(main())
