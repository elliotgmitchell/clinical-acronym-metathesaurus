#-------------------------------------------------------------------
# Step 1: Preprocessing
# wikipedia clinical trials database
#-------------------------------------------------------------------

import pandas as pd
from master_functions import *

# Load database
db = pd.read_csv('../sources/wikipedia/wikipedia_clin_trials.txt',
                 sep = ':',
                 na_filter = False,
                 header=None,
                 index_col=False,
                 names=['SF',
                        'LF'])

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

### Clean ###

# Strip leading and trailing whitespace
db['LF'] = db['LF'].str.strip()
db['SF'] = db['SF'].str.strip()

# Remove commas and quotes
db['SF'] = db['SF'].str.replace('"','')
db['LF'] = db['LF'].str.replace('"','')
db['LF'] = db['LF'].str.replace(',','')

### Populate output Data Frame ###

# Normalized Short Form
out_db['NSF'] = db['SF'].apply(standard_sf)

# Source
out_db['Source'] = 'wikipedia_ct'

# Short Form
out_db['SF'] = db['SF']

# Long Form
out_db['LF'] = db['LF']

### Cleaning ###

# Replace rows
out_db['LF'] = out_db['LF'].replace(to_replace="ACCORD Study Group", value="Action to Control Cardiovascular Risk in Diabetes (ACCORD) Study Group")
out_db['LF'] = out_db['LF'].replace(to_replace="Adjuvant Tamoxifen", value="Adjuvant Tamoxifen Longer Against Shorter")
out_db['NSF'] = out_db['NSF'].replace(to_replace="ORIGINN3FATTYACIDS", value="ORIGIN")
out_db['SF'] = out_db['SF'].replace(to_replace="ORIGIN n-3 Fatty Acids", value="ORIGIN")
out_db['LF'] = out_db['LF'].replace(to_replace="Investigators in the outcome Reduction with an Initial Glargine Intervention", value="Outcome Reduction With Initial Glargine Intervention")

# Note hard-coded locations due to replacement difficulties with \
out_db.loc[108]['LF'] = "Behandel-Strategeieen (treatment strategies)"
out_db.loc[124]['LF'] = "Iniciativa Profilaxis Pre Exposicion (Preexposure Prophylaxis Initiative)"

### Save to a file ###
out_db.to_csv('Step1_Output/preprocess_wikipedia_ct',
              index = False,
              header = True,
              sep = '|')
