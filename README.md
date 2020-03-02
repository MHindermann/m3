## Reconciling a local OWC instance with GND
_Maximilian Hindermann, https://orcid.org/0000-0002-9337-4655, University of Basel  
CC BY 4.0_

#### 0. Preamble

This document is best viewed on GitHub at https://github.com/MHindermann/m3. 

#### 1. Introduction

The Outline of World Cultures (OWC) is an ontology for cultures created by George P. Murdock [1]. It has since been refined and updated in various ways, most prominently by Yale University’s HRAF division as the subscription database eHRAF World Cultures [2]. The Museum der Kulturen Basel (MKB), however, uses a distinct instance of OWC that reflects the museum’s collection history, for example by vastly enriching OWC’s ontology with respect to modern Papua New Guinea. In this paper, I will explore whether this local OWC instance (call it OWCM) can be reconciled with the Integrated Authority File (GND) [3] used by the Basel University Library (and all other Swiss German university libraries) for indexing. 

#### 2. OWCM input data
The OWCM data was supplied to me in form of three Excel files. In what follows, I will briefly describe the content and structure of each file:

1. `input/owcm_short` contains the main geographical divisions (e.g., Asia) and their subdivisions (e.g., Korea). Each of these 250 entries has three data fields: a one or two-digit alphabetical code indicating the hierarchical level of the entry, a plaintext descriptor consisting of a few words, and a binary field indicating whether the entry was modified by the MKB.
2. `input/owcm_full` contains further lower-level divisions and is a superset of `input/owcm_short`. We can hence ignore `input/owcm_short` from now on. Each of the roughly 3000 entries has again three data fields: an alphanumerical code of various length and format indicating the hierarchical level of the entry, a plaintext descriptor ranging in scope from a few words to multiple sentences, and a binary changelog with the quirk that the actual change is indicated in the descriptor field by means of italics, or in some cases, added to the binary field itself.
3. `input/owcm_index` contains more than 10000 entries of entities that are classified according to `input/owcm_full`, using the same data fields. 

The main takeaway from this analysis is that the input data needs be cleaned. More precisely, on a conceptual level, OWCM as provided in `input/owcm_full` is a thesaurus (i.e., a controlled vocabulary with a binary relation on the vocabulary interpreted as semantic hierarchy). However, on the level of implementation, it is not even a controlled vocabulary since it lacks the usual specifications. For example, the provided data fields are undefined and sometimes used inconsistently; the plaintext descriptor is of very low granularity; the hierarchy between entries is not made explicit. This problem can be amended by converting `owcm_full` into a SKOS instance [4]. This approach ties in nicely with the Basel University Library's strategy of collecting and making available as many thesauri, vocabularies and ontologies as possible in one place at BARTOC Skosmos [5]. In addition, having a SKOS instance of OWCM provides a clear framework for reconciling OWCM with GND.

#### 3. OWCM SKOS converter

`converter.py` is a Python script to convert `input/owcm_full` into  a Skosmos [6] compliant JSON-LD called `output/owcm_skos`. The script is documented so I won't rehash the details here and instead focus on `output/owcm_skos`. `output/owcm_skos` has a preamble defining its namespace and a graph which consists of the OWCM concept scheme and all of its concepts. Let me describe some of the data fields of these concepts and explain how they relate to the data fields of `input/owcm_full` (i.e., code, descriptor, changelog):

1. `uri`: a URI of the form https://bartoc.org/ocwm/code intended to serve as its PID. By adding `output/owcm_skos` to BARTOC Skosmos, the URI will turn into a URL.
2. `prefLabel`: the part of the descriptor that names the concept (e.g., Taiwan).
3. `altLabel`: the part of the descriptor that used to name the concept (e.g., Formosa); not yet implemented.
4. `definition`: the part of the descriptor that defines the concept.
5. `historyNote`: a copy of the descriptor. 
6. `changeNote`: the change to the concept implemented by MKB as documented in changelog.
7. `broader`: the parent concept.
8. `narrower`: the child concept(s). 

In short, the code is used to provide each concept with a PID and to build the hierarchy of concepts; the descriptor is split into the data fields `prefLabel`, `altLabel`, `definition`; and changelog is used to build `changeNote`.

#### 4. Reconciling OWCM SKOS with GND

The GND provides a LOD API of its data that includes reconciliation for OpenRefine [7].  

#### 5. Outlook

#### 6. References  
[1] George P. Murdock (19XX)  
[2] https://ehrafworldcultures.yale.edu/ehrafe/   
[3] https://www.dnb.de/DE/Professionell/Standardisierung/GND/gnd_node.html  
[4] https://www.w3.org/TR/skos-reference/  
[5] https://bartoc-skosmos.unibas.ch   
[6] Suominen, O. et al. (2015): Publishing SKOS vocabularies with Skosmos. Manuscript submitted for review, June 2015.  
[7] http://lobid.org/gnd/reconcile

