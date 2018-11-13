#-------------------------------------------------------------------
# Step 1: Preprocessing
# UTHealth inventory
#-------------------------------------------------------------------

import pandas as pd
from master_functions import *

# Load database
db = pd.read_csv('../sources/uthealth/sense_distribution_448.txt',
                       sep = '\t',
                       header = None,
                       names = ['abr',
                                'long_form',
                                'frequency'],
                        na_filter = False,
                        index_col = False
                        )

# Generate output Data Frame
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



### Populate output Data Frame ###

# Normalized Short Form
out_db['NSF'] = db['abr'].apply(standard_sf)

# Prevalence
out_db['Prevalence'] = db['frequency']

# Source
out_db['Source'] = 'uthealth_sense_distribution'

# Short Form
out_db['SF'] = db['abr']

# Long Form
out_db['LF'] = db['long_form']

### Cleaning
out_db['LF'] = out_db['LF'].replace(to_replace="not an abbreviation (all of it is hemoglobin A1C)", value="hemoglobin A1C")
out_db['LF'] = out_db['LF'].replace(to_replace="cluster of differentiation 4 (but never spelled out...)", value="cluster of differentiation 4")
out_db['LF'] = out_db['LF'].replace(to_replace="ethanol (aka alcohol)", value="ethanol(alcohol)")
out_db['LF'] = out_db['LF'].replace(to_replace="roman numeral 4", value="roman numeral for the number 4")
out_db['LF'] = out_db['LF'].replace(to_replace="nothing by mouth", value="nothing by mouth (From Latin: 'Nil per os')")

# Remove rows
out_db = out_db[out_db['LF'].str.contains("typo") == False]
out_db = out_db[out_db['LF'].str.contains('exempli gratia') == False]
out_db = out_db[out_db['LF'].str.contains('id est') == False]
out_db = out_db[out_db['LF'].str.contains('not an acronym') == False]
out_db = out_db[out_db['LF'].str.contains('ii and xii are roman numerals') == False]
out_db = out_db[out_db['LF'].str.contains('not an abbreviation') == False]
out_db = out_db[out_db['LF'].str.contains('not an abbreviaion') == False]
out_db = out_db[out_db['LF'].str.contains('initial') == False]
out_db = out_db[out_db['LF'].str.contains('Initial') == False]
out_db = out_db[out_db['LF'].str.contains('means alert and oriented') == False]

# Complex replacements
for index, row in out_db.iterrows():
    if (row['SF'] == 'po') and (row['LF'] == "by mouth"):
        out_db.set_value(index, 'LF', "by mouth (From Latin: per os)")
    if (row['SF'] == 'pos') and (row['LF'] == "by mouth"):
        out_db.set_value(index, 'LF', "by mouth (From Latin: per os)")
    if (row['SF'] == 'v') and (row['LF'] == "5"):
        out_db.set_value(index, 'LF', "roman numeral for the number 5")
    if (row['SF'] == 'vi') and (row['LF'] == "6"):
        out_db.set_value(index, 'LF', "roman numeral for the number 6")

### Save to a file ###
out_db.to_csv('Step1_Output/preprocess_uthealth_sense_distribution',
              index = False,
              header = True,
              sep = '|')
