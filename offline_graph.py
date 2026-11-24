"""Same interface as Graph, but reads your files directly"""
import config, data_files as d
from io_model import ym_add

class OfflineGraph:
    def __init__(self):
        self.t, cn = d.read_trade(); 
        self.names, self.C = d.read_io(); 
        self.conc = d.concordance_with_index(self.names)
        ref, glob, _ = d.event_study(self.t)
        for h in self.conc: self.conc[h].update(name=cn[h], refill=ref.get(h, glob))
    def countries(self): return list(self.t.Country.unique())
    def coords(self): return {c: v for c, v in config.COORDS.items() if c in set(self.t.Country)}
    def window(self, as_of_year=None):
        b = int(self.t.ym.max()); end = b if as_of_year is None else min(b, as_of_year * 100 + 12); return ym_add(end, -11), end
    def _w(self, a, b): return self.t[(self.t.ym >= a) & (self.t.ym <= b)]
    def shares(self, a, b):
        g = self._w(a, b).groupby(["HS_Code", "Country"]).Trade_Value_USD.sum().reset_index(); g["s"] = g.Trade_Value_USD / g.groupby("HS_Code").Trade_Value_USD.transform("sum")
        return {(r.HS_Code, r.Country): r.s for r in g.itertuples()}
    def totals(self, a, b): return self._w(a, b).groupby("Country").Trade_Value_USD.sum().to_dict()
    def structure(self): return self.names, self.C, self.conc
