
import config
from nlp_parser import Scenario
from io_model import assess, why_chain

def options(g):
    a, b = g.window(); tot = g.totals(a, b); xy = g.coords(); names, C, conc = g.structure()
    cs = sorted((c for c in g.countries() if c != "India"), key=lambda c: -tot.get(c, 0))
    return {"countries": [c for c in cs if tot.get(c, 0) > 0], "goods": [{"hs": h, "name": v["name"]} for h, v in conc.items()],
            "window": [a, b], "has_coords": len(xy)}

def run(g, sc, as_of=None, no_refill=False):
    a, b = g.window(as_of); shares = g.shares(a, b); names, C, conc = g.structure();
    rows, rank, l0 = assess(sc, shares, conc, names, C, refill_override=0.0 if no_refill else None)
    ranking = [{"industry": n, "loss": l, "direct": d, "why": why_chain(i, l0, C, names, conc, rows) if k < 5 else []} for k, (i, n, l, d) in enumerate(rank[:10])]
    return {
        "suppliers": sc.countries, 
        "severity": sc.severity, 
        "window": [a, b],
        "direct": [
            {"name": r["name"], 
             "lost": r["lost_share"], 
             "refill": r["refill"], 
             "uncovered": r["net_loss"]
             } 
             for r in rows
             ],
            "ranking": ranking, 
            }

def scenario(g, country, hs="all", sev=1.0, as_of=None):
    known = g.countries(); cs = [c for c in config.GULF_COUNTRIES if c in known] if country == "__GULF__" else [country]
    return run(g, Scenario(cs, [] if hs in ("all", "", None) else [int(hs)], max(.05, min(1.0, sev))), as_of)
