# La demo

Due agenti, stesse istruzioni di ruolo, stessa domanda. Cambia solo il contesto a cui hanno accesso.
Prima completa il [setup](setup.md).

## I due agenti

Crea due **Fabric data agent** nello stesso workspace.

- Per **A**, aggiungi il lakehouse `FourthCoffeeLH` e seleziona tutte le 11 tabelle.
- Per **B**, aggiungi l'ontologia `FourthCoffee` e verifica che tra le sorgenti associate compaia
  lo stesso lakehouse. I binding forniscono il contesto per interrogare i dati.

Incolla le stesse istruzioni in entrambi e poni la domanda in una nuova conversazione per ciascuno.

> Sei l'assistente qualità di Fourth Coffee. Rispondi in italiano e cita i dati su cui basi la tua decisione.

## La domanda

Non «il caffè era acido»: quello è un aneddoto. La domanda di business ha una decisione dentro:

> *Tra il 7 settembre e il 1° novembre 2026 ad Assago i reclami per caffè acido sono passati da 3 a 17 a settimana. È colpa delle macchine o del caffè?
> Devo mandare il tecnico o bloccare il caffè?*

Domande di approfondimento:

1. *Da quale lotto di caffè verde viene il caffè consegnato ad Assago dal 12 ottobre al 1° novembre 2026 inclusi?*
2. *Quel lotto rispetta la Fourth Hand Standard?*
3. *Ci sono altri lotti della stessa farm ancora in magazzino?*
4. *Quel lotto è arrivato anche in altri negozi? Cosa dicono i reclami lì?*

## La risposta attesa

Le settimane vanno da S1 (dal 7 settembre 2026) a S8; S6 inizia il 12 ottobre.

- **La telemetria è nella norma.** `EQ-S003-01` ed `EQ-S003-02` restano tra 8,6 e 9,4 bar di pressione e sopra
  i 91 °C di caldaia per tutto il periodo.
- **I reclami «Gusto acido» ad Assago** per settimana: 3, 2, 4, 3, 3, **9, 14, 17**.
- **La catena.** Da S6 Assago riceve caffè del lotto verde `GL-2026-037`: tostature `RB-1013`, `RB-1015`,
  `RB-1017`, confezionamenti `PR-5013`, `PR-5015`, `PR-5017`, prima consegna il 13 ottobre.
- **La violazione.** `GL-2026-037` è stato acquistato il 5 ottobre 2026 e contiene il 35% di caffè della farm
  `F005` *Hacienda San Rafael*, sospesa dal 28 settembre: l'audit del 25 settembre non è stato superato per
  difetti di fermentazione.
- **La sfumatura temporale.** Anche `GL-2026-033` contiene caffè di `F005`, ma è stato acquistato il 20 agosto,
  prima della sospensione: è conforme, e infatti ad Assago, che lo ha ricevuto da S3 a S5, i reclami erano nella norma.
- **La controprova.** Bergamo (`S002`) riceve `GL-2026-037` da S7 e i suoi reclami per caffè acido salgono a 5 e 7.
- **L'azione.** `GL-2026-039`, acquistato il 22 ottobre con il 60% di caffè di `F005`, è ancora in magazzino
  (`InStock`): va messo in attesa.

La decisione da comunicare al responsabile qualità è mettere in attesa `GL-2026-039` per la violazione
accertata e verificare il caffè di `GL-2026-037` nei negozi che lo hanno ricevuto. Consegne, reclami e
telemetria indicano il caffè come causa più plausibile. Ogni reclamo identifica il negozio, mentre la
busta usata per quella tazza resta sconosciuta. Le letture di Assago non indicano un intervento tecnico.

Confronta come A e B motivano il diverso esito di `033` e `037` e quali dati citano. Dopo aver raccolto
entrambe le risposte, puoi proporre a entrambi un secondo giro guidato:

> Controlla la telemetria, risali dal negozio alle farm e verifica la Fourth Hand Standard alla data di
> acquisto di ogni lotto. Quali identificativi e date giustificano la tua decisione?

## Senza dati: cosa sa l'ontologia da sola

Per questa parte apri l'item **Ontology** `FourthCoffee` e avvia il suo **Ontology agent**. Puoi
provare queste domande anche subito dopo l'import, prima di configurare i binding. Per l'esercizio
su `WorkOrder` usa la modalità **Plan** per visualizzare la proposta.

| Domanda | Cosa mostra |
|---|---|
| *Cosa intendiamo in Fourth Coffee quando diciamo «lotto»?* | La disambiguazione tra GreenLot, RoastBatch e PackagingRun |
| *Come risalgo da un punto vendita alla farm che ha prodotto il caffè?* | I sinonimi («punto vendita» = Store) e il percorso nel grafo |
| *Ad Assago il caffè è acido. Quali sono le possibili cause e quali dati dovrei controllare per ciascuna?* | Il ragionamento diagnostico: soglie della macchina e regola sui lotti vengono dalle descrizioni |
| *Cosa significa che un lotto è conforme alla Fourth Hand Standard?* | La regola vive nel modello, non in una tabella |
| *Quale lotto è arrivato ad Assago dal 26 ottobre al 1° novembre 2026?* | Prima dei binding l'agente può spiegare il percorso, ma per identificare il lotto servono i dati delle consegne |
| *Aggiungi un entity type WorkOrder collegato a Equipment* | Il modello a proposta: l'agente propone, una persona approva |

Un esercizio utile: confronta la risposta alla domanda sulle cause con le descrizioni nel file
[`FourthCoffee.ttl`](../ontology/FourthCoffee.ttl). Alcune parti vengono dal modello (le soglie, la regola),
altre dalla conoscenza generale dell'AI (tostatura, logistica). È la divisione del lavoro tra ontologia e modello linguistico.

## Consigli per chi presenta

- Le risposte degli agenti non sono deterministiche: prova ogni domanda più volte e registra un video di riserva.
- Non è garantito che l'agente A fallisca: un modello forte può intuire che `destination_id` è il negozio.
  La differenza più solida da mostrare è la coerenza nell'applicare la regola alla data giusta.
- Le funzionalità in preview cambiano: rifai la prova il giorno prima sul tenant che userai.
