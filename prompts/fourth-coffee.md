# Prompt: l'esempio di Fourth Coffee

Il [modello di prompt](template.md) compilato per il business della demo. Mostra quanto contesto serve:
le istruzioni sul formato sono poche righe, il resto è conoscenza del business.

Il risultato non sarà identico al file in [`ontology/`](../ontology), che è stato costruito e verificato con gli
script di [`tools/`](../tools). Prima di generare, l'AI dovrebbe farti domande come «una spedizione può
contenere più confezionamenti?» o «la certificazione è un'entità a sé o un attributo della farm?».
Sono le stesse decisioni descritte in [Le scelte di modellazione](../docs/design.md).

## Il prompt

```
Sei un ontology engineer. Devo costruire un'ontologia per Microsoft Fabric IQ
che descriva Fourth Coffee, una catena di caffetterie, dalla piantagione alla tazzina.

1. IL BUSINESS
Fourth Coffee ha sei negozi tra Milano, Assago, Monza, Bergamo, Torino e Bologna
(bar, drive-through e kiosk). Compriamo caffè verde da farm in Brasile, Colombia,
Etiopia, Guatemala, Honduras e Kenya, tramite processor locali. Ogni lotto di caffè
verde mescola chicchi di più farm, con quote diverse. Lo tostiamo nella nostra
torrefazione di Lodi, lo confezioniamo in buste da 1 kg e lo spediamo ai negozi due
volte a settimana. Ogni negozio ha due macchine espresso che inviano telemetria
(pressione della pompa, temperatura della caldaia). I clienti lasciano reclami da
app, cassa e web. Chiamiamo questa filiera "le quattro mani": farmer, processor,
roaster, cliente.

2. IL GLOSSARIO
- "Lotto" ha tre significati: per il sourcing è il lotto di caffè verde acquistato,
  per la torrefazione è una singola tostatura, per la logistica è il ciclo di
  confezionamento stampato sulla busta.
- "Negozio", "punto vendita", "store" e "bar" sono la stessa cosa.
- "Farm", "produttore" e "finca" sono la stessa cosa.
- "In regola" e "conforme" hanno il significato definito nelle regole.

3. LE SORGENTI
- Anagrafica negozi (Azure SQL): stores(StoreId, StoreName, City, StoreFormat, OpenedOn)
- Registro dispositivi (Cosmos DB): equipment(asset_id, store_id, model, install_date)
- Telemetria (Eventhouse): machine_telemetry(asset_id, timestamp, pump_pressure_bar, boiler_temp_c)
- Spedizioni (HorizonDB): shipments(shipment_id, packaging_run_id, destination_id,
  ship_date, delivery_date, carrier, bags_shipped)
- Sourcing: farms(FarmId, FarmName, Country, Region, AltitudeM),
  certifications(CertificationId, FarmId, CertScheme, CertStatus, ValidFrom, ValidTo,
  SuspendedFrom, SuspensionReason, LastAuditDate, LastAuditOutcome),
  green_lots(GreenLotId, PurchaseDate, Processor, WeightKg, CuppingScore, MoisturePct,
  WarehouseStatus), green_lot_farms(GreenLotId, FarmId, SharePct)
- Produzione: roast_batches(RoastBatchId, GreenLotId, RoastDate, RoastPlant,
  RoastProfile, RoastWeightKg), packaging_runs(PackagingRunId, RoastBatchId,
  PackagingDate, PackagingLine, BagsProduced, BestBefore)
- Clienti: complaints(ComplaintId, StoreId, ComplaintDate, ComplaintCategory,
  ComplaintText, Channel)
Attenzione: StoreId, store_id e destination_id sono lo stesso codice negozio.

4. LE REGOLE
- Fourth Hand Standard: compriamo caffè verde solo da farm in regola il giorno
  dell'acquisto. Un lotto di caffè verde è conforme solo se ogni farm che lo
  rifornisce aveva, alla data di acquisto, una certificazione valida e non sospesa.
  Basta una sola farm non in regola. Una sospensione non tocca i lotti acquistati
  prima. Le certificazioni vengono sospese quando l'audit qualità non è superato,
  per esempio per difetti di fermentazione, che in tazza danno un gusto acido.
  I lotti non conformi ancora in magazzino vanno messi in attesa.
- Macchine: pressione normale 8,5-9,5 bar, caldaia 90-96 °C. Sotto queste soglie
  l'espresso è sottoestratto e risulta acido.

PRIMA DI SCRIVERE IL FILE
- Fammi domande dove un termine ha più significati o dove due sorgenti chiamano in
  modo diverso la stessa cosa. Non scegliere tu.
- Proponimi l'elenco di entità, relazioni e proprietà principali e aspetta la mia
  conferma.

POI GENERA UN FILE TURTLE (.ttl) CON QUESTI VINCOLI
- Namespace: https://fourthcoffee.example/ontology/
- owl:Class per ogni entità; owl:DatatypeProperty sempre con rdfs:domain e un
  rdfs:range xsd (string, integer, double, dateTime, boolean); owl:ObjectProperty
  con dominio e codominio.
- Nomi in inglese, PascalCase per entità e proprietà: 1-26 caratteri, solo lettere,
  numeri, trattino e underscore, senza spazi.
- Un rdfs:comment in italiano per ogni concetto, che spieghi cosa significa per il
  business, con soglie e regole: è quello che leggerà l'agente.
- skos:altLabel in italiano per i sinonimi che le persone usano davvero.
- Niente restrizioni OWL complesse né proprietà transitive o simmetriche.

INFINE ELENCA A PARTE
la chiave di ogni entità, la colonna sorgente di ogni proprietà e il testo di ogni
regola: chiavi, binding e regole si configurano in Fabric dopo l'import.
```
