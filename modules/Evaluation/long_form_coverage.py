'''

long form coverage

'''

import pandas as pd

# Load Source Instances
mae = pd.read_csv(r"../../Clinical Abbreviation and Acronym Crosswalk/SourceInstances.txt",
                  sep = '|',
                  na_filter = False)

mae_LF = mae['LF'].tolist()

# Load Annotation Key
key = pd.read_csv(r"../../modules (sense disambiguation)/6_Evaluation/Development of the Gold Standard/"
                  r"Annotation Key.txt",
                  sep = '|',
                  na_filter = False)

key_Annotation = key['Annotation']

# Macroaverage
count = 0
for key in key_Annotation:
    print key
    if key in mae_LF:
        count += 1


