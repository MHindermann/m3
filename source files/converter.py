from __future__ import annotations # see https://www.python.org/dev/peps/pep-0563/
from typing import List, Set, Dict, Tuple, Optional, Union
from openpyxl import load_workbook
from collections import OrderedDict

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
WORKBOOK = os.path.join(HERE, "OWC_Text.xlsx")

def main(workbook: str) -> None:
    convert(workbook)


def convert(workbook: str) -> None: # workbook is OWC-Text
    """ Convert the workbook to JSON-LD in SKOS format """

    # load template and transform into ordered dict
    with open("template.json", 'r') as file:
        template = json.load(file)
    jsonld = OrderedDict()
    jsonld.update(template)

    #
    wb = load_workbook(workbook)
    for ws in wb:
        for row in ws.iter_rows(min_row=7, min_col=1, max_col=3, values_only=True):

            entry = OrderedDict()

            # convert code to uri
            code = row[0]
            uri = make_uri(code)

            # use first part of label as preflabel
            label = row[1]

            entry.update( {"uri": uri} )

            print(entry)

    return jsonld

def make_uri(code: str) -> str:
    """ Convert OCW-code to URI """

    code.replace(" ", "")
    uri = "https://bartoc.org/ocw/" + code
    return uri

def parse_label(label: str) -> None:
    """ Parse OCW-label"""

    prefLabel = None # text vor dem punkt
    # "prefLabel":{"lang":"en","value":"Archaeological Measures, Techniques and Analysis"},
    altLabel = None # text in klammern oder k, evtl eher hiddenLabel
    definition = None # text hinter dem punkt
    inScheme = None # wenn top label, dann name des schemas
    broader = None # wenn nicht top label, elternlabel
    narrower = None # wenn nicht bottom label, kinderlabel


    labels = { "skos:prefLabel": prefLabel}

""" context = OrderedDict()
    context.update( { "skos" : "http://www.w3.org/2004/02/skos/core#" } )

    for resource in resources:
        context.update( { resource.name : resource.url } )
    
    context.update( { "results" : { "@id": results_id,
                                    "@type" : "@id",
                                    "@container" : "@set" }
                      } )

    context.update( { "altLabel" : "skos:altLabel",
                      "definition" : "skos:definition",
                      "hiddenLabel" : "skos:hiddenLabel",
                      "prefLabel" : "skos:prefLabel",
                      "source" : "skos:ConceptScheme",
                      "uri" : "@id"
                      } )
"""


""" Data structure of OWC Text entries: 
    1. Code is both hierarchical and identifier; so use as uri 
    2. Bezeichnung is both preflabel and definition
    3. K indicates changes to OWC standard, perhaps as altlabel oder hiddenlabel """

main(WORKBOOK)