#-------------------------------------------------------------------
# Merge Databases
#-------------------------------------------------------------------

import glob
import pandas as pd
import numpy as np
from master_functions import *


path =r'Step1_Output'

allFiles = glob.glob(path + "/*")

df = pd.DataFrame(columns = ['NSF',
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

# Append dataframes
list_ = []

for file_ in allFiles:
    frame = pd.read_csv(file_, sep = '|',
                        header = 0,
                        index_col = False,
                        na_filter = False)
    list_.append(frame)

df = pd.concat(list_)

# Export dataframe
df.to_csv(path_or_buf='Step2_Output/combination_part1',
          index = False,
          header = True,
          sep = '|')
