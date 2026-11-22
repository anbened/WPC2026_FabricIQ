import sys
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from spec import ENTITIES, RELATIONSHIPS  # noqa: E402

D = Path(sys.argv[1])
t = {p.stem: pd.read_csv(p, dtype=str, keep_default_na=False) for p in D.glob("*.csv")}

# 1. Every bound column exists; keys unique; relationship ends resolve
key_col = {}
for e in ENTITIES:
    df = t[e["table"]]
    for (_l, _ty, col, _c, _s) in e["props"]:
        assert col in df.columns, (e["label"], col)
    for k in e["key"]:
        assert k in df.columns
    assert not df.duplicated(e["key"]).any(), f"duplicate keys in {e['table']}"
    key_col[e["label"]] = (e["table"], e["key"][0])
    ts = e.get("timeseries")
    if ts:
        tdf = t[ts["table"]]
        assert {ts["key"], ts["timestamp"]} <= set(tdf.columns)
        assert set(tdf[ts["key"]]) <= set(df[e["key"][0]])
for (label, src, tgt, table, sc, tc, *_r) in RELATIONSHIPS:
    df = t[table]
    stab, skey = key_col[src]
    ttab, tkey = key_col[tgt]
    assert set(df[sc]) <= set(t[stab][skey]), (label, "source")
    assert set(df[tc]) <= set(t[ttab][tkey]), (label, "target")
print("bindings OK")

# 2. Apply the Fourth Hand Standard
cert = t["certifications"]
def farm_ok(fid, day):
    for _, c in cert[cert.FarmId == fid].iterrows():
        vf, vt = date.fromisoformat(c.ValidFrom), date.fromisoformat(c.ValidTo)
        sus = date.fromisoformat(c.SuspendedFrom) if c.SuspendedFrom else None
        if vf <= day <= vt and (sus is None or sus > day):
            return True
    return False

lots = t["green_lots"].set_index("GreenLotId")
mix = t["green_lot_farms"]
bad = []
for lid, l in lots.iterrows():
    pdate = date.fromisoformat(l.PurchaseDate)
    off = [f for f in mix[mix.GreenLotId == lid].FarmId if not farm_ok(f, pdate)]
    if off:
        bad.append((lid, l.PurchaseDate, off, l.WarehouseStatus))
print("non-compliant lots:", bad)

# 3. Trace shipments to Assago and Bergamo back to the green lot
sh = t["shipments"].merge(t["packaging_runs"], left_on="packaging_run_id", right_on="PackagingRunId") \
    .merge(t["roast_batches"], on="RoastBatchId")
S1 = date(2026, 9, 7)
sh["week"] = sh.delivery_date.map(lambda x: 1 + (date.fromisoformat(x) - S1).days // 7)
for sid in ("S003", "S002", "S001"):
    print(sid, sh[sh.destination_id == sid].groupby("week").GreenLotId.first().to_dict())

# 4. Complaints per week (acid) per store
c = t["complaints"]
c["week"] = c.ComplaintDate.map(lambda x: 1 + (date.fromisoformat(x) - S1).days // 7)
acid = c[c.ComplaintCategory == "Gusto acido"].groupby(["StoreId", "week"]).size().unstack(fill_value=0)
print(acid)

# 5. Telemetry at Assago vs the Torino dip
tel = t["machine_telemetry"].astype({"pump_pressure_bar": float, "boiler_temp_c": float})
for a in ("EQ-S003-01", "EQ-S003-02", "EQ-S004-02"):
    x = tel[tel.asset_id == a]
    print(a, "pressure min/mean", x.pump_pressure_bar.min(), round(x.pump_pressure_bar.mean(), 2),
          "temp min", x.boiler_temp_c.min(), "below 8.5 bar:", int((x.pump_pressure_bar < 8.5).sum()))
