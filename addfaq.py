import sys, json, re

def add_tool_faq(path, items):
    """items: list of (question, answer). Appends to FAQPage JSON-LD and to visible body FAQ, in the same order."""
    s = open(path, encoding='utf-8').read()

    # --- JSON-LD: find the FAQPage block ---
    blocks = [m for m in re.finditer(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', s, re.S)]
    target = None
    for m in blocks:
        if '"FAQPage"' in m.group(1):
            target = m
    if target is None:
        raise SystemExit(f"no FAQPage in {path}")
    data = json.loads(target.group(1))
    for q, a in items:
        data["mainEntity"].append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a}
        })
    new_json = json.dumps(data, indent=2, ensure_ascii=False)
    s = s[:target.start(1)] + new_json + s[target.end(1):]

    # --- Body: append after the last visible FAQ <p> ---
    h3s = list(re.finditer(r'<h3 style="font-family: var\(--font-display\);[^"]*">(.*?)</h3>\s*\n\s*<p style="color: var\(--brown-mid\);[^"]*">.*?</p>', s, re.S))
    if not h3s:
        raise SystemExit(f"no body FAQ h3/p pattern in {path}")
    last = h3s[-1]
    h3style = 'font-family: var(--font-display); font-size: 1.05rem; color: var(--brown); margin-bottom: 8px; margin-top: 18px;'
    pstyle  = 'color: var(--brown-mid); line-height: 1.7; margin-bottom: 16px;'
    add = ""
    for q, a in items:
        add += f'\n\n    <h3 style="{h3style}">{q}</h3>\n    <p style="{pstyle}">{a}</p>'
    s = s[:last.end()] + add + s[last.end():]
    open(path, 'w', encoding='utf-8').write(s)
    print("OK", path, "->", len(data["mainEntity"]), "faqs")
