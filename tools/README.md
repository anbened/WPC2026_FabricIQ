# Strumenti

Script Python che generano l'ontologia e i dati della demo e verificano che la storia torni.
Servono se vuoi rigenerare i file, modificarli o adattarli a un tuo scenario.

## Requisiti

Python 3.10 o successivo.

```bash
pip install -r tools/requirements.txt
```

## Uso

Dalla radice del repository:

```bash
python tools/build_ontology.py ontology   # genera ontology/FourthCoffee.ttl e .rdf
python tools/gen_data.py data             # genera i CSV in data/
python tools/verify.py data               # controlla binding, regola e storia
```

## I file

| File | Cosa fa |
|---|---|
| `spec.py` | Unica fonte di verità dell'ontologia: entità, proprietà, colonne sorgente, relazioni, descrizioni, sinonimi e testo della regola |
| `build_ontology.py` | Legge `spec.py`, controlla i vincoli di Fabric sui nomi e scrive Turtle e RDF/XML, con una verifica di andata e ritorno |
| `gen_data.py` | Genera i dati fittizi; la storia della demo è descritta in testa al file |
| `verify.py` | Controlla che ogni colonna collegata esista, che le chiavi siano univoche, che le relazioni si risolvano, e applica la Fourth Hand Standard ai dati |

## Adattare a un altro scenario

1. Modifica `spec.py`: entità, proprietà (con la colonna sorgente), relazioni, descrizioni e regola.
2. Rigenera l'ontologia con `build_ontology.py`: lo script si ferma se un nome non rispetta i vincoli di Fabric
   (1-26 caratteri, lettere, numeri, trattini e underscore) o se la stessa proprietà ha tipi diversi.
3. Se usi dati tuoi, adatta `verify.py` per controllare che le colonne indicate in `spec.py` esistano.

I dati sono generati con un seme fisso: rieseguendo `gen_data.py` ottieni sempre gli stessi file.
