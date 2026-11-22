# Ontologia

| File | Formato |
|---|---|
| `FourthCoffee.ttl` | Turtle: il file da importare in Fabric |
| `FourthCoffee.rdf` | RDF/XML: stessa ontologia, alternativa se l'import del Turtle dà problemi |

Contenuto: 9 entity type, 51 proprietà (di cui 2 time series), 8 relazioni, sinonimi e descrizioni in italiano.
Per importarla segui il [setup](../docs/setup.md); per capire perché è fatta così leggi
[Le scelte di modellazione](../docs/design.md).

I file sono generati da [`tools/build_ontology.py`](../tools/build_ontology.py): per modificarli conviene
cambiare `tools/spec.py` e rigenerarli.
