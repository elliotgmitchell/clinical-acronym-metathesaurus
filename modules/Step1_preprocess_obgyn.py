#-------------------------------------------------------------------
# Step 1: Preprocessing
# OBGYN Database
#-------------------------------------------------------------------

import pandas as pd
from master_functions import *

out_db = pd.DataFrame(columns = ['NSF',
                                 'NSFUI',
                                 'SF',
                                 'SFUI',
                                 'LF',
                                 'LFUI',
                                 'PLF',
                                 'PLFUI',
                                 'UMLS CUI',
                                 'MetaMap CUI',
                                 'Source',
                                 'SFEUI',
                                 'LFEUI',
                                 'Prevalence'])

file = open('../sources/obgyn/obgyn.txt', 'r+')

for line in file:
    var1, var2 = line.split(" ", 1)
    var2 = var2.strip()
    out_db = out_db.append({'SF': var1, 'LF': var2}, ignore_index=True)

# Add normalized short form
out_db['NSF'] = out_db['SF'].apply(standard_sf)

# Add source
out_db['Source'] = "columbia"

# Export file
out_db.to_csv( path_or_buf='Step1_Output/preprocess_obgyn',
               index = False,
               header = True,
               sep = '|')

file.close()