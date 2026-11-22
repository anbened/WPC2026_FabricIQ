# Prompt: farsi generare un'ontologia per il proprio business

Un modello di prompt da usare con un assistente AI (Copilot, Claude, ChatGPT o altri) per ottenere un file di
ontologia importabile in Microsoft Fabric IQ. Sostituisci le parti tra parentesi quadre.

Prima di usarlo, tre cose da sapere:

- **Il lavoro vero è il contesto.** Le istruzioni sul formato sono poche righe; la qualità del risultato dipende da
  quanto bene descrivi business, gergo, sistemi e regole. Se il contesto è vago, l'ontologia sarà vaga.
- **Lascia che l'AI ti faccia domande.** Il prompt le chiede di segnalare le ambiguità invece di risolverle da sola.
  Le sue domande sono le decisioni di modellazione che devi prendere tu, magari insieme ai reparti coinvolti.
- **Verifica sempre il risultato.** Importa il file in un item Ontology vuoto, leggi il riepilogo e il log
  dell'import: lì vedi cosa Fabric ha accettato e cosa ha scartato.

Per un esempio compilato vedi [il prompt di Fourth Coffee](fourth-coffee.md).

## Il prompt

```
Sei un ontology engineer. Devo costruire un'ontologia per Microsoft Fabric IQ che descriva
[il nostro dominio, es. la supply chain dal fornitore al cliente].

TI DO QUESTO CONTESTO
1. Il business: [chi siamo e il processo end-to-end in 5-10 righe]
2. Il glossario: [i termini che usiamo e cosa significano per ciascun reparto,
   soprattutto quelli che reparti diversi usano in modo diverso]
3. Le sorgenti: [tabelle e colonne principali, con il sistema da cui vengono;
   segnala quando lo stesso concetto ha nomi diversi]
4. Le regole: [le regole di business in linguaggio naturale, con soglie e date,
   es. "compriamo solo da fornitori certificati alla data di acquisto"]

PRIMA DI SCRIVERE IL FILE
- Fammi domande dove un termine ha più significati o dove due sorgenti chiamano in modo
  diverso la stessa cosa. Non scegliere tu.
- Proponimi l'elenco di entità, relazioni e proprietà principali e aspetta la mia conferma.

POI GENERA UN FILE TURTLE (.ttl) CON QUESTI VINCOLI
- Namespace: [https://nostra-azienda.example/ontology/]
- owl:Class per ogni entità; owl:DatatypeProperty sempre con rdfs:domain e un rdfs:range
  xsd (string, integer, double, dateTime, boolean); owl:ObjectProperty con dominio e codominio.
- Nomi in inglese, PascalCase: 1-26 caratteri, solo lettere, numeri, trattino e underscore,
  senza spazi.
- Un rdfs:comment in [italiano] per ogni concetto, che spieghi cosa significa per il business,
  con soglie e regole: è quello che leggerà l'agente.
- skos:altLabel in [italiano] per i sinonimi che le persone usano davvero.
- Niente restrizioni OWL complesse né proprietà transitive o simmetriche.

INFINE ELENCA A PARTE
la chiave di ogni entità, la colonna sorgente di ogni proprietà e il testo di ogni regola:
chiavi, binding e regole si configurano in Fabric dopo l'import.
```

## Perché questi vincoli

| Vincolo | Motivo |
|---|---|
| Ogni proprietà con `rdfs:domain` | Fabric salta le proprietà che non riesce ad attribuire a un'entità importata |
| Nomi di 1-26 caratteri, senza spazi | Sono le regole di Fabric per i nomi di entità e proprietà |
| Tipi xsd semplici | Corrispondono ai tipi delle proprietà in Fabric; quelli non supportati diventano stringhe |
| Niente restrizioni OWL | Fabric non ha un equivalente e le ignora |
| Chiavi, binding e regole a parte | Lo standard RDF non li trasporta: si configurano in Fabric dopo l'import |

## Alternative in Fabric

Il prompt non è l'unica strada. Fabric può generare un'ontologia anche da un semantic model di Power BI o con
l'AI direttamente nel prodotto. Il prompt è utile quando parti da zero, da documenti o da sistemi esterni a Fabric,
oppure quando vuoi un file portabile da rivedere e versionare.
