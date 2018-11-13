# Modules

Here, we give a series of modules for processing each source database into the final crosswalk.

## Master Functions

This documents contains functions used several times during each of the processing steps.

## Step 1: Preprocessing

Each database is processed to fit the following format:

NSF | NSFUI | SF | SFUI | LF | LFUI | PLF | PLFUI | UMLS CUI | MetaMap CUI | Source | SFEUI | LFEUI | Prevalence

**NSF:** Normalized short form; defined as the short form converted to upper case with spaces and punctuation removed.

**NSFUI:** Normalized short form unique identifier.

**SF:** Short form; contains each individual short form as found in the source database.

**SFUI:** Short form unique identifier.

**LF:** Long form; contains each individual long form as found in the source database.

**LFUI:** Long form unique identifier.

**PLF:** Preferred long form; defined as the preferred long form for a given sense of a short form.

**PLFUI:** Preferred long form unique identifier.

**UMLS CUI:** The UMLS CUI as provided in the source database.

**MetaMap CUI:** If the UMLS CUI is not provided, MetaMap is used to map the each long form to the appropriate UMLS CUI, provided in this column.

**Source:** The source database.

**SFEUI:** Short form entry unique identifier; contains the entry unique identifier of the long form in the UMLS LRABR.

**LFEUI:** Long form entry unique identifier; contains the entry unique identifier of the long form in the UMLS LRABR.

**Prevalence:** Prevalence, frequency, or likelihood information for that particular original short form as given in the source database.

We defined the "Source", "NSF", "SF", and "LF" columns for each source database, as well as other columns as necessary for source transparency. 

We cleaned databases to improve their quality without loss of source information (See Step 2, Part 2: Quality Check).

## Step 2: Add Identifiers

### Part 1: Merge Databases

All the preprocessed databases become merged into one complete database.

### Part 2: Quality Check

We identified potential quality problems according to 6 quality heuristics:

**Quality Heuristic 1:** The last character in the long form is a punctuation mark or symbol in .,'%/#!$^&@?<>\*:;{}-=_`~()[]"

*(e.g. the long form "nitric oxide synthase;" should be "nitric oxide synthase")*

**Quality Heuristic 2:** The short form or long form contains formatting errors (repeat quotations, excess punctuation, typos).

*(e.g. the short form "..IVF" should be "IVF")*

**Quality Heuristic 3:** The row is an exact duplicate of another row.

**Quality Heuristic 4:** The short form is greater than 6 characters long.

**Quality Heuristic 5:** The long form is greater than 50 characters long.

**Quality Heuristic 6:** The alphabetic characters in the short form don't occur anywhere in the long form.

*(e.g. the short form "PRBC" occurring with the long form "packed #000066 blood cells", which should be "packed red blood cells")*

A medical student manually reviewed rows that our quality heuristics identified, and modified the databases within the preprocessing step (Step 1) according to the following 11 rules:

**Rule 1:** Remove explanations but not qualifiers.

*(e.g. an explanation such as "(this acronym is never spelled out)" is removed, but qualifiers such as "(gene)", "(syndrome)", or "(virus)" remain)*

**Rule 2:** Separate qualifiers from their short forms or long forms into a separate column called **Qualifiers**.

*(e.g. for the short form "ECHO" with the long form "enteric cytopathic human orphan (virus)", the new long form is "enteric cytopathic human orphan" and the qualifier is "virus")*

*(e.g. for the short form "AGES criteria", the new short form is "AGES" and the qualifier is "criteria")*

**Rule 3:** Remove short forms that are symbols, not abbreviations or acronyms.

*(e.g. the short forms "@" or "%" are removed)*

**Rule 4:** Remove formatting errors (repeat quotations, excess punctuation, typos).

*(e.g. the long form "nothing by moouth" becomes "nothing by mouth")*

**Rule 5:** Separate lines containing multiple short forms or long forms.

*(e.g. the short form "co or c/o" is separated into two lines, one for "co" and one for "c/o")*

**Rule 6:** Remove short forms that are words, not abbreviations or acronyms.

*(e.g. the short form "rhythm" with the long form "rhythm" is removed)*

**Rule 7:** Expand long forms containing acronyms.

*(e.g. the long form "bleo mtx vcr" becomes "bleomycin, methotrexate, vincristine")*

**Rule 8:** Clarify long forms missing information corresponding to the characters in the short form.

*(e.g. for the short form "APKD" with long form "adult polycystic disease", the new long form is "adult polycystic kidney disease")*

*(e.g. for the short form "nullip" with long form "never gave birth", the new long form is "nulliparous" and the qualifier is "never gave birth")*

**Rule 9:** Remove rows containing long forms with the explanations "not an abbreviation", "not an acronym", and "physician initials".

**Rule 10:** Replace "null" values with an empty string.

**Rule 11:** Remove rows that are exact duplicates of another row.

### Part 3: Assign NSFUI

Each normalized short form unique identifier is assigned.

### Part 4: Assign SFUI

Each original short form unique identifier is assigned.

### Part 5: Assign LFUI

Each long form unique identifier is assigned.

## Step 3: Map to UMLS CUIs

Each long form is mapped to one or more UMLS CUIs (concept unique identifiers) using MetaMap.
MetaMap is available at https://metamap.nlm.nih.gov/

## Step 4: Discover Semantic Groups

We used the UMLS CUIs and string similarity between long forms to identify semantic groups and assign PLFUI. Then, we assigned preferred long forms to each group.  

## Step 5: Output the crosswalk

**Files.txt:** File names and information

**ColumnNames.txt:** Column names and information

**Sources.txt:** Source names and information

**SourceInstances.txt:** One row for each atom

**SemanticGroups.txt:** One row for each semantic group

**SimpleMap.txt:** UMLS CUIs for preferred long forms

**Map.txt:** UMLS CUIs for all long forms

## Other files

### Master Functions

This file contains functions used several times during each of the steps.

### lvg_wrapper.py and metamap.py

MetaMap and lexical variant generation (lvg) are command line tools, so those files are python wrappers for the umls command line tools. metamap.py has functions to start and stop the metamap server, and run metamap on an input file. lvg_wrapper has a function to run umls lexical variant generation on an input file. Both rely on a local installation of the UMLS tools.
