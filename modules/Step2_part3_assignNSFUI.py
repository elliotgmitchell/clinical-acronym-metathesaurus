#-------------------------------------------------------------------
# Assign NSFUI
#-------------------------------------------------------------------

import glob
import pandas as pd
import numpy as np
from master_functions import *

# Global variables
verbose = True

# Read in database
df = pd.read_csv('Step2_Output/combination_part2',
                 sep = '|',
                 header = 0,
                 index_col = False,
                 na_filter = False,
                 dtype=object)

# Sort
df = df.sort_values(by='NSF')

# Reindex dataframe
df = df.reset_index()

# Assign NSFUIs
if verbose: print "Assigning NSFUIs... this might take a minute or two"
assignment = 1
for index, row in df.iterrows():
    if index == 0:
        df.set_value(index, 'NSFUI', assignment)
    elif df.loc[index, 'NSF'] == df.loc[index-1, 'NSF']:
        df.set_value(index, 'NSFUI', assignment)
    else:
        assignment += 1
        df.set_value(index, 'NSFUI', assignment)

# Add leading zeros and letter
df["NSFUI"] = "N" + (df.NSFUI.map("{:06}".format))

# Export dataframe
df.to_csv(path_or_buf='Step2_Output/combination_part3',
          columns=['NSF', 'NSFUI', 'SF', 'SFUI', 'LF', 'LFUI', 'PLF', 'PLFUI',
                   'UMLS CUI', 'MetaMap CUI', 'Source', 'SFEUI', 'LFEUI', 'Prevalence'],
          index = False,
          header = True,
          sep = '|')
