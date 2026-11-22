import re
import sys
from pathlib import Path

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import OWL, RDF, RDFS, SKOS, XSD

sys.path.insert(0, str(Path(__file__).parent))
from spec import BASE, ENTITIES, ONTOLOGY_COMMENT, ONTOLOGY_LABEL, RELATIONSHIPS  # noqa: E402

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

NAME_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9_-]{0,24}[A-Za-z0-9])?$")
XSD_MAP = {"string": XSD.string, "integer": XSD.integer, "double": XSD.double,
           "dateTime": XSD.dateTime, "boolean": XSD.boolean}

ont = Namespace(BASE)
g = Graph()
g.bind("fc", ont)
g.bind("owl", OWL)
g.bind("skos", SKOS)
g.bind("xsd", XSD)

onto = URIRef(BASE)
g.add((onto, RDF.type, OWL.Ontology))
g.add((onto, RDFS.label, Literal(ONTOLOGY_LABEL)))
g.add((onto, RDFS.comment, Literal(ONTOLOGY_COMMENT)))

seen_names, prop_types = set(), {}


def check(name):
    assert NAME_RE.match(name), f"invalid Fabric name: {name}"


for e in ENTITIES:
    check(e["label"])
    assert e["label"] not in seen_names
    seen_names.add(e["label"])
    c = ont[e["label"]]
    g.add((c, RDF.type, OWL.Class))
    g.add((c, RDFS.label, Literal(e["label"])))
    g.add((c, RDFS.comment, Literal(e["comment"])))
    for s in e["synonyms"]:
        g.add((c, SKOS.altLabel, Literal(s)))
    props = list(e["props"]) + list(e.get("timeseries", {}).get("props", []))
    for (label, typ, _col, comment, syns) in props:
        check(label)
        assert prop_types.setdefault(label, typ) == typ, f"type clash on {label}"
        p = ont[f"{e['label']}_{label}"]
        g.add((p, RDF.type, OWL.DatatypeProperty))
        g.add((p, RDFS.label, Literal(label)))
        g.add((p, RDFS.domain, c))
        g.add((p, RDFS.range, XSD_MAP[typ]))
        g.add((p, RDFS.comment, Literal(comment)))
        for s in syns:
            g.add((p, SKOS.altLabel, Literal(s)))

for (label, src, tgt, _t, _sc, _tc, comment, syns) in RELATIONSHIPS:
    check(label)
    assert label not in seen_names
    seen_names.add(label)
    r = ont[f"{src}_{label}_{tgt}"]
    g.add((r, RDF.type, OWL.ObjectProperty))
    g.add((r, RDFS.label, Literal(label)))
    g.add((r, RDFS.domain, ont[src]))
    g.add((r, RDFS.range, ont[tgt]))
    g.add((r, RDFS.comment, Literal(comment)))
    for s in syns:
        g.add((r, SKOS.altLabel, Literal(s)))

header = (
    "# Fourth Coffee - ontologia per la demo Fabric IQ (WPC 2026)\n"
    "# Importare in un item Ontology (preview) VUOTO: Home > Import ontology.\n"
    "# Chiavi, data binding e regole non fanno parte dello standard RDF: vanno configurati dopo l'import (vedi docs/setup.md).\n\n"
)
(OUT / "FourthCoffee.ttl").write_text(header + g.serialize(format="turtle"), encoding="utf-8")
g.serialize(destination=str(OUT / "FourthCoffee.rdf"), format="xml", encoding="utf-8")

# Round-trip check
g2 = Graph().parse(OUT / "FourthCoffee.ttl", format="turtle")
g3 = Graph().parse(OUT / "FourthCoffee.rdf", format="xml")
assert len(g2) == len(g) == len(g3)
print("triples", len(g),
      "classes", len(list(g.subjects(RDF.type, OWL.Class))),
      "datatype props", len(list(g.subjects(RDF.type, OWL.DatatypeProperty))),
      "relationships", len(list(g.subjects(RDF.type, OWL.ObjectProperty))))
