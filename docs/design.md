# Le scelte di modellazione

Perché l'ontologia di Fourth Coffee è fatta così. Ogni scelta è un tipo di decisione che incontrerai
modellando il tuo business.

## 1. Modellare la domanda, non l'azienda

L'ontologia ha nove entity type: Farm, Certification, GreenLot, RoastBatch, PackagingRun, Shipment, Store,
Equipment, Complaint. Sono le entità necessarie per rispondere a una domanda precisa: *perché ad Assago il
caffè è acido?* Mancano prodotti, clienti, dipendenti, prezzi. Non perché non contino, ma perché un'ontologia
che parte da tutto non finisce mai. Si parte da una decisione importante e si estende quando arriva la
domanda successiva.

## 2. Tre «lotti», tre entità

Sourcing, torrefazione e logistica usano tutti la parola «lotto», con significati diversi. Abbiamo scelto
tre entità distinte con nomi non ambigui (`GreenLot`, `RoastBatch`, `PackagingRun`) e in ciascuna descrizione
abbiamo scritto esplicitamente da cosa si distingue. I sinonimi aiutano l'agente a capire le persone
(«lotto verde», «tostatura», «lotto di confezionamento»), ma la parola «lotto» da sola non è sinonimo di nessuna:
è ambigua, e l'ambiguità va dichiarata, non nascosta.

## 3. Un negozio, tre nomi: niente ETL

Il negozio si chiama `StoreId`, `store_id` e `destination_id` in tre sistemi diversi. Si potrebbe rinominare
tutto in una pipeline di trasformazione. Abbiamo scelto di lasciare i dati come sono e di riconciliarli
nell'ontologia: le relazioni `deliveredTo` e `installedAt` sono collegate rispettivamente a `destination_id`
e `store_id`, e la descrizione di Store dice che sono lo stesso codice. Il significato sta nel modello,
non in una copia dei dati.

## 4. La certificazione è un'entità, non un attributo

La soluzione più semplice sarebbe un campo «certificata sì/no» sulla farm. Ma la regola chiede se la farm
era in regola *alla data dell'acquisto*, e uno stato attuale non risponde a una domanda sul passato.
`Certification` è un'entità separata con date di validità, data di sospensione, motivo ed esito dell'audit,
e può avere una storia (nei dati, `F004` ha anche una certificazione scaduta). La descrizione avverte che
`CertStatus` è lo stato di oggi e che per una data passata vanno usate le date.

## 5. Il mix dei lotti è molti-a-molti

Un lotto di caffè verde mescola chicchi di più farm, e una farm rifornisce più lotti. La relazione `supplies`
passa da una tabella di mapping (`green_lot_farms`) che contiene anche la quota di ciascuna farm. La regola dice
che basta una farm non in regola, qualunque sia la sua quota: il 35% di `GL-2026-037` è sufficiente.

## 6. Le descrizioni sono istruzioni

Ogni entità e proprietà ha una descrizione in italiano scritta per chi ragiona sui dati, non per chi li carica.
Contiene le soglie operative (pressione normale tra 8,5 e 9,5 bar), le avvertenze (lo stato attuale non è lo
stato a una data) e le regole. È quello che l'agente legge: quando dice «sotto 8,5 bar il caffè può risultare
acido», sta citando la descrizione di Equipment.

## 7. La regola, scritta due volte

Fabric distingue le regole semantiche (che definiscono un significato, come la conformità di un lotto) dalle
regole operative (che fanno scattare un'azione, come aprire un intervento quando la pressione scende).
La Fourth Hand Standard è una regola semantica: va creata come regola nell'ontologia, ed è ripetuta anche
nelle descrizioni di Farm e GreenLot perché l'import RDF non trasporta le regole.

Un limite da conoscere: la regola semantica è testo che l'agente interpreta, non un calcolo eseguito dal motore.
Per questo abbiamo reso esplicite in proprietà tutte le date che servono (`PurchaseDate`, `ValidFrom`,
`ValidTo`, `SuspendedFrom`): più la regola è verificabile sui dati, meno dipende dall'interpretazione.

## 8. Nomi e vincoli tecnici

- Nomi in inglese e PascalCase, descrizioni e sinonimi in italiano: i nomi restano stabili e leggibili in
  qualsiasi strumento, le descrizioni parlano la lingua di chi fa le domande.
- Fabric accetta nomi da 1 a 26 caratteri con lettere, numeri, trattini e underscore.
- Ogni proprietà ha un dominio (l'entità a cui appartiene): senza, l'import la salta.
- Gli identificativi RDF hanno la forma `Entità_Proprietà` (es. `Equipment_PumpPressureBar`). In alcune risposte
  l'agente li mostra così; il nome visualizzato in Fabric è quello senza prefisso.
- Niente costrutti OWL avanzati (restrizioni, proprietà transitive): Fabric non li supporta.

## 9. Cosa è rimasto fuori

Buoni esercizi per estendere il modello:

- **Processor** come entità (oggi è solo una proprietà del lotto): serve se vuoi verificare anche la seconda
  delle quattro mani.
- **WorkOrder** collegato a Equipment: serve alla regola operativa sulla pressione.
- **Product** e **Sale**: servono per misurare l'impatto economico del problema.

## 10. Dati che raccontano una storia

I dati sono generati da [`tools/gen_data.py`](../tools/gen_data.py) per mettere alla prova il ragionamento,
non solo per riempire tabelle:

- un lotto della stessa farm acquistato *prima* della sospensione (`GL-2026-033`), conforme: distingue chi applica
  la regola alla data giusta da chi generalizza;
- un secondo negozio (Bergamo) che riceve il lotto non conforme una settimana dopo: una controprova indipendente;
- una macchina di Torino con un calo di pressione reale ma estraneo alla storia: una falsa pista;
- un lotto non conforme ancora in magazzino (`GL-2026-039`): la domanda finisce con un'azione.

Lo script [`tools/verify.py`](../tools/verify.py) controlla che tutto questo sia vero nei dati.
