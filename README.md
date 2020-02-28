## Reconciling a local OWC instance with GND
Maximilian Hindermann (https://orcid.org/0000-0002-9337-4655), University of Basel

#### 1. Introduction

The Outline of World Cultures (OWC) is an ontology for cultures created by George P. Murdock [1]. It has since been refined and updated in various ways, most prominently by Yale University’s HRAF division as the subscription database eHRAF World Cultures [2]. The Museum der Kulturen Basel (MKB), however, uses a distinct instance of OWC that reflects the museum’s collection history, for example by vastly enriching OWC’s ontology with respect to modern Papua New Guinea. In this paper, I will explore whether this local OWC instance (call it OWCM) can be reconciled with the Integrated Authority File (GND) [3] used by the Basel University Library (and all other Swiss German university libraries) for indexing. 

#### 2. OWCM input data
The OWCM data was supplied to me in form of three Excel files. In what follows, I will briefly describe the content and structure of each file:

1. `input/owcm_short` contains the main geographical divisions (e.g., Asia) and their subdivisions (e.g., Korea). Each of these 250 entries has three data fields: a one or two-digit alphabetical code indicating the hierarchical level of the entry, a plaintext descriptor consisting of a few words, and a binary field indicating whether the entry was modified by the MKB.
2. `input/owcm_full` contains further lower-level divisions and is a superset of `input/owcm_short`. We can hence ignore `input/owcm_short` from now on. Each of the roughly 3000 entries has again three data fields: an alphanumerical code of various length and format indicating the hierarchical level of the entry, a plaintext descriptor ranging in scope from a few words to multiple sentences, and a binary changelog with the quirk that the actual change is indicated in the descriptor field by means of italics, or in some cases, added to the binary field itself.
3. `input/owcm_index` contains more than 10000 entries of entities that are classified according to `input/owcm_full`, using the same data fields. 

The main takeaway from this analysis is that the input data needs be cleaned. More precisely, on a conceptual level, OWCM as provided in `input/owcm_full` is a thesaurus (i.e., a controlled vocabulary with a binary relation on the vocabulary interpreted as semantic hierarchy). However, on the level of implementation, it is not even a controlled vocabulary since it lacks the usual specifications (see [4]). For example, the provided data fields are undefined and sometimes used inconsistently; the plaintext descriptor is of very low granularity; the hierarchy between entries is not made explicit. This problem can be amended by converting owcm_full into a SKOS instance [5]. This approach ties in nicely with the Basel University Library's strategy of collecting and making available as many thesauri, vocabularies and ontologies as possible in one place at BARTOC Skosmos [6]. In addition, having a SKOS instance of OWCM provides a clear framework for reconciling OWCM with GND.

#### 3. OWCM to SKOS converter

`converter.py` is a Python script to convert `input/owcm_full` to  a Skosmos compliant JSON-LD called `output/owcm_skos.json`.  

#### 4. Outlook

#### 5. References  
[1] George P. Murdock (19XX)  
[2] https://ehrafworldcultures.yale.edu/ehrafe/   
[3] https://www.dnb.de/DE/Professionell/Standardisierung/GND/gnd_node.html  
[4]  
[5] https://www.w3.org/TR/skos-reference/  
[6] https://bartoc-skosmos.unibas.ch   

