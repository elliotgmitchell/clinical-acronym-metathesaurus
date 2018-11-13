#-------------------------------------------------------------------
# Quality Check
#-------------------------------------------------------------------

import glob
import pandas as pd
import numpy as np
from master_functions import *
import re

# Global variables
verbose = True
exceptions1 = 60
exceptions2 = 0
exceptions3 = 0
exceptions4 = 68
exceptions5 = 44
exceptions6 = 472

# Convenience setting for printing pandas data frames
pd.set_option('display.width', 1000)

# Read in database
df = pd.read_csv('Step2_Output/combination_part1',
                 sep = '|',
                 header = 0,
                 index_col = False,
                 na_filter = False,
                 dtype = object)

# Sort
df = df.sort_values(by=['Source', 'NSF'])

# Reindex dataframe
df = df.reset_index()

# Remove index column
del df['index']

###########################################
### Manual Cleaning Based on Heuristics ###
###########################################

if verbose: print "Cleaning data ..."

# Remove duplicate rows
df = df[df.duplicated() == False]

# Move info in parentheses to another column
df['Qualifier'] = ''
for index, row in df.iterrows():
    if (row['Source'] != "UMLS") & (row['Source'] != "ADAM") & (row['Source'] != "wikipedia_ct"):
        var = re.search('.*\)$', row['LF'])
        if var:
            df.set_value(index, 'Qualifier', re.search('\(([^)]+)', row['LF']).group(1))
            df.set_value(index, 'LF', re.sub("[\(].*?[\)]", "", row['LF']).strip())

###########################################
### Identify Potential Quality Problems ###
###########################################

# May exclude UMLS and ADAM from heuristic check iff check returns many chemicals
if verbose: print "Checking all 6 heuristics ..."

### Heuristic 1: Contains punctuation marks or symbols at end
# Excluded + due to use in ions
check = df[df['LF'].str.contains('.*\.$') == True]
check = check.append(df[df['LF'].str.contains('.*,$') == True])
check = check.append(df[df['LF'].str.contains('.*%$') == True])
check = check.append(df[df['LF'].str.contains('.*\/$') == True])
check = check.append(df[df['LF'].str.contains('.*#$') == True])
check = check.append(df[df['LF'].str.contains('.*!$') == True])
check = check.append(df[df['LF'].str.contains('.*\$$') == True])
check = check.append(df[df['LF'].str.contains('.*\^$') == True])
check = check.append(df[df['LF'].str.contains('.*&$') == True])
check = check.append(df[df['LF'].str.contains('.*@$') == True])
check = check.append(df[df['LF'].str.contains('.*\?$') == True])
check = check.append(df[df['LF'].str.contains('.*<$') == True])
check = check.append(df[df['LF'].str.contains('.*>$') == True])
check = check.append(df[df['LF'].str.contains('.*\*$') == True])
check = check.append(df[df['LF'].str.contains('.*:$') == True])
check = check.append(df[df['LF'].str.contains('.*;$') == True])
check = check.append(df[df['LF'].str.contains('.*{$') == True])
check = check.append(df[df['LF'].str.contains('.*}$') == True])
check = check.append(df[df['LF'].str.contains('.*=$') == True])
check = check.append(df[df['LF'].str.contains('.*\-$') == True])
check = check.append(df[df['LF'].str.contains('.*_$') == True])
check = check.append(df[df['LF'].str.contains('.*`$') == True])
check = check.append(df[df['LF'].str.contains('.*~$') == True])
check = check.append(df[df['LF'].str.contains('.*\($') == True])
check = check.append(df[(df['LF'].str.contains('.*\)$') == True) & (df['Source'] != "UMLS") & (df['Source'] != "ADAM")])
check = check.append(df[df['LF'].str.contains('.*\[$') == True])
check = check.append(df[df['LF'].str.contains('.*\]$') == True])
check = check.append(df[df['LF'].str.contains('.*\"$') == True])
check = check.append(df[df['LF'].str.contains('.*\'$') == True])

if verbose:
    if check.shape[0] <= exceptions1:
        print "\nHeuristic Check #1 (Punctuation): CLEARED!"
    else:
        print "\nHeuristic Check #1 (Punctuation): NOT CLEARED \nReview {} terms in Step2_Output/check_heuristic1".format(check.shape[0])

# Export dataframe
check.to_csv(path_or_buf='Step2_Output/check_heuristic1',
             columns=['NSF', 'NSFUI', 'SF', 'SFUI', 'LF', 'LFUI', 'Qualifier', 'PLF', 'PLFUI',
                      'UMLS CUI', 'MetaMap CUI', 'Source', 'SFEUI', 'LFEUI', 'Prevalence'],
             index=False,
             header=True,
             sep='|')

### Heuristic 2: Contains formatting errors
check = df[(df['LF'].str.contains("\"\"") == True) & (df['Source'] != "ADAM") & (df['Source'] != "UMLS")]
check = check.append(df[(df['LF'].str.contains("\'\'") == True) & (df['Source'] != "ADAM") & (df['Source'] != "UMLS")])
check = check.append(df[(df['SF'].str.contains("^\.") == True) & (df['Source'] == "vanderbilt_clinic_notes")])
check = check.append(df[(df['SF'].str.contains("^\.") == True) & (df['Source'] == "vanderbilt_discharge_sums")])

if verbose:
    if check.shape[0] <= exceptions2:
        print "\nHeuristic Check #2 (Formatting Errors): CLEARED!"
    else:
        print "\nHeuristic Check #2 (Formatting Errors): NOT CLEARED \nReview {} terms in Step2_Output/check_heuristic2".format(check.shape[0])

# Export dataframe
check.to_csv(path_or_buf='Step2_Output/check_heuristic2',
             columns=['NSF', 'NSFUI', 'SF', 'SFUI', 'LF', 'LFUI', 'Qualifier', 'PLF', 'PLFUI',
                      'UMLS CUI', 'MetaMap CUI', 'Source', 'SFEUI', 'LFEUI', 'Prevalence'],
             index=False,
             header=True,
             sep='|')

### Heuristic 3: Duplicate rows
check = df[df.duplicated(keep=False) == True]

if verbose:
    if check.shape[0] <= exceptions3:
        print "\nHeuristic Check #3 (Duplicate Rows): CLEARED!"
    else:
        print "\nHeuristic Check #3 (Duplicate Rows): NOT CLEARED \nReview {} terms in Step2_Output/check_heuristic3".format(check.shape[0])

# Export dataframe
check.to_csv(path_or_buf='Step2_Output/check_heuristic3',
             columns=['NSF', 'NSFUI', 'SF', 'SFUI', 'LF', 'LFUI', 'Qualifier', 'PLF', 'PLFUI',
                      'UMLS CUI', 'MetaMap CUI', 'Source', 'SFEUI', 'LFEUI', 'Prevalence'],
             index=False,
             header=True,
             sep='|')

### Heuristic 4: SF too long
check = df[(df['SF'].str.len() > 6) & (df['Source'] != "ADAM") & (df['Source'] != "UMLS")
           & (df['Source'] != "berman") & (df['Source'] != "wikipedia_ct")]

if verbose:
    if check.shape[0] <= exceptions4:
        print "\nHeuristic Check #4 (Long SF): CLEARED!"
    else:
        print "\nHeuristic Check #4 (Long SF): NOT CLEARED \nReview {} terms in Step2_Output/check_heuristic4".format(check.shape[0])

# Export dataframe
check.to_csv(path_or_buf='Step2_Output/check_heuristic4',
             columns=['NSF', 'NSFUI', 'SF', 'SFUI', 'LF', 'LFUI', 'Qualifier', 'PLF', 'PLFUI',
                      'UMLS CUI', 'MetaMap CUI', 'Source', 'SFEUI', 'LFEUI', 'Prevalence'],
             index=False,
             header=True,
             sep='|')

### Heuristic 5: LF is too long
check = df[(df['LF'].str.len() > 50) & (df['Source'] != "ADAM") & (df['Source'] != "UMLS")
           & (df['Source'] != "berman") & (df['Source'] != "wikipedia_ct")]

if verbose:
    if check.shape[0] <= exceptions5:
        print "\nHeuristic Check #5 (Long LF): CLEARED!"
    else:
        print "\nHeuristic Check #5 (Long LF): NOT CLEARED \nReview {} terms in Step2_Output/check_heuristic5".format(check.shape[0])

# Export dataframe
check.to_csv(path_or_buf='Step2_Output/check_heuristic5',
             columns=['NSF', 'NSFUI', 'SF', 'SFUI', 'LF', 'LFUI', 'Qualifier', 'PLF', 'PLFUI',
                      'UMLS CUI', 'MetaMap CUI', 'Source', 'SFEUI', 'LFEUI', 'Prevalence'],
             index=False,
             header=True,
             sep='|')

### Heuristic 6: Letters in SF not found in LF
temp = df.apply(lambda x: x.astype(str).str.lower())
temp['boo'] = False
for index, row in temp.iterrows():
    a = list(row['SF'])
    b = list(row['LF'])
    a = [e for e in a if e not in ("(", ")", "-", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                                   "x", "&", "/", "\\", "\'", " ", "+", "@", 'q', ".")]
    if set(a) < set(b):
        temp.set_value(index, 'boo', True)
check = df[temp['boo'] == False]
check = check[check['Source'].str.contains('ADAM') == False]
check = check[check['Source'].str.contains('UMLS') == False]

if verbose:
    if check.shape[0] <= exceptions6:
        print "\nHeuristic Check #6 (SF in LF): CLEARED!"
    else:
        print "\nHeuristic Check #6 (SF in LF): NOT CLEARED \nReview {} terms in Step2_Output/check_heuristic6".format(check.shape[0])

# Export dataframe
check.to_csv(path_or_buf='Step2_Output/check_heuristic6',
             columns=['NSF', 'NSFUI', 'SF', 'SFUI', 'LF', 'LFUI', 'Qualifier', 'PLF', 'PLFUI',
                      'UMLS CUI', 'MetaMap CUI', 'Source', 'SFEUI', 'LFEUI', 'Prevalence'],
             index=False,
             header=True,
             sep='|')

# Export dataframe
df.to_csv(path_or_buf='Step2_Output/combination_part2',
          columns=['NSF', 'NSFUI', 'SF', 'SFUI', 'LF', 'LFUI', 'Qualifier', 'PLF', 'PLFUI',
                   'UMLS CUI', 'MetaMap CUI', 'Source', 'SFEUI', 'LFEUI', 'Prevalence'],
          index = False,
          header = True,
          sep = '|')
