# Single source of truth for the Fourth Coffee demo ontology.
# Used to generate the .ttl / .rdf files, the binding tables in the README,
# and to cross-check that every bound column exists in the generated data.

BASE = "https://fourthcoffee.example/ontology/"

ONTOLOGY_LABEL = "FourthCoffee"

FOURTH_HAND_STANDARD = (
    "Fourth Hand Standard: Fourth Coffee acquista caffè verde solo da produttori in regola "
    "il giorno dell'acquisto. Un GreenLot è conforme solo se OGNI Farm che lo rifornisce "
    "(relazione supplies), qualunque sia la sua quota, alla data PurchaseDate del lotto aveva una "
    "Certification con ValidFrom <= PurchaseDate <= ValidTo e con SuspendedFrom vuoto oppure "
    "successivo a PurchaseDate. Basta una sola Farm non in regola per rendere non conforme "
    "l'intero lotto. Una sospensione non rende non conformi i lotti acquistati prima della data "
    "di sospensione. Le certificazioni vengono sospese quando l'audit qualità non è superato "
    "(per esempio difetti di fermentazione del caffè verde, che danno un gusto acido in tazza). "
    "I lotti non conformi ancora in magazzino (WarehouseStatus = InStock) vanno messi in attesa "
    "e segnalati al team sourcing."
)

ONTOLOGY_COMMENT = (
    "Ontologia di Fourth Coffee: la catena che porta il caffè dalla farm alla tazzina "
    "(Farm -> GreenLot -> RoastBatch -> PackagingRun -> Shipment -> Store), le macchine "
    "installate nei negozi e i reclami dei clienti. " + FOURTH_HAND_STANDARD
)

# Property tuple: (label, xsd type, source column, comment, synonyms)
# Entity: label, table, key column(s), comment, synonyms, properties, timeseries
ENTITIES = [
    dict(
        label="Farm",
        table="farms",
        key=["FarmId"],
        comment=(
            "Il produttore (farmer) che coltiva il caffè: la prima delle quattro mani. "
            "Un GreenLot può contenere caffè di più Farm. Per sapere se una Farm era in regola "
            "a una certa data si guardano le sue Certification (relazione holdsCertification). "
            + FOURTH_HAND_STANDARD
        ),
        synonyms=["produttore", "farmer", "fattoria", "piantagione", "finca", "coltivatore"],
        props=[
            ("FarmId", "string", "FarmId", "Codice univoco del produttore.", ["codice farm", "codice produttore"]),
            ("FarmName", "string", "FarmName", "Nome del produttore.", ["nome farm", "nome produttore"]),
            ("FarmCountry", "string", "Country", "Paese di origine del caffè.", ["paese di origine", "origine"]),
            ("FarmRegion", "string", "Region", "Regione di coltivazione.", ["regione di origine"]),
            ("AltitudeM", "integer", "AltitudeM", "Altitudine della piantagione in metri.", ["altitudine"]),
        ],
    ),
    dict(
        label="Certification",
        table="certifications",
        key=["CertificationId"],
        comment=(
            "Certificazione e audit di una Farm secondo la Fourth Hand Standard. Una Farm è in regola "
            "alla data D se ha una Certification con ValidFrom <= D <= ValidTo e SuspendedFrom vuoto "
            "oppure successivo a D. CertStatus è lo stato ATTUALE, non lo stato a una data passata: "
            "per verificare la conformità a una data usare sempre ValidFrom, ValidTo e SuspendedFrom."
        ),
        synonyms=["certificazione", "audit", "certificato", "stato di conformità"],
        props=[
            ("CertificationId", "string", "CertificationId", "Codice univoco della certificazione.", []),
            ("CertScheme", "string", "CertScheme", "Schema di certificazione e audit applicato.", ["schema"]),
            ("CertStatus", "string", "CertStatus", "Stato attuale: Active, Suspended o Expired.", ["stato certificazione"]),
            ("ValidFrom", "dateTime", "ValidFrom", "Inizio validità della certificazione.", ["valida dal"]),
            ("ValidTo", "dateTime", "ValidTo", "Fine validità della certificazione.", ["valida fino al", "scadenza"]),
            ("SuspendedFrom", "dateTime", "SuspendedFrom", "Data da cui la certificazione è sospesa. Vuota se mai sospesa.", ["sospesa dal", "data sospensione"]),
            ("SuspensionReason", "string", "SuspensionReason", "Motivo della sospensione.", ["motivo sospensione"]),
            ("LastAuditDate", "dateTime", "LastAuditDate", "Data dell'ultimo audit qualità.", ["data ultimo audit"]),
            ("LastAuditOutcome", "string", "LastAuditOutcome", "Esito dell'ultimo audit: Passed o Failed.", ["esito audit"]),
        ],
    ),
    dict(
        label="GreenLot",
        table="green_lots",
        key=["GreenLotId"],
        comment=(
            "Lotto di caffè verde (non tostato) acquistato da Fourth Coffee: è il «lotto» nel linguaggio "
            "del sourcing. Mescola chicchi di una o più Farm (relazione supplies, con quota percentuale "
            "nella tabella green_lot_farms). Non confonderlo con RoastBatch (lotto di tostatura) né con "
            "PackagingRun (lotto di confezionamento). Quando qualcuno chiede «da quale lotto viene il "
            "caffè» riferendosi all'origine, intende il GreenLot. " + FOURTH_HAND_STANDARD
        ),
        synonyms=["green lot", "lotto verde", "lotto di caffè verde", "lotto di acquisto", "partita di caffè verde"],
        props=[
            ("GreenLotId", "string", "GreenLotId", "Codice univoco del lotto di caffè verde.", ["codice lotto verde"]),
            ("PurchaseDate", "dateTime", "PurchaseDate", "Data di acquisto del lotto: è la data rispetto a cui si verifica la Fourth Hand Standard.", ["data di acquisto", "data acquisto"]),
            ("Processor", "string", "Processor", "Il processor (seconda mano) che ha lavorato i chicchi.", ["lavoratore", "beneficio", "processor"]),
            ("GreenWeightKg", "double", "WeightKg", "Peso del lotto in kg.", ["peso lotto"]),
            ("CuppingScore", "double", "CuppingScore", "Punteggio qualitativo all'assaggio in ingresso (scala SCA, 0-100).", ["punteggio cupping", "punteggio qualità"]),
            ("MoisturePct", "double", "MoisturePct", "Umidità del caffè verde in percentuale.", ["umidità"]),
            ("WarehouseStatus", "string", "WarehouseStatus", "Stato in magazzino: InStock (non ancora tostato), Roasted (già tostato) o OnHold (in attesa).", ["stato magazzino"]),
        ],
    ),
    dict(
        label="RoastBatch",
        table="roast_batches",
        key=["RoastBatchId"],
        comment=(
            "Una singola tostatura in impianto (il roaster, terza mano): è il «lotto» nel linguaggio "
            "della torrefazione. Ogni RoastBatch usa caffè di un solo GreenLot."
        ),
        synonyms=["roast batch", "tostatura", "lotto di tostatura", "cotta"],
        props=[
            ("RoastBatchId", "string", "RoastBatchId", "Codice univoco della tostatura.", ["codice tostatura"]),
            ("RoastDate", "dateTime", "RoastDate", "Data della tostatura.", ["data tostatura"]),
            ("RoastPlant", "string", "RoastPlant", "Impianto di torrefazione.", ["torrefazione", "impianto"]),
            ("RoastProfile", "string", "RoastProfile", "Profilo di tostatura.", ["profilo tostatura"]),
            ("RoastWeightKg", "double", "RoastWeightKg", "Peso del caffè tostato in kg.", []),
        ],
    ),
    dict(
        label="PackagingRun",
        table="packaging_runs",
        key=["PackagingRunId"],
        comment=(
            "Un ciclo di confezionamento: è il «lotto» nel linguaggio della logistica, quello stampato "
            "sulla busta. Ogni PackagingRun confeziona caffè di un solo RoastBatch."
        ),
        synonyms=["packaging run", "lotto di confezionamento", "confezionamento", "lotto busta"],
        props=[
            ("PackagingRunId", "string", "PackagingRunId", "Codice univoco del ciclo di confezionamento.", ["codice confezionamento"]),
            ("PackagingDate", "dateTime", "PackagingDate", "Data del confezionamento.", ["data confezionamento"]),
            ("PackagingLine", "string", "PackagingLine", "Linea di confezionamento.", ["linea"]),
            ("BagsProduced", "integer", "BagsProduced", "Numero di buste da 1 kg prodotte.", ["buste prodotte"]),
            ("BestBefore", "dateTime", "BestBefore", "Data di scadenza consigliata.", ["da consumarsi preferibilmente entro"]),
        ],
    ),
    dict(
        label="Shipment",
        table="shipments",
        key=["shipment_id"],
        comment=(
            "Una spedizione di caffè confezionato verso un negozio. Nel sistema della supply chain "
            "il negozio di destinazione si chiama destination_id ed è lo stesso codice di StoreId."
        ),
        synonyms=["spedizione", "consegna", "invio", "DDT"],
        props=[
            ("ShipmentId", "string", "shipment_id", "Codice univoco della spedizione.", ["codice spedizione"]),
            ("ShipDate", "dateTime", "ship_date", "Data di partenza della spedizione.", ["data spedizione"]),
            ("DeliveryDate", "dateTime", "delivery_date", "Data di consegna al negozio.", ["data consegna", "data arrivo"]),
            ("Carrier", "string", "carrier", "Corriere.", ["corriere", "vettore"]),
            ("BagsShipped", "integer", "bags_shipped", "Numero di buste spedite.", ["buste spedite"]),
        ],
    ),
    dict(
        label="Store",
        table="stores",
        key=["StoreId"],
        comment=(
            "Un punto vendita Fourth Coffee (la quarta mano: il cliente beve qui). Lo stesso negozio si "
            "chiama StoreId nell'anagrafica, store_id nel registro dispositivi e destination_id nelle "
            "spedizioni: sono lo stesso codice."
        ),
        synonyms=["negozio", "punto vendita", "caffetteria", "bar", "outlet", "drive-through", "store"],
        props=[
            ("StoreId", "string", "StoreId", "Codice univoco del negozio (es. S003).", ["codice negozio"]),
            ("StoreName", "string", "StoreName", "Nome del negozio.", ["nome negozio"]),
            ("City", "string", "City", "Città del negozio.", ["città", "comune"]),
            ("StoreFormat", "string", "StoreFormat", "Formato: Bar, Drive-through o Kiosk.", ["formato"]),
            ("OpenedOn", "dateTime", "OpenedOn", "Data di apertura.", ["data apertura"]),
        ],
    ),
    dict(
        label="Equipment",
        table="equipment",
        key=["asset_id"],
        comment=(
            "Una macchina espresso installata in un negozio. Ha due proprietà time series dalla "
            "telemetria: PumpPressureBar (normale tra 8,5 e 9,5 bar; sotto 8,5 bar l'espresso è "
            "sottoestratto e risulta acido) e BoilerTempC (normale tra 90 e 96 °C; sotto 90 °C il "
            "caffè risulta acido)."
        ),
        synonyms=["macchina", "macchina espresso", "macchina del caffè", "attrezzatura", "asset"],
        props=[
            ("AssetId", "string", "asset_id", "Codice univoco della macchina.", ["codice macchina", "matricola"]),
            ("EquipmentModel", "string", "model", "Modello della macchina.", ["modello"]),
            ("InstallDate", "dateTime", "install_date", "Data di installazione.", ["data installazione"]),
        ],
        timeseries=dict(
            table="machine_telemetry",
            key="asset_id",
            timestamp="timestamp",
            props=[
                ("PumpPressureBar", "double", "pump_pressure_bar", "Pressione della pompa in bar (time series). Normale: 8,5-9,5 bar.", ["pressione pompa", "pressione"]),
                ("BoilerTempC", "double", "boiler_temp_c", "Temperatura della caldaia in °C (time series). Normale: 90-96 °C.", ["temperatura caldaia", "temperatura acqua"]),
            ],
        ),
    ),
    dict(
        label="Complaint",
        table="complaints",
        key=["ComplaintId"],
        comment=(
            "Un reclamo di un cliente in un negozio. ComplaintCategory distingue per esempio "
            "«Gusto acido», «Gusto amaro», «Temperatura», «Servizio lento», «Errore ordine»."
        ),
        synonyms=["reclamo", "lamentela", "segnalazione cliente", "feedback negativo"],
        props=[
            ("ComplaintId", "string", "ComplaintId", "Codice univoco del reclamo.", []),
            ("ComplaintDate", "dateTime", "ComplaintDate", "Data del reclamo.", ["data reclamo"]),
            ("ComplaintCategory", "string", "ComplaintCategory", "Categoria del reclamo.", ["tipo reclamo", "motivo reclamo"]),
            ("ComplaintText", "string", "ComplaintText", "Testo del reclamo.", ["testo"]),
            ("Channel", "string", "Channel", "Canale: App, Cassa o Web.", ["canale"]),
        ],
    ),
]

# Relationship: label, source entity, target entity, source table, source-key column,
# target-key column, comment, synonyms
RELATIONSHIPS = [
    ("supplies", "Farm", "GreenLot", "green_lot_farms", "FarmId", "GreenLotId",
     "La Farm rifornisce il GreenLot (molti-a-molti: un lotto mescola più farm; la quota è SharePct in green_lot_farms).",
     ["rifornisce", "fornisce", "contiene caffè di"]),
    ("holdsCertification", "Farm", "Certification", "certifications", "FarmId", "CertificationId",
     "La Farm possiede questa Certification.",
     ["ha certificazione", "certificata da"]),
    ("roastedInto", "GreenLot", "RoastBatch", "roast_batches", "GreenLotId", "RoastBatchId",
     "Il GreenLot è stato tostato in questo RoastBatch.",
     ["tostato in"]),
    ("packedInto", "RoastBatch", "PackagingRun", "packaging_runs", "RoastBatchId", "PackagingRunId",
     "Il RoastBatch è stato confezionato in questo PackagingRun.",
     ["confezionato in"]),
    ("shippedWith", "PackagingRun", "Shipment", "shipments", "packaging_run_id", "shipment_id",
     "Il PackagingRun è stato spedito con questa Shipment.",
     ["spedito con"]),
    ("deliveredTo", "Shipment", "Store", "shipments", "shipment_id", "destination_id",
     "La Shipment è stata consegnata a questo Store (destination_id = StoreId).",
     ["consegnata a", "destinazione"]),
    ("installedAt", "Equipment", "Store", "equipment", "asset_id", "store_id",
     "La macchina è installata in questo Store (store_id = StoreId).",
     ["installata in", "si trova in"]),
    ("reportedAt", "Complaint", "Store", "complaints", "ComplaintId", "StoreId",
     "Il reclamo è stato fatto in questo Store.",
     ["segnalato in", "ricevuto da"]),
]
