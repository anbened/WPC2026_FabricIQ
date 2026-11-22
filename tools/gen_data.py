"""Demo dataset for the Fourth Coffee story.

Story baked into the data:
- Weeks S1..S8 start on Monday 2026-09-07 (S6 starts 2026-10-12).
- Farm F005 has its certification suspended from 2026-09-28 (failed quality audit:
  fermentation defects).
- GreenLot GL-2026-033 contains F005 but was bought on 2026-08-20 -> compliant.
- GreenLot GL-2026-037 contains F005 (35%) and was bought on 2026-10-05 -> NOT compliant.
  It reaches Assago (S003) from S6 and Bergamo (S002) from S7.
- GreenLot GL-2026-039 contains F005, bought 2026-10-22, still InStock -> to put on hold.
- Assago machines have normal pump pressure and boiler temperature throughout.
- A Torino machine has a short pressure dip (operational-rule example, unrelated).
- Assago "Gusto acido" complaints per week: 3,2,4,3,3,9,14,17 (deck slide 25).
"""
import csv
import random
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
rnd = random.Random(42)

S1 = date(2026, 9, 7)
WEEKS = [S1 + timedelta(days=7 * i) for i in range(8)]  # Monday of S1..S8


def write(name, header, rows):
    with open(OUT / f"{name}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    return rows


def d(x):
    return x.isoformat() if x else ""


# ---------------- Stores (Azure SQL style: StoreId) ----------------
stores = [
    ("S001", "Fourth Coffee Milano Duomo", "Milano", "Bar", date(2019, 3, 1)),
    ("S002", "Fourth Coffee Bergamo Centro", "Bergamo", "Bar", date(2020, 6, 15)),
    ("S003", "Fourth Coffee Assago", "Assago", "Drive-through", date(2021, 9, 1)),
    ("S004", "Fourth Coffee Torino Porta Nuova", "Torino", "Bar", date(2020, 1, 20)),
    ("S005", "Fourth Coffee Bologna Stazione", "Bologna", "Kiosk", date(2022, 4, 4)),
    ("S006", "Fourth Coffee Monza", "Monza", "Bar", date(2023, 5, 10)),
]
write("stores", ["StoreId", "StoreName", "City", "StoreFormat", "OpenedOn"],
      [(s[0], s[1], s[2], s[3], d(s[4])) for s in stores])
STORE_IDS = [s[0] for s in stores]

# ---------------- Farms & certifications ----------------
farms = [
    ("F001", "Cooperativa Monte Azul", "Brasile", "Sul de Minas", 1150),
    ("F002", "Finca Altamira", "Colombia", "Huila", 1700),
    ("F003", "Sidama Highlands Union", "Etiopia", "Sidama", 1950),
    ("F004", "Finca Los Cedros", "Guatemala", "Huehuetenango", 1600),
    ("F005", "Hacienda San Rafael", "Honduras", "Santa Barbara", 1450),
    ("F006", "Nyeri Hills Estate", "Kenya", "Nyeri", 1800),
]
write("farms", ["FarmId", "FarmName", "Country", "Region", "AltitudeM"], farms)

certs = []
for i, f in enumerate(farms, 1):
    fid = f[0]
    if fid == "F005":
        certs.append((f"CERT-{fid}-2025", fid, "Fourth Hand Standard - Quality & Ethics Audit", "Suspended",
                      d(date(2025, 7, 1)), d(date(2027, 6, 30)), d(date(2026, 9, 28)),
                      "Audit qualità non superato: difetti di fermentazione (sour beans oltre soglia)",
                      d(date(2026, 9, 25)), "Failed"))
    else:
        certs.append((f"CERT-{fid}-2025", fid, "Fourth Hand Standard - Quality & Ethics Audit", "Active",
                      d(date(2025, 7, 1)), d(date(2027, 6, 30)), "", "",
                      d(date(2026, 6, 1) + timedelta(days=9 * i)), "Passed"))
# An expired older certificate, to make the temporal logic non-trivial
certs.append(("CERT-F004-2023", "F004", "Fourth Hand Standard - Quality & Ethics Audit", "Expired",
              d(date(2023, 7, 1)), d(date(2025, 6, 30)), "", "", d(date(2024, 6, 12)), "Passed"))
write("certifications", ["CertificationId", "FarmId", "CertScheme", "CertStatus", "ValidFrom", "ValidTo",
                         "SuspendedFrom", "SuspensionReason", "LastAuditDate", "LastAuditOutcome"], certs)

# ---------------- Green lots & mix ----------------
# id, purchase, processor, kg, cupping, moisture, status, [(farm, share)]
lots = [
    ("GL-2026-031", date(2026, 7, 15), "Beneficio Sul de Minas", 6000, 85.0, 10.9, "Roasted", [("F001", 60), ("F003", 40)]),
    ("GL-2026-032", date(2026, 7, 28), "Beneficio Huila Norte", 6000, 84.5, 11.0, "Roasted", [("F002", 50), ("F004", 50)]),
    ("GL-2026-033", date(2026, 8, 20), "Beneficio Copán", 6000, 84.0, 11.2, "Roasted", [("F005", 30), ("F001", 40), ("F006", 30)]),
    ("GL-2026-034", date(2026, 9, 2), "Sidama Washing Station 4", 6000, 86.0, 10.8, "Roasted", [("F003", 50), ("F006", 50)]),
    ("GL-2026-035", date(2026, 9, 15), "Beneficio Huila Norte", 6000, 85.5, 10.9, "Roasted", [("F002", 60), ("F004", 40)]),
    ("GL-2026-036", date(2026, 9, 30), "Sidama Washing Station 4", 6000, 85.5, 11.0, "Roasted", [("F003", 50), ("F006", 50)]),
    ("GL-2026-037", date(2026, 10, 5), "Beneficio Copán", 6000, 80.5, 12.6, "Roasted", [("F002", 40), ("F005", 35), ("F001", 25)]),
    ("GL-2026-038", date(2026, 10, 14), "Beneficio Huehuetenango", 6000, 85.0, 11.0, "Roasted", [("F004", 50), ("F006", 50)]),
    ("GL-2026-039", date(2026, 10, 22), "Beneficio Copán", 6000, 81.0, 12.4, "InStock", [("F005", 60), ("F003", 40)]),
]
write("green_lots", ["GreenLotId", "PurchaseDate", "Processor", "WeightKg", "CuppingScore", "MoisturePct", "WarehouseStatus"],
      [(l[0], d(l[1]), l[2], l[3], l[4], l[5], l[6]) for l in lots])
write("green_lot_farms", ["GreenLotId", "FarmId", "SharePct"],
      [(l[0], fid, sh) for l in lots for fid, sh in l[7]])
LOT = {l[0]: l for l in lots}

# ---------------- Supply plan: which green lot each store gets each week ----------------
plan = {
    1: {"S001": "031", "S003": "031", "S005": "031", "S002": "032", "S004": "032", "S006": "032"},
    2: {"S001": "031", "S003": "031", "S005": "031", "S002": "032", "S004": "032", "S006": "032"},
    3: {"S001": "033", "S003": "033", "S002": "034", "S004": "034", "S005": "034", "S006": "034"},
    4: {"S003": "033", "S005": "033", "S001": "034", "S002": "034", "S004": "035", "S006": "035"},
    5: {"S003": "033", "S006": "033", "S001": "035", "S002": "035", "S004": "035", "S005": "035"},
    6: {"S003": "037", "S001": "036", "S002": "036", "S004": "036", "S005": "036", "S006": "036"},
    7: {"S003": "037", "S002": "037", "S001": "038", "S004": "038", "S005": "036", "S006": "036"},
    8: {"S003": "037", "S002": "037", "S001": "038", "S004": "038", "S005": "038", "S006": "038"},
}

roasts, packs, ships = [], [], []
run_for = {}  # (week, lot) -> packaging run id
rb_n, pr_n, sh_n = 1001, 5001, 1
for wk in range(1, 9):
    for lot_suffix in sorted(set(plan[wk].values())):
        lot_id = f"GL-2026-{lot_suffix}"
        roast_day = WEEKS[wk - 1] - timedelta(days=4)  # Thursday of previous week
        assert roast_day > LOT[lot_id][1], (lot_id, roast_day)
        rb = f"RB-{rb_n}"; rb_n += 1
        roasts.append((rb, lot_id, d(roast_day), "Torrefazione Lodi", "Espresso Medium", 1200))
        pr = f"PR-{pr_n}"; pr_n += 1
        pack_day = roast_day + timedelta(days=1)
        packs.append((pr, rb, d(pack_day), f"Linea {1 + (pr_n % 2)}", 1180, d(pack_day + timedelta(days=270))))
        run_for[(wk, lot_suffix)] = pr
    for sid in STORE_IDS:
        pr = run_for[(wk, plan[wk][sid])]
        for offset in (0, 3):  # Monday and Thursday
            ship_day = WEEKS[wk - 1] + timedelta(days=offset)
            ships.append((f"SH-{sh_n:05d}", pr, sid, d(ship_day), d(ship_day + timedelta(days=1)),
                          rnd.choice(["BRT", "GLS", "SDA"]), rnd.randint(36, 60)))
            sh_n += 1

write("roast_batches", ["RoastBatchId", "GreenLotId", "RoastDate", "RoastPlant", "RoastProfile", "RoastWeightKg"], roasts)
write("packaging_runs", ["PackagingRunId", "RoastBatchId", "PackagingDate", "PackagingLine", "BagsProduced", "BestBefore"], packs)
# HorizonDB-style naming on purpose: destination_id is the StoreId
write("shipments", ["shipment_id", "packaging_run_id", "destination_id", "ship_date", "delivery_date", "carrier", "bags_shipped"], ships)

# ---------------- Equipment (Cosmos DB style: store_id) & telemetry ----------------
equipment = []
for sid in STORE_IDS:
    for k in (1, 2):
        equipment.append((f"EQ-{sid}-0{k}", sid, rnd.choice(["Aurelia Wave T3", "Leva X 2GR", "Linea PB 2GR"]),
                          d(date(2023, 1, 10) + timedelta(days=rnd.randint(0, 600)))))
write("equipment", ["asset_id", "store_id", "model", "install_date"], equipment)

tele = []
start = datetime.combine(WEEKS[0], datetime.min.time())
for day in range(56):
    for hour in range(6, 22):
        ts = start + timedelta(days=day, hours=hour)
        for eq in equipment:
            p = rnd.gauss(9.0, 0.12)
            t = rnd.gauss(93.0, 0.6)
            if eq[0] == "EQ-S004-02" and ts.date() == date(2026, 10, 21) and 10 <= hour <= 12:
                p = rnd.gauss(7.3, 0.15)  # Torino: short pump failure, unrelated to the story
            tele.append((eq[0], ts.strftime("%Y-%m-%d %H:%M:%S"), round(p, 2), round(t, 1)))
write("machine_telemetry", ["asset_id", "timestamp", "pump_pressure_bar", "boiler_temp_c"], tele)

# ---------------- Complaints ----------------
acid = {
    "S003": [3, 2, 4, 3, 3, 9, 14, 17],
    "S002": [1, 0, 1, 1, 1, 1, 5, 7],
}
acid_texts = ["Espresso acido, quasi aceto", "Il caffè oggi sa di acido", "Sapore acido e strano",
              "Caffè con un retrogusto fermentato", "Espresso aspro, non il solito", "Gusto acido, l'ho lasciato"]
other = {
    "Gusto amaro": ["Caffè troppo amaro", "Espresso bruciato"],
    "Temperatura": ["Caffè tiepido", "Cappuccino freddo"],
    "Servizio lento": ["Attesa lunga in coda", "Servizio lento al drive"],
    "Errore ordine": ["Mi hanno dato un americano", "Ordine sbagliato in app"],
}
complaints, cid = [], 1
for sid in STORE_IDS:
    for wk in range(8):
        n_acid = acid.get(sid, [rnd.randint(0, 2) for _ in range(8)])[wk]
        n_other = rnd.randint(1, 4)
        rows = [("Gusto acido", rnd.choice(acid_texts)) for _ in range(n_acid)]
        for _ in range(n_other):
            cat = rnd.choice(list(other))
            rows.append((cat, rnd.choice(other[cat])))
        for cat, txt in rows:
            day = WEEKS[wk] + timedelta(days=rnd.randint(1 if cat == "Gusto acido" else 0, 6))
            complaints.append((f"CMP-{cid:05d}", sid, d(day), cat, txt, rnd.choice(["App", "Cassa", "Web"])))
            cid += 1
complaints.sort(key=lambda r: (r[2], r[0]))
write("complaints", ["ComplaintId", "StoreId", "ComplaintDate", "ComplaintCategory", "ComplaintText", "Channel"], complaints)

print({p.name: sum(1 for _ in open(p)) - 1 for p in sorted(OUT.glob("*.csv"))})
