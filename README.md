## Reconciling a local OWC instance with GND
Maximilian Hindermann (https://orcid.org/0000-0002-9337-4655), University of Basel

####Introduction

The Outline of World Cultures (OWC) is an ontology for cultures created by George P. Murdock [1]. It has since been refined and updated in various ways, most prominently by Yale University’s HRAF division as the subscription database eHRAF World Cultures [1]. The Museum der Kulturen Basel (MKB), however, uses a distinct instance of OWC that reflects the museum’s collection history, for example by vastly enriching OWC’s ontology with respect to modern Papua New Guinea. In this paper, I will explore whether this local OWC instance (call it OWCM) can be reconciled with the Integrated Authority File (GND) [3] used by the Basel University Library (and all other Swiss German university libraries) for indexing. 

####OWCM input data
The data was handed to me in form of three Excel files which shall be described in what follows:
- owcm_text provides three data fields for each of its ca. 3000 entries:
    - Code: alphanumeric characters with spaces and dots; reflects the hierarchical level of the entry.  
    - Description: plaintext explaining the code field. The scope ranges from single words to multiple sentences.
    - Changelog: binary marker to indicate that changes were made by the MKB. If there was a change, it is either identified with italics in the description field or in some cases added to the binary field itself.
- owcm_index is similar to owcm_text, but the description fields are limited in scope. With respect to the description fields, there is a one-to-many relation from owcm_text to owcm_index.
- owcm_divisions is a subset of owcm_text. 

To summarize, the input data is quite messy due to the low granularity (and sometimes inconsistent use) of the data fields. In order to clean the data, 



####References
[1] George P. Murdock (19XX)  
[2] https://ehrafworldcultures.yale.edu/ehrafe/   
[3] https://www.dnb.de/DE/Professionell/Standardisierung/GND/gnd_node.html 
