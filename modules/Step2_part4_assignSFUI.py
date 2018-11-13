#-------------------------------------------------------------------
# Assign SFUI
#-------------------------------------------------------------------

import glob
import pandas as pd
import numpy as np
from master_functions import *

# Global variables
verbose = True

# Read in database
df = pd.read_csv('Step2_Output/combination_part3',
                 sep = '|',
                 header = 0,
                 index_col = False,
                 na_filter = False)

# Sort
df = df.sort_values(by=['SF'])

# Reindex dataframe
df = df.reset_index()

# Assign SFUIs
if verbose: print "Assigning SFUIs... this might take a minute or two"
assignment = 1
for index, row in df.iterrows():
    if index == 0:
        df.set_value(index, 'SFUI', assignment)
    elif df.loc[index, 'SF'] == df.loc[index-1, 'SF']:
        df.set_value(index, 'SFUI', assignment)
    else:
        assignment += 1
        df.set_value(index, 'SFUI', assignment)

# Add leading zeros and letter
df["SFUI"] = "S" + (df.SFUI.map("{:06}".format))

# Export dataframe
df.to_csv(path_or_buf='Step2_Output/combination_part4',
          columns=['NSF', 'NSFUI', 'SF', 'SFUI', 'LF', 'LFUI', 'PLF', 'PLFUI',
                   'UMLS CUI', 'MetaMap CUI', 'Source', 'SFEUI', 'LFEUI', 'Prevalence'],
          index = False,
          header = True,
          sep = '|')