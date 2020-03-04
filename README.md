## Reconciling a local OWC instance with GND
Maximilian Hindermann, https://orcid.org/0000-0002-9337-4655, University of Basel  
_CC BY 4.0_

### 0. Preamble

This document is best viewed on GitHub at https://github.com/MHindermann/m3. 

### 1. Introduction

The Outline of World Cultures (OWC) is an ontology for cultures created by George P. Murdock [1]. It has since been refined and updated in various ways, most prominently by Yale University’s HRAF division as the subscription database eHRAF World Cultures [2]. The Museum der Kulturen Basel (MKB), however, uses a distinct instance of OWC that reflects the museum’s collection history, for example by vastly enriching OWC’s ontology with respect to modern Papua New Guinea. In this paper, I will explore whether this local OWC instance (call it OWCM) can be reconciled with the Integrated Authority File (GND) [3] used by the Basel University Library (and all other Swiss German university libraries) for indexing. 

### 2. OWCM input data
The OWCM data was supplied to me in form of three XLS(X) files. In what follows, I will briefly describe the content and structure of each file:

1. `input/owcm_short` contains the main geographical divisions (e.g., Asia) and their subdivisions (e.g., Korea). Each of these 250 entries has three data fields: a one or two-digit alphabetical code indicating the hierarchical level of the entry, a plaintext descriptor consisting of a few words, and a binary field indicating whether the entry was modified by the MKB.
2. `input/owcm_full` contains further lower-level divisions and is a superset of `input/owcm_short`. We can hence ignore `input/owcm_short` from now on. Each of the roughly 3000 entries has again three data fields: an alphanumerical code of various length and format indicating the hierarchical level of the entry, a plaintext descriptor ranging in scope from a few words to multiple sentences, and a binary changelog with the quirk that the actual change is indicated in the descriptor field by means of italics, or in some cases, added to the binary field itself.
3. `input/owcm_index` contains more than 10000 entries of entities that are classified according to `input/owcm_full`, using the same data fields. 

The main takeaway from this analysis is that the input data needs be cleaned. More precisely, on a conceptual level, OWCM as provided in `input/owcm_full` is a thesaurus (i.e., a controlled vocabulary with a binary relation on the vocabulary interpreted as semantic hierarchy). However, on the level of implementation, it is not even a controlled vocabulary since it lacks the usual specifications. For example, the provided data fields are undefined and sometimes used inconsistently; the plaintext descriptor is of very low granularity; the hierarchy between entries is not made explicit. This problem can be amended by converting `input/owcm_full` into a SKOS instance [4]. This approach ties in nicely with the Basel University Library's strategy of collecting and making available as many thesauri, vocabularies and ontologies as possible in one place at BARTOC Skosmos [5]. In addition, having a SKOS instance of OWCM provides a clear framework for reconciling OWCM with GND.

### 3. OWCM SKOS converter

`converter.py` is a Python script to convert `input/owcm_full` into  a Skosmos [6] compliant JSON-LD called `skos/owcm_skos`. The script is documented so I won't rehash the details here and instead focus on `skos/owcm_skos`. `skos/owcm_skos` has a preamble defining its namespace and a graph which consists of the OWCM concept scheme and all of its concepts. Let me describe some of the data fields of these concepts and explain how they relate to the data fields of `input/owcm_full` (i.e., code, descriptor, changelog):

1. `uri`: a URI of the form https://bartoc.org/ocwm/code intended to serve as its PID. By adding `skos/owcm_skos` to BARTOC Skosmos, the URI will turn into a URL.
2. `prefLabel`: the part of the descriptor that names the concept (e.g., _Taiwan_).
3. `altLabel`: the part of the descriptor that used to name the concept (e.g., _Formosa_); not yet implemented.
4. `definition`: the part of the descriptor that defines the concept.
5. `historyNote`: a copy of the descriptor. 
6. `changeNote`: the change to the concept implemented by MKB as documented in changelog.
7. `broader`: the parent concept.
8. `narrower`: the child concept(s). 

In short, the code is used to provide each concept with a PID and to build the hierarchy of concepts; the descriptor is split into the data fields `prefLabel`, `altLabel`, `definition`; and changelog is used to build `changeNote`.

### 4. Reconciling OWCM SKOS with GND

The GND provides a LOD API of its data that includes reconciliation for OpenRefine [7]. Reconciliation means that a OWCM concept from `skos/owcm_skos` is matched to a GND entry (see [8] for details on the matching process). A (partial) mapping between OWCM and GND based on these matches is deemed valuable since it would allow for an easier integration of the MKB's holdings into the catalogues (respectively discovery systems to employ New Librarian Speak) of other institutions. In what follows I will discuss naive and more informed reconciliation strategies and their respective challenges. The result of each reconciliation test is provided as CSV or XLSX as `reconciled/owcm_gnd_naiveORinformed` and can be reproduced by calling `reconciled/owcm_naiveORinformed_history` on `skos/owcm_skos` in OpenRefine. 

#### 4.1 Naive reconciliation

`reconciled/owcm_gnd_naive` is a reconciliation based on the single data field `prefLabel` without any restrictions to a GND datatype. The result has 1443 or 43% automatic (i.e., high confidence) matches. (Note that naive reconciliation with Wikidata results in less than 1% automatic matches.) However, even a cursory glance reveals quite a few (kinds of) false positives:

- _Minor Asiatic Colonies_ is matched to GND's _Minoer_, the ancient Minoan civilization.
- 28 concepts that include the prefix _modern_ (e.g., _Modern Canada_) are matched to _Suite en style modern_ by composer Joseph Achron.
-  _Maritime Arabs_ is matched to a 16th century person called _Arabs Sorsanus_.

 Some of these errors might be avoided by excluding specific GND datatypes such as works of music or literature, or persons. Other errors are due to fact that OWCM is in English and the GND is in German and lacks English translations for many of its entries.
 
#### 4.2 Informed reconciliation

`reconciled/owcm_gnd_informed` is still based on the single data field `prefLabel` but limited to the GND datatype `PlaceOrGeographicName` [9]. Recall is lower as compared to `reconciled/owcm_gnd_naive`, but precision is increased.

### 5. Outlook

So far I have provided the basis of a reconciliation of OWCM SKOS with GND. However, implementing this reconciliation requires further work. There are many errors and any proposed mapping would have to be checked by an expert in the field (I for one lack the domain specific knowledge in many cases). So I propose the following road map to move forwards: 

1. Compile a set of test concepts a with the help of an ethnographer to be used as benchmark.
2. Systematize the encountered errors.
3. Get a deeper understanding of the OpenRefine matching scores and check whether they can be adapted to the needs at hand.
4. See whether triangulation can be used to improve matching quality by employing Cocoda [10].


### 6. References  
[1] Murdock, George P. (1969): _Outline of World Cultures_, 3rd revised edition. New Haven, Conn.: HRAF Press.  
[2] https://ehrafworldcultures.yale.edu/ehrafe/   
[3] https://www.dnb.de/DE/Professionell/Standardisierung/GND/gnd_node.html  
[4] https://www.w3.org/TR/skos-reference/  
[5] https://bartoc-skosmos.unibas.ch   
[6] Suominen, O. et al. (2015): _Publishing SKOS vocabularies with Skosmos._ Manuscript submitted for review.  
[7] http://lobid.org/gnd/reconcile  
[8] https://github.com/OpenRefine/OpenRefine/wiki/Reconciliation  
[9] https://d-nb.info/standards/elementset/gnd   
[10] https://coli-conc.gbv.de/cocoda/  

