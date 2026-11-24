"""Checks the parser, the cascade and the screen's data WITHOUT Neo4j.   python test_offline.py"""
import json, service
from offline_graph import OfflineGraph
from nlp_parser import parse
g = OfflineGraph(); o = service.options(g); print("window", o["window"], "| countries", len(o["countries"]), "| goods", len(o["goods"]), "| coords", o["has_coords"])
for t in ["If Russia stops oil exports", "If Iran in war has stopped exports", "china cuts electronics by 40%", "rusia bans fertilizer"]:
    sc = parse(t, g.countries()); print(">", t, "->", sc.countries[:3], sc.hs, sc.severity)
for c, h in [("Russian Federation", "2709"), ("__GULF__", "all")]:
    r = service.scenario(g, c, h, 1.0); print(f"\n{c} / {h}: top", [(x["industry"][:26], round(x["loss"], 3)) for x in r["ranking"][:3]])
    print("  why:", r["ranking"][0]["why"], "| arcs for", [s["name"] for s in r["map"]["suppliers"] if s["hit"]][:4]); json.dumps(r)
