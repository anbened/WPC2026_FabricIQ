# Setup: rifare la demo su Microsoft Fabric

Tempo stimato: circa un'ora. Alla fine avrai in Fabric un lakehouse con i dati di Fourth Coffee,
un'ontologia collegata ai dati e due agenti da confrontare.

## Prerequisiti

- Un workspace dove puoi creare gli item e leggere le sorgenti. Per i data agent serve una capacità
  Fabric a pagamento F2 o superiore, oppure Power BI Premium P1 o superiore con Fabric abilitato.
  [Prerequisiti del Fabric data agent](https://learn.microsoft.com/en-us/fabric/data-science/how-to-create-data-agent)
- Nel tenant devono essere abilitate la creazione di item Fabric e Ontology (preview) e la funzionalità Graph.
  Per i data agent verifica con l'amministratore anche le impostazioni di Copilot e Azure OpenAI,
  incluse quelle di elaborazione e archiviazione fuori area quando richieste per la regione della capacità.
  [Impostazioni del tenant per i data agent](https://learn.microsoft.com/en-us/fabric/data-science/data-agent-tenant-settings)
- I file di questo repository, scaricabili da GitHub con **Code › Download ZIP**.

## 1. Carica i dati

1. Crea un lakehouse dedicato alla demo, per esempio `FourthCoffeeLH`.
2. In **Files** crea la cartella `fourth_coffee` e caricaci tutti i CSV della cartella [`data/`](../data).
   Devi ottenere `Files/fourth_coffee/stores.csv`, `Files/fourth_coffee/farms.csv` e così via.
3. Importa nel workspace il notebook [`notebooks/load_tables.ipynb`](../notebooks/load_tables.ipynb),
   e collega il lakehouse della demo come predefinito. **Controlla il lakehouse selezionato prima di eseguire
   il notebook.** Il caricamento crea 11 tabelle Delta gestite e sovrascrive dati e schema delle eventuali
   tabelle omonime. Esegui il notebook e controlla i conteggi stampati confrontandoli con il [riepilogo dei CSV](../data/README.md).

Si può usare anche **Load to Tables** su ogni CSV, ma i campi data restano stringhe: il notebook è più sicuro.
Per avvicinarti allo scenario reale puoi caricare `machine_telemetry` in un **Eventhouse**: il binding
time series funziona sia da lakehouse sia da eventhouse.

I nomi delle colonne sono volutamente diversi tra le tabelle, come accade tra sistemi diversi:
il negozio è `StoreId` in `stores` (stile Azure SQL), `store_id` in `equipment` (stile Cosmos DB)
e `destination_id` in `shipments` (stile HorizonDB). L'ontologia li ricondurrà allo stesso concetto.

## 2. Importa l'ontologia

1. Crea un item **Ontology (preview)** vuoto, per esempio `FourthCoffee`. L'import funziona solo in un item vuoto.
2. **Home › Import ontology › Browse**, scegli [`ontology/FourthCoffee.ttl`](../ontology/FourthCoffee.ttl)
   e seleziona **Start import**.
3. Leggi il riepilogo **prima di premere Done**: non si può riaprire. Scarica il log.
   Atteso: 9 entity type, 51 proprietà, 8 relazioni. Se un tipo (integer, double, dateTime) risulta
   convertito in stringa, correggilo a mano nella proprietà.

Se il file `.ttl` dà problemi, prova [`ontology/FourthCoffee.rdf`](../ontology/FourthCoffee.rdf):
è la stessa ontologia in RDF/XML.

Lo standard RDF non trasporta chiavi, data binding e regole: si configurano nei passi seguenti.

## 3. Chiavi e data binding

Per ogni entity type: **Configure › Add binding**, scegli il lakehouse e la tabella, mappa le colonne sulle
proprietà importate e imposta la chiave.

| Entity type | Tabella | Chiave (proprietà ← colonna) | Proprietà con nome diverso dalla colonna |
|---|---|---|---|
| **Farm** | `farms` | `FarmId` ← `FarmId` | `FarmCountry` ← `Country`, `FarmRegion` ← `Region` |
| **Certification** | `certifications` | `CertificationId` ← `CertificationId` | stessi nomi |
| **GreenLot** | `green_lots` | `GreenLotId` ← `GreenLotId` | `GreenWeightKg` ← `WeightKg` |
| **RoastBatch** | `roast_batches` | `RoastBatchId` ← `RoastBatchId` | stessi nomi |
| **PackagingRun** | `packaging_runs` | `PackagingRunId` ← `PackagingRunId` | stessi nomi |
| **Shipment** | `shipments` | `ShipmentId` ← `shipment_id` | `ShipmentId` ← `shipment_id`, `ShipDate` ← `ship_date`, `DeliveryDate` ← `delivery_date`, `Carrier` ← `carrier`, `BagsShipped` ← `bags_shipped` |
| **Store** | `stores` | `StoreId` ← `StoreId` | stessi nomi |
| **Equipment** | `equipment` | `AssetId` ← `asset_id` | `AssetId` ← `asset_id`, `EquipmentModel` ← `model`, `InstallDate` ← `install_date` |
| **Complaint** | `complaints` | `ComplaintId` ← `ComplaintId` | stessi nomi |

## 4. Relazioni

Per ogni relazione indica la tabella sorgente e le due colonne che corrispondono alle chiavi delle entità
collegate.

| Relazione | Da → A | Tabella | Colonna sorgente | Colonna destinazione |
|---|---|---|---|---|
| **supplies** | Farm → GreenLot | `green_lot_farms` | `FarmId` | `GreenLotId` |
| **holdsCertification** | Farm → Certification | `certifications` | `FarmId` | `CertificationId` |
| **roastedInto** | GreenLot → RoastBatch | `roast_batches` | `GreenLotId` | `RoastBatchId` |
| **packedInto** | RoastBatch → PackagingRun | `packaging_runs` | `RoastBatchId` | `PackagingRunId` |
| **shippedWith** | PackagingRun → Shipment | `shipments` | `packaging_run_id` | `shipment_id` |
| **deliveredTo** | Shipment → Store | `shipments` | `shipment_id` | `destination_id` |
| **installedAt** | Equipment → Store | `equipment` | `asset_id` | `store_id` |
| **reportedAt** | Complaint → Store | `complaints` | `ComplaintId` | `StoreId` |

`supplies` è molti-a-molti: un lotto di caffè verde mescola più farm. La tabella `green_lot_farms`
contiene anche la quota di ciascuna farm (`SharePct`).

## 5. Telemetria delle macchine

Su **Equipment** aggiungi un binding **time series**: tabella `machine_telemetry`, chiave `asset_id`,
timestamp `timestamp`, proprietà `PumpPressureBar` ← `pump_pressure_bar` e `BoilerTempC` ← `boiler_temp_c`.

Facoltativo: crea una **regola operativa** (Activator) su `PumpPressureBar < 8.5`. Nei dati scatta solo
su una macchina di Torino (`EQ-S004-02`, il 21 ottobre tra le 10 e le 12), non ad Assago.

## 6. La regola: Fourth Hand Standard

Aggiungi una regola collegata a **Farm**, **GreenLot** e **Certification** con questo testo:

> Fourth Hand Standard: Fourth Coffee acquista caffè verde solo da produttori in regola il giorno dell'acquisto. Un GreenLot è conforme solo se OGNI Farm che lo rifornisce (relazione supplies), qualunque sia la sua quota, alla data PurchaseDate del lotto aveva una Certification con ValidFrom <= PurchaseDate <= ValidTo e con SuspendedFrom vuoto oppure successivo a PurchaseDate. Basta una sola Farm non in regola per rendere non conforme l'intero lotto. Una sospensione non rende non conformi i lotti acquistati prima della data di sospensione. Le certificazioni vengono sospese quando l'audit qualità non è superato (per esempio difetti di fermentazione del caffè verde, che danno un gusto acido in tazza). I lotti non conformi ancora in magazzino (WarehouseStatus = InStock) vanno messi in attesa e segnalati al team sourcing.

Lo stesso testo è già nelle descrizioni di Farm e GreenLot, quindi l'agente lo trova anche senza la regola.
Averla come regola esplicita però la rende visibile e governabile.

## 7. Verifica

Aggiorna il grafo e controlla sul canvas che la catena Farm → GreenLot → RoastBatch → PackagingRun →
Shipment → Store sia completa. Poi passa allo [script della demo](demo.md).

## Se qualcosa non funziona

- **Il grafo è vuoto o incompleto:** di solito manca una chiave o una colonna di relazione non corrisponde
  alla chiave dell'entità collegata. Ricontrolla le tabelle dei passi 3 e 4.
- **L'import ha saltato qualcosa:** leggi il log scaricato al passo 2. Le proprietà senza dominio e i
  costrutti OWL complessi vengono ignorati.
- **Le tabelle non compaiono nel binding:** devono essere tabelle Delta gestite, senza OneLake security
  e senza column mapping. Il notebook le crea così.
