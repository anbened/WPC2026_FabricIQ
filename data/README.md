# Dati

Undici tabelle di dati **fittizi** che raccontano la storia della demo, dal 7 settembre al 1° novembre 2026
(settimane S1-S8). Formato CSV con intestazione, separatore virgola, codifica UTF-8, date in formato ISO.

| File | Contenuto | Chiave | Righe |
|---|---|---|---|
| `stores.csv` | Anagrafica negozi (stile Azure SQL) | `StoreId` | 6 |
| `farms.csv` | Produttori di caffè verde | `FarmId` | 6 |
| `certifications.csv` | Certificazioni e audit delle farm, con date di validità e sospensione | `CertificationId` | 7 |
| `green_lots.csv` | Lotti di caffè verde acquistati | `GreenLotId` | 9 |
| `green_lot_farms.csv` | Composizione dei lotti: quali farm e con che quota | `GreenLotId + FarmId` | 20 |
| `roast_batches.csv` | Tostature | `RoastBatchId` | 18 |
| `packaging_runs.csv` | Cicli di confezionamento | `PackagingRunId` | 18 |
| `shipments.csv` | Spedizioni ai negozi (stile HorizonDB: destination_id = StoreId) | `shipment_id` | 96 |
| `equipment.csv` | Macchine espresso (stile Cosmos DB: store_id = StoreId) | `asset_id` | 12 |
| `machine_telemetry.csv` | Telemetria oraria delle macchine, 6:00-21:00 | `asset_id + timestamp` | 10.752 |
| `complaints.csv` | Reclami dei clienti | `ComplaintId` | 239 |

I nomi delle colonne seguono convenzioni diverse apposta, come accade tra sistemi diversi: lo stesso negozio è
`StoreId`, `store_id` o `destination_id` a seconda della tabella.

Per caricarli in Fabric usa il notebook [`load_tables.ipynb`](../notebooks/load_tables.ipynb) come descritto nel
[setup](../docs/setup.md). Per la storia contenuta nei dati vedi la [demo](../docs/demo.md); per rigenerarli,
[`tools/gen_data.py`](../tools/gen_data.py).
