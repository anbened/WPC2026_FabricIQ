import sys
from datetime import date
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from spec import ENTITIES, RELATIONSHIPS  # noqa: E402

D = Path(sys.argv[1])
t = {p.stem: pd.read_csv(p, dtype=str, keep_default_na=False) for p in D.glob("*.csv")}


def expect(label, actual, expected):
    if actual != expected:
        sys.exit(f"{label}: atteso {expected}, trovato {actual}")


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
bad = {}
for lid, l in lots.iterrows():
    pdate = date.fromisoformat(l.PurchaseDate)
    off = [f for f in mix[mix.GreenLotId == lid].FarmId if not farm_ok(f, pdate)]
    if off:
        bad[lid] = (l.PurchaseDate, sorted(off), l.WarehouseStatus)
print("non-compliant lots:", bad)
expect("Lotti non conformi alla data di acquisto", bad, {
    "GL-2026-037": ("2026-10-05", ["F005"], "Roasted"),
    "GL-2026-039": ("2026-10-22", ["F005"], "InStock"),
})
expect("Acquisto del lotto conforme GL-2026-033", lots.at["GL-2026-033", "PurchaseDate"], "2026-08-20")
for lid, share in [("GL-2026-033", "30"), ("GL-2026-037", "35"), ("GL-2026-039", "60")]:
    shares = mix.loc[(mix.GreenLotId == lid) & (mix.FarmId == "F005"), "SharePct"]
    expect(f"Quota di F005 in {lid} (%)", shares.tolist(), [share])
expect("Sospensione di F005", cert.loc[cert.CertificationId == "CERT-F005-2025", "SuspendedFrom"].tolist(),
       ["2026-09-28"])

# 3. Trace shipments to Assago and Bergamo back to the green lot
sh = t["shipments"].merge(t["packaging_runs"], left_on="packaging_run_id", right_on="PackagingRunId") \
    .merge(t["roast_batches"], on="RoastBatchId")
S1 = date(2026, 9, 7)
sh["week"] = sh.delivery_date.map(lambda x: 1 + (date.fromisoformat(x) - S1).days // 7)
for sid, suffixes in {
    "S003": ["031", "031", "033", "033", "033", "037", "037", "037"],
    "S002": ["032", "032", "034", "034", "035", "036", "037", "037"],
}.items():
    by_week = sh[sh.destination_id == sid].groupby("week").GreenLotId.agg(set).to_dict()
    expected = {week: {f"GL-2026-{suffix}"} for week, suffix in enumerate(suffixes, start=1)}
    expect(f"Lotti consegnati per settimana a {sid}", by_week, expected)
    print(sid, by_week)
print("S001", sh[sh.destination_id == "S001"].groupby("week").GreenLotId.agg(set).to_dict())
assago_lot = sh[(sh.destination_id == "S003") & (sh.GreenLotId == "GL-2026-037")]
expect("Prima consegna di GL-2026-037 ad Assago", assago_lot.delivery_date.min(), "2026-10-13")
chain = assago_lot[["week", "RoastBatchId", "PackagingRunId"]].drop_duplicates()
expect("Tostature e confezionamenti di GL-2026-037 ad Assago", sorted(chain.itertuples(index=False, name=None)),
       [(6, "RB-1013", "PR-5013"), (7, "RB-1015", "PR-5015"), (8, "RB-1017", "PR-5017")])

# 4. Complaints per week (acid) per store
c = t["complaints"]
c["week"] = c.ComplaintDate.map(lambda x: 1 + (date.fromisoformat(x) - S1).days // 7)
acid = c[c.ComplaintCategory == "Gusto acido"].groupby(["StoreId", "week"]).size().unstack(fill_value=0)
print(acid)
for sid, counts in {
    "S003": [3, 2, 4, 3, 3, 9, 14, 17],
    "S002": [1, 0, 1, 1, 1, 1, 5, 7],
}.items():
    observed = acid.reindex(index=[sid], columns=range(1, 9), fill_value=0).iloc[0].tolist()
    expect(f"Reclami settimanali per gusto acido a {sid}", observed, counts)

# 5. Telemetry at Assago vs the Torino dip
tel = t["machine_telemetry"].astype({"pump_pressure_bar": float, "boiler_temp_c": float})
equipment = t["equipment"].set_index("asset_id")
assago_assets = {"EQ-S003-01", "EQ-S003-02"}
expect("Macchine installate ad Assago", set(equipment[equipment.store_id == "S003"].index), assago_assets)
expect("Negozio della macchina EQ-S004-02", equipment.at["EQ-S004-02", "store_id"], "S004")
hours = pd.date_range(start=S1, periods=56 * 24, freq="h")
service_hours = hours[(hours.hour >= 6) & (hours.hour <= 21)].strftime("%Y-%m-%d %H:%M:%S")
for a in ("EQ-S003-01", "EQ-S003-02", "EQ-S004-02"):
    x = tel[tel.asset_id == a]
    if a in assago_assets:
        if sorted(x.timestamp) != list(service_hours):
            sys.exit(f"Telemetria di {a}: attesa una lettura ogni ora di servizio per tutte le otto settimane")
        if not x.pump_pressure_bar.between(8.6, 9.4).all():
            sys.exit(f"Pressione di {a} fuori dall'intervallo atteso 8,6-9,4 bar")
        if not x.boiler_temp_c.between(91, 96, inclusive="right").all():
            sys.exit(f"Temperatura di {a} fuori dall'intervallo atteso (91, 96] °C")
    print(a, "pressure min/mean", x.pump_pressure_bar.min(), round(x.pump_pressure_bar.mean(), 2),
          "temp min", x.boiler_temp_c.min(), "below 8.5 bar:", int((x.pump_pressure_bar < 8.5).sum()))

dips = tel.loc[tel.pump_pressure_bar < 8.5, ["asset_id", "timestamp"]]
expect("Cali di pressione sotto 8,5 bar", sorted(dips.itertuples(index=False, name=None)),
       [("EQ-S004-02", f"2026-10-21 {hour}:00:00") for hour in (10, 11, 12)])
print("Verifica della demo superata.")
