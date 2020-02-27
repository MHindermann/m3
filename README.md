## Reconciling a local OWC instance with GND
Maximilian Hindermann (https://orcid.org/0000-0002-9337-4655), University of Basel

####Introduction

The Outline of World Cultures (OWC) is an ontology for cultures created by George P. Murdock [1]. It has since been refined and updated in various ways, most prominently by Yale University’s HRAF division as the subscription database eHRAF World Cultures [1]. The Museum der Kulturen Basel (MKB), however, uses a distinct instance of OWC that reflects the museum’s collection history, for example by vastly enriching OWC’s ontology with respect to modern Papua New Guinea. In this paper, I will explore whether this local OWC instance (call it OWCM) can be reconciled with the Integrated Authority File (GND) [3] used by the Basel University Library (and all other Swiss German university libraries) for indexing. 

####OWCM input data
The OWCM data was supplied to me in form of three Excel files. In what follows, I will briefly describe the content and structure of each file:

1.	owcm_divisions contains the main geographical divisions (e.g., Asia) and their subdivisions (e.g., Korea). Each of these 250 entries has three data fields: a one or two-digit alphabetical code indicating the hierarchical level of the entry, a plaintext descriptor consisting of a few words, and a binary field indicating whether the entry was modified by the MKB.
2.	owcm_text contains further lower-level divisions and is a superset of owcm_divisions. We can hence ignore owcm_divisions from now on. Each of the roughly 3000 entries has again three data fields: an alphanumerical code of various length and format indicating the hierarchical level of the entry, a plaintext descriptor ranging in scope from a few words to multiple sentences, and a binary changelog with the quirk that the actual change is indicated in the descriptor field by means of italics, or in some cases, added to the binary field itself.
3.	owcm_index contains more than 10000 entries of entities that are classified according to owcm_text, using the same data fields. 

There are a couple of takeaways from this analysis. First, on a conceptual level, OWCM as provided in owcm_text is a thesaurus (i.e., a controlled vocabulary with a binary relation on the vocabulary interpreted as semantic hierarchy). However, on the level of implementation, it is not even a controlled vocabulary since it lacks the usual specifications (see [4]). For example, the provided data fields are undefined and sometimes used inconsistently, and especially the plaintext descriptor is of very low granularity. 

In order to amend this problem, 




####References
[1] George P. Murdock (19XX)  
[2] https://ehrafworldcultures.yale.edu/ehrafe/   
[3] https://www.dnb.de/DE/Professionell/Standardisierung/GND/gnd_node.html 
