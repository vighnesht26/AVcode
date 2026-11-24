"""Read the raw files"""
import numpy as np, pandas as pd
import config

def read_trade():
    """Monthly imports, summed per (year, month, HS code, country).Also adds ym = year*100+month (201905)."""
    df = pd.read_csv(config.TRADE_CSV)
    g = df.groupby(["Year", "Month", "HS_Code", "Country"], as_index=False).Trade_Value_USD.sum()
    g["ym"] = g.Year * 100 + g.Month
    names = df.drop_duplicates("HS_Code").set_index("HS_Code").Commodity.str.slice(0, 80).to_dict()
    return g, names

def read_io():
    """MoSPI matrix A (A[i,j] = input from industry i per unit output of j) -> industry names and
    C[i,j] = industry i's share of j's total input"""
    X = pd.read_excel(config.IO_XLSX, sheet_name=config.IO_SHEET, header=None)
    names = [str(n) for n in X.iloc[1:, 0]]
    A = X.iloc[1:, 1:].astype(float).values
    return names, A / np.maximum(A.sum(0, keepdims=True), 1e-9)

def concordance_with_index(names):
    """Attach the position of each industry (by name prefix) to the CONCORDANCE table."""
    out = {}
    for hs, (key, dep) in config.CONCORDANCE.items():
        hit = [i for i, n in enumerate(names) if n.startswith(key)]
        if not hit: raise ValueError(f"No MoSPI industry starts with '{key}' (HS {hs})")
        out[hs] = {"ind": hit[0], "dep": dep}
    return out

def event_study(trade):
    """DESCRIPTIVE statistics, find past months where a big supplier (>=5% share) fell below half its normal level,
    and measure what fraction of the lost amount other suppliers made up. Returns {hs: average refill}, plus a global average."""
    refill = {}
    for hs, d in trade.groupby("HS_Code"):
        g = d.pivot_table(index="ym", columns="Country", values="Trade_Value_USD", aggfunc="sum").fillna(0)
        g = g.reindex(sorted(g.index))
        tot = g.sum(1)
        ys = []
        for c in g.columns:
            s, last = g[c], -99
            for t in range(12, len(g) - 3):
                base = s.iloc[t-12:t].mean(); share = base / max(tot.iloc[t-12:t].mean(), 1)
                if share < .05 or t - last < 6 or s.iloc[t:t+3].mean() >= .5 * base: continue
                oth = g.drop(columns=c).sum(1); lost = base - s.iloc[t:t+3].mean()
                gain = oth.iloc[t:t+3].mean() - oth.iloc[t-12:t].mean()
                ys.append(float(np.clip(gain / lost, 0, 1))); last = t
        refill[hs] = ys
    allv = [v for ys in refill.values() for v in ys]
    glob = float(np.mean(allv)) if allv else config.DEFAULT_REFILL
    return {hs: (float(np.mean(ys)) if len(ys) >= 5 else glob) for hs, ys in refill.items()}, glob, len(allv)
