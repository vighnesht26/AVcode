"""Optional text-mode version (uses the NLP parser).   python main.py "If Russia stops oil exports"   or just  python main.py"""
import sys, os
import config, service
from nlp_parser import parse

def get_graph():
        from offline_graph import OfflineGraph; return OfflineGraph()
    
def show(g, text):
    sc = parse(text, g.countries()); print(f"\nUnderstood: {', '.join(sc.countries) or '?'} | goods {sc.hs or 'all'} | {'; '.join(sc.notes)}")
    if not sc.countries: return
    r = service.run(g, sc)
    for d in r["direct"]: print(f"  {d['name'][:42]:42s} lost {d['lost']:.0%}, refilled {d['refill']:.0%}, uncovered {d['uncovered']:.0%}")
    for x in r["ranking"]: print(f"  {x['loss']:6.1%}  {x['industry'][:55]}" + (f"\n          why: {' -> '.join(x['why'])}" if x["why"] else ""))

if __name__ == "__main__":
    g = get_graph(); t = " ".join(sys.argv[1:])
    if t: show(g, t)
    else:
        while (t := input("\nWhat if...? > ").strip()): show(g, t)
