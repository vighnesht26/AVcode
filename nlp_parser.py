"""Turn a sentence like "If Russia stops oil exports" into a Scenario.
Rule-based NLP (no ML): normalise text -> match entities from a gazetteer (countries, goods) -> fuzzy-match typos -> read intensity words/percentages."""
import re, difflib
from dataclasses import dataclass, field
import config

@dataclass
class Scenario:
    countries: list
    hs: list = field(default_factory=list)      # empty = all tracked goods
    severity: float = 1.0
    notes: list = field(default_factory=list)
    text: str = ""

def _clean(s):                                   # lowercase, punctuation -> spaces, so "China, Hong Kong SAR" and user text compare fairly
    return " " + re.sub(r"\s+", " ", re.sub(r"[^a-z0-9% ]", " ", s.lower())) + " "

def _find_countries(low, known):
    names = {_clean(k).strip(): k for k in known}
    names.update({a: c for a, c in config.COUNTRY_ALIASES.items() if c in known})
    found = []
    for n in sorted(names, key=len, reverse=True):                 # longest first: "south korea" before "korea"
        if re.search(rf"\b{re.escape(n)}\b", low):
            if names[n] not in found: found.append(names[n])
            low = re.sub(rf"\b{re.escape(n)}\b", " ", low)
    reserved = {w for k in config.COMMODITY_KEYWORDS for w in k.split()} | {"stops", "stop", "stopped", "exports", "export", "import", "imports", "supply", "supplies", "shipments"}
    single = [n for n in names if " " not in n]
    for tok in set(re.findall(r"[a-z]{5,}", low)) - reserved:      # typo tolerance ("rusia" -> russia)
        m = difflib.get_close_matches(tok, single, n=1, cutoff=.85)
        if m and names[m[0]] not in found: found.append(names[m[0]])
    return found

def _find_goods(low):
    hs = []
    for phrase in sorted(config.COMMODITY_KEYWORDS, key=len, reverse=True):
        pat = rf"\b{re.escape(phrase)}s?\b" if " " in phrase or len(phrase) <= 4 else rf"\b{re.escape(phrase)}\w*"
        if re.search(pat, low):
            for h in config.COMMODITY_KEYWORDS[phrase]:
                if h not in hs: hs.append(h)
            low = re.sub(pat, " ", low)                            # so "edible oil" is not also read as plain "oil"
    return hs

def _severity(text, low):
    m = re.search(r"(\d+(?:\.\d+)?)\s*(%|percent|per cent)", text.lower())
    if m: return min(1.0, float(m.group(1)) / 100), f"{m.group(1)}% stated"
    for sev, words in sorted(config.SEVERITY_WORDS.items()):        # 0.25 first, then 0.5, then 1.0: weaker words win over "cut"
        if any(re.search(rf"\b{w}", low) for w in words): return sev, "from wording"
    return 1.0, "assumed full stop"

def parse(text, known_countries):
    low = _clean(text); notes = []; countries = []
    war = any(re.search(rf"\b{w}", low) for w in config.WAR_WORDS)
    if any(f" {t} " in low for t in config.GULF_TRIGGERS) or (re.search(r"\biran\b", low) and war):
        countries = [c for c in config.GULF_COUNTRIES if c in known_countries]
        notes.append("Gulf shipping route treated as blocked (Iran itself now sells India little; the real risk is Gulf transit)")
    for c in _find_countries(low, known_countries):
        if c not in countries: countries.append(c)
    hs = _find_goods(low); sev, why = _severity(text, low); notes.append(f"severity {sev:.0%} ({why})")
    if not countries: notes.append("no country recognised")
    return Scenario(countries, hs, sev, notes, text)
