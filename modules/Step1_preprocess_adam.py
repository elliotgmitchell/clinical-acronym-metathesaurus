#-------------------------------------------------------------------
# Step 1: Preprocessing
# ADAM Database
#-------------------------------------------------------------------

import pandas as pd
from master_functions import *
from tqdm import tqdm

# Load ADAM database
adam_db = pd.read_csv('../sources/adam/adam_database',
                       sep = '\t',
                       skiprows = 38,
                       header = None,
                       names = ['pref_abr',
                                'alt_abr',
                                'long_forms',
                                'score',
                                'count'],
                        na_filter = False,
                        # dtype = str,
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


# Return cell content without count or prevalence info
def trim_adam_cell(c):
    return c.split(':')[0]


### Populate output Data Frame ###

# Normalized Short Form
out_db['NSF'] = adam_db['pref_abr'].apply(standard_sf)

# Prevalence
out_db['Prevalence'] = adam_db['score']

# Source
out_db['Source'] = 'ADAM'

# Short Form
out_db['SF'] = adam_db['alt_abr']

# Long Form
out_db['LF'] = adam_db['long_forms']

# Expand and trim Short Form
print "expanding short forms"
out_db = expand_col(out_db, 'SF')
print 'trimming short forms'
out_db['SF'] = out_db['SF'].apply(trim_adam_cell)
out_db = out_db.reset_index()

# Expand and trim Long Form
print "expanding long forms"
out_db = expand_col(out_db, 'LF')
print 'trimming long forms'
out_db['LF'] = out_db['LF'].apply(trim_adam_cell)

### Cleaning
out_db['LF'] = out_db['LF'].replace(to_replace="'diffuse noxious inhibitory controls'", value="diffuse noxious inhibitory controls")
out_db['LF'] = out_db['LF'].replace(to_replace="'do not resuscitate'", value="do not resuscitate")
out_db['LF'] = out_db['LF'].replace(to_replace="technetium-99m-", value="technetium-99m")
out_db['LF'] = out_db['LF'].replace(to_replace="pokeweed mitogen-", value="pokeweed mitogen")
out_db['LF'] = out_db['LF'].replace(to_replace="American Society of Anesthesiologists'", value="American Society of Anesthesiologists")
out_db['LF'] = out_db['LF'].replace(to_replace="Joint Commission on Accreditation of Healthcare Organizations'", value="Joint Commission on Accreditation of Healthcare Organizations")
out_db['LF'] = out_db['LF'].replace(to_replace="general practitioners'", value="general practitioners")

# Remove rows
out_db = out_db[(out_db['LF'].str.contains('diffusion-$') == False)]
out_db = out_db[(out_db['LF'].str.contains('CD4-CD8-$') == False)]
out_db = out_db[(out_db['LF'].str.contains('acetylcholine-$') == False)]
out_db = out_db[(out_db['LF'].str.contains('Epstein-Barr virus-$') == False)]
out_db = out_db[(out_db['LF'].str.contains('Epstein Barr virus-$') == False)]
out_db = out_db[(out_db['LF'].str.contains('endothelin-A-$') == False)]
out_db = out_db[(out_db['LF'].str.contains('interleukin-$') == False)]
out_db = out_db[(out_db['LF'].str.contains('lipopolysaccharide-$') == False)]
out_db = out_db[(out_db['LF'].str.contains('neuropeptide Y-$') == False)]
out_db = out_db[(out_db['LF'].str.contains('^3\'$') == False)]
out_db = out_db[(out_db['LF'].str.contains('^adenosine 3\'$') == False)]
out_db = out_db[(out_db['LF'].str.contains('nurse practitioners\'$') == False) & (out_db['SF'].str.contains('NPs$') == False)]
out_db = out_db[(out_db['LF'].str.contains("penicillin-binding protein 2\'") == False)]

### Save to a file ###
print "saving to file"
out_db.to_csv('Step1_Output/preprocess_adam',
              index = False,
              header = True,
              sep = '|')

# Hacky handling to get rid of index column: re-load and re-save
db = pd.read_csv('Step1_Output/preprocess_adam',
                 na_filter = False,
                 sep = '|')
del db['index']
# Change column order
db = db[['NSF',
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
         'Prevalence']]

db.to_csv('Step1_Output/preprocess_adam',
            index = False,
            sep = '|')
