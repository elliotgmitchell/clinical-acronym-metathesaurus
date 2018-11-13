#-------------------------------------------------------------------
# Assign LFUI
#-------------------------------------------------------------------

import glob
import pandas as pd
import numpy as np
from master_functions import *

# Global variables
verbose = True

# Read in database
df = pd.read_csv('Step2_Output/combination_part4',
                 sep = '|',
                 header = 0,
                 index_col = False,
                 na_filter = False)

# Sort
df = df.sort_values(by=['LF'])

# Reindex dataframe
df = df.reset_index()

# Assign LFUIs
if verbose: print "Assigning LFUIs... this might take a minute or two"
assignment = 1
for index, row in df.iterrows():
    if index == 0:
        df.set_value(index, 'LFUI', assignment)
    elif df.loc[index, 'LF'] == df.loc[index-1, 'LF']:
        df.set_value(index, 'LFUI', assignment)
    else:
        assignment += 1
        df.set_value(index, 'LFUI', assignment)

# Add leading zeros and letter
df["LFUI"] = "L" + (df.LFUI.map("{:06}".format))

# Export dataframe
df.to_csv(path_or_buf='Step2_Output/combination_part5',
          columns=['NSF', 'NSFUI', 'SF', 'SFUI', 'LF', 'LFUI', 'PLF', 'PLFUI',
                   'UMLS CUI', 'MetaMap CUI', 'Source', 'SFEUI', 'LFEUI', 'Prevalence'],
          index = False,
          header = True,
          sep = '|')
