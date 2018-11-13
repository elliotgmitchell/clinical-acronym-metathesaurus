'''
Code to add lexical normalization and MetaMap CUIs to database
'''
import pandas as pd
import os
from lvg_wrapper import *
from metamap import *
from tqdm import tqdm

# Convenience setting for printing pandas data frames
pd.set_option('display.width', 1000)

# ---------------------------------------------------------
# Add Normalized Long Forms (NLF) with UMLS lvg
# ---------------------------------------------------------
def add_nlf(run_lvg = True, verbose = False):
    # Load big DB
    if verbose: print "Loading database..."
    abr_db = pd.read_csv('Step2_Output/combination_part5',
                         sep = '|',
                         na_filter = False)

    # Remove non-ascii characters from long forms
    abr_db['LF'] = abr_db.LF.str.replace('[^\x00-\x7F]','')

    # Find unique long forms
    uniq_long_forms = pd.Series(abr_db['LF'].unique())

    # Save off file for processing by lvg tools
    uniq_long_forms.to_csv('Step3_Output/lvg_input.temp',
                            index = False,
                            encoding = 'ascii')

    # Call lvg on file
    if run_lvg or (not os.path.exists('Step3_Output/lvg_input.temp')):
        if verbose: print "Running Lexical Variant Generation..."
        lvg_output = lvg('Step3_Output/lvg_input.temp',
                        flow = 'q0:g:rs:o:t:l:B:Ct:q7:q8',
                        output_file = 'Step3_Output/lvg_output.temp',
                        restrict = True,
                        print_no_output = True)
        if verbose: print lvg_output
    else:
        if verbose: print "Using previously cached LVG output..."

    # Read in output from lvg
    norm_long_forms = pd.read_csv('Step3_Output/lvg_output.temp',
                                    sep = '|',
                                    header = None,
                                    usecols = [1])

    # Combine long forms and noramlized long forms into a single data frame
    normed_df = pd.DataFrame()
    normed_df['LF'] = uniq_long_forms
    normed_df['NLF'] = norm_long_forms

    # if Lexical Variant Generation returned '-No Output', populate NLF with LF
    normed_df.loc[normed_df['NLF'] == '-No Output-', 'NLF'] = normed_df.loc[normed_df['NLF'] == '-No Output-', 'LF']

    # Merge normalized long forms into abbreviation data frame
    abr_db = pd.merge(abr_db, normed_df, how = 'left', on = 'LF')

    # Save off abr_db with normalized long forms
    if verbose: print "Saving database with normalized long forms..."
    abr_db.to_csv('Step3_Output/abr_db_with_NLF.temp',
                            index = False,
                            sep = '|')

    return abr_db

# ---------------------------------------------------------
# Add MetaMap CUIs
# ---------------------------------------------------------
def add_cuis(abr_db = None, run_mm = True, verbose = False):
    # If we don't pass in a dataframe for processing, grab it from the disk,
    #   or call the add_nlf to get make it
    if abr_db == None:
        try:
            abr_db = pd.read_csv('Step3_Output/abr_db_with_NLF.temp',
                                    na_filter = False,
                                    sep = '|')
        except Exception as e:
            abr_db = add_nlf()

    # Start MetaMap server
    start_mm()

    # Remove non-ascii characters from normalized long forms
    abr_db['NLF'] = abr_db.NLF.str.replace('[^\x00-\x7F]','')

    # unique normalized long forms to process with metamap
    uniq_nlf = abr_db[['LFUI','NLF']].drop_duplicates(subset = ['NLF'])

    # Make file to pass to MetaMap (format: ID|NLF)
    uniq_nlf.to_csv('Step3_Output/metamap_input.temp',
                    sep = '|',
                    index = False,
                    encoding = 'ascii')

    # Run metamap on input file and save output to temp file
    if run_mm or (not os.path.exists('Step3_Output/metamap_output.temp')):
        if verbose: print "Running MetaMap..."
        execute_mm('Step3_Output/metamap_input.temp',
                    output_file = 'Step3_Output/metamap_output.temp',
                    exact_match = True)

    # Load metamap output as a DataFrame for processing
    if verbose: print "Loading MetaMap output..."
    mm_output = pd.read_csv('Step3_Output/metamap_output.temp',
                            sep = '|',
                            na_filter = False,
                            header = None,
                            index_col = None,
                            names = ['LFUI',
                                    'MMI',
                                    'score',
                                    'preferred_term',
                                    'CUI',
                                    'semantic_type',
                                    'original_string',
                                    'TX',
                                    'position',
                                    '?'],
                            usecols = [0,2,3,4,8])

    # Pick the CUI with the highest score on a given subportion of the long form
    # combining cuis that don't overlap the term
    # For each LFUI
    if verbose: print "Adding MetaMap data to abbreviation database..."
    for LFUI in tqdm(mm_output['LFUI'].unique()):
        # Slice that referrences the current long form unique identifier
        slice_df = mm_output[mm_output['LFUI'] == LFUI]
        # Remove duplicate positions - store CUI with best score, per position
        slice_df = slice_df.drop_duplicates(subset = ['position'])

        # Save CUI list and preferred_term list to abr_db
        cuis = '|'.join(slice_df['CUI'])
        pref_terms= '|'.join(slice_df['preferred_term'])

        # Traverse back to the NLF from the LFUI
        NLF = abr_db.loc[abr_db['LFUI'] == LFUI, 'NLF']
        NLF = list(NLF)[0]

        abr_db.loc[abr_db['NLF'] == NLF, 'MetaMap CUI'] = cuis
        abr_db.loc[abr_db['NLF'] == NLF, 'MetaMap Preferred Term'] = pref_terms

        # temp = abr_db.loc[abr_db['NLF'] == NLF, ['NSF','LFUI','NLF','MetaMap CUI']]
        # if len(temp['LFUI'].unique()) > 1:
        #     print temp

        # abr_db.loc[abr_db['LFUI'] == LFUI, 'MetaMap CUI'] = cui_list
        # abr_db.loc[abr_db['LFUI'] == LFUI, 'MetaMap Preferred Term'] = pref_term_list

    # Save abr_db with MetaMap CUIs
    if verbose: print "Saving database with UMLS CUIs from MetaMap..."
    abr_db.to_csv('Step3_Output/abr_db_with_NLF_and_CUIs',
                            index = False,
                            sep = '|')

    # Stop MetaMap server
    stop_mm()

    return abr_db


if __name__ == '__main__':
    # abr_db = add_nlf(run_lvg = False, verbose = True)
    abr_db = add_cuis(run_mm = False, verbose = True)
