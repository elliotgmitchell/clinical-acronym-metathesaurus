#-------------------------------------------------------------------
# Step 1: Preprocessing
# UMLS Database
#-------------------------------------------------------------------

import pandas as pd
from master_functions import *

umls_db = pd.read_csv('../sources/umls/LRABR',
                       sep = '|',
                       header = None,
                       index_col = False,
                       na_filter = False,
                       names = ['SF_EUI',
                                'SF',
                                'type',
                                'LF_EUI',
                                'LF'])

out_umls_db = pd.DataFrame(columns = ['NSF',
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

# Add short form
out_umls_db['SF'] = umls_db['SF']

# Add long form
out_umls_db['LF'] = umls_db['LF']

# Add SFEUI
out_umls_db['SFEUI'] = umls_db['SF_EUI']

# Add LFEUI
out_umls_db['LFEUI'] = umls_db['LF_EUI']

# Add source
out_umls_db['Source'] = "UMLS"

# Add NSF
out_umls_db['NSF'] = umls_db['SF'].apply(standard_sf)

### Cleaning
out_umls_db['LF'] = out_umls_db['LF'].replace(to_replace="zinc finger protein, subfamily 1A, 2,", value="zinc finger protein, subfamily 1A, 2")
out_umls_db['LF'] = out_umls_db['LF'].replace(to_replace="amplified-fragment-length polymorphis-", value="amplified-fragment-length polymorphism")

# Export file
out_umls_db.to_csv( path_or_buf='Step1_Output/preprocess_umls',
                    index = False,
                    header = True,
                    sep = '|')
