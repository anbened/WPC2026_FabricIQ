# La demo

Due agenti, stesse istruzioni di ruolo, stessa domanda. Cambia solo il contesto a cui hanno accesso.
Prima completa il [setup](setup.md).

## I due agenti

**Agente A**: Fabric data agent con sorgente **solo il lakehouse** `FourthCoffeeLH`, tutte le tabelle.
Istruzioni:

> Sei l'assistente qualità di Fourth Coffee. Rispondi in italiano usando i dati disponibili.

**Agente B**: Fabric data agent con sorgente **l'ontologia** `FourthCoffee`. Istruzioni:

> Sei l'assistente qualità di Fourth Coffee. Rispondi in italiano. Per capire la causa di un problema in
> negozio valuta prima la macchina (telemetria), poi il caffè risalendo la catena fino alla Farm.
> Verifica sempre la Fourth Hand Standard alla data di acquisto del lotto. Cita gli identificativi
> (lotti, farm, date) su cui basi la conclusione.

## La domanda

Non «il caffè era acido»: quello è un aneddoto. La domanda di business ha una decisione dentro:

> *Ad Assago i reclami per caffè acido sono passati da 3 a 17 a settimana. È colpa delle macchine o del caffè?
> Devo mandare il tecnico o bloccare il caffè?*

Domande di approfondimento:

1. *Da quale lotto di caffè verde viene il caffè consegnato ad Assago nelle ultime tre settimane?*
2. *Quel lotto rispetta la Fourth Hand Standard?*
3. *Ci sono altri lotti della stessa farm ancora in magazzino?*
4. *Quel lotto è arrivato anche in altri negozi? Cosa dicono i reclami lì?*

## La risposta attesa

Le settimane vanno da S1 (dal 7 settembre 2026) a S8; S6 inizia il 12 ottobre.

- **Le macchine sono a posto.** `EQ-S003-01` ed `EQ-S003-02` restano tra 8,6 e 9,4 bar di pressione e sopra
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

Il punto da far notare non è se l'agente trova `F005`, ma se applica la regola **alla data giusta**:
un agente che conclude «la farm è sospesa, quindi tutti i suoi lotti sono non conformi» sbaglia su `GL-2026-033`.

## Senza dati: cosa sa l'ontologia da sola

Anche prima dei binding, l'agente dell'ontologia ragiona sul modello. Domande utili per mostrarlo:

| Domanda | Cosa mostra |
|---|---|
| *Cosa intendiamo in Fourth Coffee quando diciamo «lotto»?* | La disambiguazione tra GreenLot, RoastBatch e PackagingRun |
| *Come risalgo da un punto vendita alla farm che ha prodotto il caffè?* | I sinonimi («punto vendita» = Store) e il percorso nel grafo |
| *Ad Assago il caffè è acido. Quali sono le possibili cause e quali dati dovrei controllare per ciascuna?* | Il ragionamento diagnostico: soglie della macchina e regola sui lotti vengono dalle descrizioni |
| *Cosa significa che un lotto è conforme alla Fourth Hand Standard?* | La regola vive nel modello, non in una tabella |
| *Quale lotto è arrivato ad Assago la settimana scorsa?* | Il limite: l'ontologia non contiene dati, li collega |
| *Aggiungi un entity type WorkOrder collegato a Equipment* | Il modello a proposta: l'agente propone, una persona approva |

Un esercizio utile: confronta la risposta alla domanda sulle cause con le descrizioni nel file
[`FourthCoffee.ttl`](../ontology/FourthCoffee.ttl). Alcune parti vengono dal modello (le soglie, la regola),
altre dalla conoscenza generale dell'AI (tostatura, logistica). È la divisione del lavoro tra ontologia e modello linguistico.

## Consigli per chi presenta

- Le risposte degli agenti non sono deterministiche: prova ogni domanda più volte e registra un video di riserva.
- Non è garantito che l'agente A fallisca: un modello forte può intuire che `destination_id` è il negozio.
  La differenza più solida da mostrare è la coerenza nell'applicare la regola alla data giusta.
- Le funzionalità in preview cambiano: rifai la prova il giorno prima sul tenant che userai.
