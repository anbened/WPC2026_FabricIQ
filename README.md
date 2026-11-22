# Fabric IQ: dai dati unificati all'intelligenza unificata

Materiale della sessione di **Andrea Benedetti** a **WPC 2026**.

Ad Assago i clienti di Fourth Coffee si lamentano: il caffè è acido. Le metriche dicono *quanto* sono aumentati
i reclami, non *perché*. La risposta attraversa quattro sistemi che chiamano lo stesso negozio in tre modi
diversi, tre significati della parola «lotto» e una regola aziendale che non sta in nessuna tabella.

Questo repository contiene tutto quello che serve per capire l'idea, rifare la demo sul proprio tenant
Microsoft Fabric e applicare lo stesso metodo al proprio business.

## Da dove partire

| Se vuoi… | Tempo | Vai a |
|---|---|---|
| **Capire** le idee della sessione | 5 minuti | [Le idee chiave](docs/idee-chiave.md) |
| **Rifare la demo** su Microsoft Fabric | circa 1 ora | [Setup](docs/setup.md), poi [Demo](docs/demo.md) |
| **Costruire un'ontologia** per il tuo business | dipende dal dominio | [Le scelte di modellazione](docs/design.md) e [il prompt](prompts/template.md) |

## La storia in breve

Fourth Coffee è una catena di caffetterie immaginaria. Il caffè fa questo percorso:

```
Farm ──rifornisce──▶ GreenLot ──tostato in──▶ RoastBatch ──confezionato in──▶ PackagingRun
                                                                                   │
                     Store ◀──consegnata a── Shipment ◀──────spedito con───────────┘
```

Ad Assago i reclami per caffè acido passano da 3 a 17 a settimana. Il sospetto ovvio è la macchina espresso,
ma la telemetria è nella norma. Risalendo la catena si scopre che il caffè arriva da un lotto acquistato
una settimana dopo la sospensione di una delle farm che lo riforniscono: la regola aziendale
(la *Fourth Hand Standard*) è stata violata. Le consegne e i reclami indicano il caffè come causa più
plausibile. La demo confronta come due agenti motivano la decisione, uno con le tabelle del lakehouse
e uno con il contesto dell'**ontologia** di Fabric IQ.

## Cosa contiene

| Cartella | Contenuto |
|---|---|
| [`ontology/`](ontology) | L'ontologia di Fourth Coffee, in Turtle (`.ttl`) e RDF/XML (`.rdf`), pronta da importare in Fabric |
| [`data/`](data) | 11 tabelle CSV di dati fittizi che raccontano la storia della demo |
| [`notebooks/`](notebooks) | Notebook Fabric che carica i CSV come tabelle Delta con i tipi corretti |
| [`docs/`](docs) | Idee chiave, guida al setup, script della demo e scelte di modellazione |
| [`prompts/`](prompts) | Il prompt per farsi generare un'ontologia: modello generico ed esempio compilato |
| [`tools/`](tools) | Script Python che generano ontologia e dati e verificano che la storia torni |
| [`slides/`](slides) | Le slide saranno pubblicate in PDF dopo WPC 2026 |

Per scaricare insieme ontologia, dati, notebook e guida, scegli **Code › Download ZIP** su GitHub.

## Stato delle funzionalità

Al 22 novembre 2026. Lo stato cambia spesso: verifica sempre su
[Microsoft Learn](https://learn.microsoft.com/fabric/iq/ontology/overview).

| Funzionalità | Stato |
|---|---|
| Fabric IQ | Dichiarato generalmente disponibile (giugno 2026) |
| Ontology | **Preview**. La vecchia esperienza viene ritirata il 31 gennaio 2027 |
| Graph in Microsoft Fabric | Generalmente disponibile |
| Operations agent | Generalmente disponibile; azioni pre-approvate in preview |
| Fabric IQ in Copilot Chat e Copilot Cowork | Generalmente disponibile |
| Uso dell'ontologia da agenti esterni (MCP, Foundry IQ, GitHub Copilot) | Preview |

## Avvertenze

- Tutti i dati sono **fittizi**. Fourth Coffee è un'azienda immaginaria usata negli esempi Microsoft;
  nomi di farm, negozi e persone sono inventati.
- È materiale personale dell'autore: **non è documentazione ufficiale Microsoft** e non è supportato da Microsoft.
- Diverse funzionalità sono in preview e possono cambiare.

## Licenza

- Codice (`tools/`, `notebooks/`): [MIT](LICENSE).
- Documentazione, ontologia, dati e prompt: [CC BY 4.0](LICENSE-DOCS.md). Puoi riusarli e adattarli, anche
  per uso commerciale, citando la fonte.

Domande, errori, suggerimenti: apri una [issue](https://github.com/anbened/WPC2026_FabricIQ/issues).
