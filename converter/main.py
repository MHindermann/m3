""" main.py """

from __future__ import annotations
from typing import List, Dict, Union
from collections import OrderedDict
from os import path
import json

from utility import load_codes, load_workbook, load_template

DIR = path.dirname(path.abspath(__file__))
WORKBOOK = path.join(DIR, "input/owcm_full.xlsx")
CODES = load_codes(WORKBOOK)
SCHEME = {"uri": "https://bartoc.org/owcm/",
          "type": "skos:ConceptScheme",
          "label": "OWCM"}
INSCHEME = "https://bartoc.org/owcm/"

def main(workbook: str, verbose: int = 0) -> None:
    """ Main app"""

    vocabulary = convert(workbook)
    # print to console:
    if verbose == 1:
        print(json.dumps(vocabulary, indent=4, sort_keys=False))
    # save to file:

    with open(path.join(DIR, "output/owcm_skosmos.json"), 'w') as file:
        json.dump(vocabulary, file, indent=4, sort_keys=False)


def convert(workbook: str) -> OrderedDict:
    """ Convert workbook to JSON-LD in SKOS format """

    vocabulary = load_template()
    graph = [SCHEME]

    wb = load_workbook(workbook)
    for ws in wb:
        for row in ws.iter_rows(min_row=7, min_col=1, max_col=3, values_only=True):  # add max_row for dev

            entry = OrderedDict()

            code = row[0]
            descriptor = row[1]
            change = row[2]

            # convert code to uri and add type:
            if code is None:
                continue
            code = code.replace(" ", "")
            if code is "":
                continue
            uri = make_uri(code)
            entry.update({"uri": uri,
                          "type": "skos:Concept"})

            # add labels:
            labels = parse(descriptor)
            entry.update(labels)

            # add historyNote:
            entry.update({"historyNote": descriptor})

            # add changeNote:
            entry.update(make_changenote(descriptor, change))

            # add hierarchy:
            entry.update(make_hierarchy(code))

            graph.append(entry)

    vocabulary.update({"graph": graph})
    return vocabulary


def make_top(code: str) -> Dict:
    """ Make hierarchy for a top concept """

    codes = CODES.copy()
    broader = None
    narrower = []
    for entry in codes:
        # exclude (other) top concepts (e.g., A):
        if len(entry) < 2:
            continue
        # first symbol of entry matches:
        if code[0] is entry[0]:
            # second symbol is number (e.g, A1):
            if entry[1] in str(set(range(0, 10))):
                narrower.append({"uri": make_uri(entry)})
            # second symbol is not number and no other numbers (e.g., AA):
            elif len(entry) < 3:
                narrower.append({"uri": make_uri(entry)})
    return {"broader": broader,
            "narrower": narrower}


def make_middle(code: str, debug: int = 0) -> Dict:
    """ Make hierarchy for a middle concept """

    if debug == 1:
        print(f"middle concept with code {code}")
    codes = CODES.copy()
    broader = [{"uri": make_uri(code[0])}]
    narrower = []
    for entry in codes:
        if entry == code:
            continue
        elif code in entry and "." not in entry:
            narrower.append({"uri": make_uri(entry)})
    return {"broader": broader,
            "narrower": narrower}


def make_ojn_dot(code: str) -> Dict:
    """ Make hierarchy for OJn-dot(-dot) concepts (e.g., OJ5.11 or OJ5.11.cAbau) """

    codes = CODES.copy()
    # OJ-dot-dot concept (e.g., OJ5.11.cAbau):
    if code.count(".") == 2:
        narrower = None
        broader = [{"uri": make_uri(code.split(".")[0] + "." + code.split(".")[1])}]
    # OJ-dot concept (e.g, OJ5.11):
    else:
        broader = [{"uri": make_uri(code.split(".")[0])}]
        narrower = []
        for entry in codes:
            if entry == code:
                continue
            elif code in entry:
                narrower.append({"uri": make_uri(entry)})
        if len(narrower) == 0:
            narrower = None
    return {"broader": broader,
            "narrower": narrower}


def make_ojn(code: str) -> Dict:
    """ Make hierarchy for OJn concepts (e.g., OJ1) """

    codes = CODES.copy()
    broader = [{"uri": make_uri("OJ")}]
    narrower = []
    for entry in codes:
        if entry == code:
            continue
        elif code in entry and entry.count(".") == 1:
            narrower.append({"uri": make_uri(entry)})
    if len(narrower) == 0:
        narrower = None
    return {"broader": broader,
            "narrower": narrower}


def make_hierarchy(code: str) -> Dict:
    """ Make broader and narrower for code """

    # top concept:
    if len(code) == 1:
        return make_top(code)
    # middle concept:
    elif len(set(code).intersection(str(set(range(0, 10))))) == 0:
        return make_middle(code)
    # bottom concept:
    else:
        print(f"bottom concept with code {code}")  # debug
        # OJn special case:
        if "." in code:
            return make_ojn_dot(code)

        elif "OJ" in code:
            return make_ojn(code)
        # standard case:
        else:
            narrower = None
            broader = [{"uri": make_uri(code[:2])}]
            return {"broader": broader,
                    "narrower": narrower}


def make_uri(code: str) -> str:
    """ Convert OCWM-code to URI """

    code = code.replace(" ", "")
    uri = "https://bartoc.org/ocwm/" + code
    return uri


def parse(label: str) -> Dict:
    """ Parse OCWM-label"""

    label_copy = label.strip()

    # prefLabel:
    label_split = label_copy.split(".", 1)
    value = label_split[0]
    pref_label = {"lang": "en",
                  "value": value}

    # definition:
    if len(label_split) < 2 or label_split == "":
        definition = None
    else:
        value = label_split[1].strip()
        definition = {"lang": "en",
                      "value": value}  # text hinter dem punkt

    # TODO: altLabel:
    alt_label = None  # text in klammern oder k, evtl eher hiddenLabel

    # inScheme:
    in_scheme = INSCHEME

    labels = {"prefLabel": pref_label,
              "altLabel": alt_label,
              "definition": definition,
              "inScheme": in_scheme}

    return labels


def make_changenote(descriptor, change: Union[str, None]) -> Dict:
    """ Make changeNote based on descriptor and change """

    if change is None:
        return {"changeNote": None}
    else:
        change = change.strip()
        # cell is of form "K":
        if change == "K":
            change_note = descriptor
        # cell is of from "K word(s)":
        else:
            change_note = change[2:]

        return {"changeNote": change_note}


main(WORKBOOK, 1)
