"""Input-output cascade + Neo4j access.
Layer 1: how much of each imported good is lost.  
Layer 2: part is refilled by other suppliers (historical average).
Layer 3: the net shortage hits industries directly, then spreads along the MoSPI input-output links."""
import numpy as np
import config

def ym_add(ym, n):    # 201905 + (-11) -> 201806
    i = (ym // 100) * 12 + (ym % 100 - 1) + n
    return (i // 12) * 100 + i % 12 + 1

def spread(l0, C, alpha=config.SPREAD_STRENGTH, rounds=config.SPREAD_ROUNDS):
    """Domino step: loss_j = direct_j + alpha * sum_i C[i,j] * loss_i, repeated so effects travel several links; capped at 100%."""
    l = l0.copy()
    for _ in range(rounds): l = np.minimum(1, l0 + alpha * (C.T @ l))
    return l

def assess(sc, shares, conc, names, C, refill_override=None, alpha=config.SPREAD_STRENGTH):
    """shares {(hs,country): share}; conc {hs:{ind,dep,refill,name}}. Returns (direct rows, ranked industries, direct-loss vector)."""
    l0 = np.zeros(len(names)); rows = []
    for hs, v in conc.items():
        if sc.hs and hs not in sc.hs: continue
        lost = sum(shares.get((hs, c), 0) for c in sc.countries) * sc.severity
        if lost <= 0: continue
        lost = min(lost, 1); rf = v["refill"] if refill_override is None else refill_override
        net = lost * (1 - rf); L = net * v["dep"]
        l0[v["ind"]] = 1 - (1 - l0[v["ind"]]) * (1 - L)
        rows.append({"hs": hs, "name": v["name"], "lost_share": lost, "refill": rf, "net_loss": net, "dependence": v["dep"]})
    l = spread(l0, C, alpha)
    rank = [(int(i), names[i], float(l[i]), float(l0[i])) for i in np.argsort(-l) if l[i] > 5e-4]
    return rows, rank, l0

def why_chain(target, l0, C, names, conc, rows, hops=3):
    """Strongest chain that explains a hit: good -> first industry hurt -> ... -> target (product of link strengths, up to 3 links)."""
    best = (0.0, None)
    for o in np.where(l0 > 0)[0]:
        stack = [(int(o), [int(o)], 1.0)]
        while stack:
            n, p, w = stack.pop()
            if n == target:
                if l0[o] * w > best[0]: best = (l0[o] * w, p)
                continue
            if len(p) > hops: continue
            for j in np.where(C[n] > .02)[0]:
                if int(j) not in p: stack.append((int(j), p + [int(j)], w * C[n, j]))
    if best[1] is None: return []
    good = next((r["name"] for r in rows if conc[r["hs"]]["ind"] == best[1][0]), "imports")
    return [good[:40]] + [names[i][:40] for i in best[1]]

