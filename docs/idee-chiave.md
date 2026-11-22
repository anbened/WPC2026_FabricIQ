# Le idee chiave

Sei idee dalla sessione, in cinque minuti di lettura. Non serve conoscere Microsoft Fabric.

## 1. Unificare i dati non significa unificarne il significato

Portare tutti i dati in un unico posto (in Fabric, OneLake) risolve il problema di *dove* sono i dati.
Non risolve il problema di *cosa vogliono dire*. Nell'esempio, lo stesso negozio si chiama `StoreId`
nell'anagrafica, `store_id` nel registro delle macchine e `destination_id` nelle spedizioni. I dati sono
tutti lì, ma nessuno, persona o agente, sa che si tratta della stessa cosa finché qualcuno non lo scrive.

## 2. La stessa parola, significati diversi

In Fourth Coffee «lotto» significa tre cose: per il sourcing è il lotto di caffè verde acquistato,
per la torrefazione è una tostatura, per la logistica è il ciclo di confezionamento stampato sulla busta.
Ogni reparto ha ragione. Ma un agente che riceve la domanda «da quale lotto viene questo caffè?» deve
sapere quale dei tre intendi. Un'**ontologia** dà a ciascun concetto un nome, una definizione e i suoi
collegamenti con gli altri.

## 3. Le metriche dicono quanto, non perché

I reclami ad Assago passano da 3 a 17 a settimana: una dashboard lo mostra benissimo. Ma per sapere
*perché* bisogna risalire una catena che attraversa clienti, macchine, spedizioni, torrefazione, acquisti
e certificazioni dei produttori. Le domande «perché» sono quelle in cui un modello semantico fatto di
misure si ferma e serve un modello delle entità e delle loro relazioni.

## 4. Le regole più importanti non stanno nelle tabelle

La causa del problema è una regola: «compriamo caffè solo da produttori in regola il giorno dell'acquisto».
Le date delle certificazioni sono in una tabella; il significato di quelle date no. Sta in una policy,
nella testa di qualcuno, o in un documento che nessun sistema collega ai dati. Scritta nell'ontologia,
la regola diventa contesto che l'agente usa.

## 5. Le descrizioni fanno parte del modello

Quando l'agente dice «sotto 8,5 bar il caffè può risultare acido», non lo sta inventando: lo legge nella
descrizione dell'entità *macchina espresso*. Descrizioni, sinonimi e soglie non sono commenti per i
programmatori: sono quello che l'agente legge per ragionare. Descrizioni vaghe producono ragionamenti vaghi.

## 6. L'AI scrive la sintassi, il significato lo decidete voi

Un'AI genera in pochi secondi un file di ontologia formalmente corretto. Il lavoro vero è decidere cosa
significano i concetti, chi ha l'autorità di definirli e quali regole valgono. Il [prompt](../prompts/template.md)
di questo repository chiede all'AI di **fare domande** sulle ambiguità invece di scegliere da sola.

## Non vendi caffè?

Sostituisci i chicchi con componenti, principi attivi, materie prime. Lotti che si mescolano, fornitori con
certificazioni che scadono, un sintomo che si manifesta lontano dalla causa: manifattura, alimentare,
farmaceutico, logistica hanno lo stesso problema. È tracciabilità, più conformità, più analisi delle cause.

## Quattro domande da portare in azienda

1. Quali parole usiamo con significati diversi tra un reparto e l'altro?
2. Quali regole importanti vivono in documenti o nella testa delle persone, e non nei dati?
3. Chi ha l'autorità di decidere cosa significa un concetto, quando due reparti non sono d'accordo?
4. Quali decisioni oggi richiedono a una persona di saltare tra tre sistemi diversi per avere una risposta?
