#-------------------------------------------------------------------
# Step 1: Preprocessing
# UTHealth Vanderbilt Database
#-------------------------------------------------------------------

import pandas as pd
from master_functions import *
from tqdm import tqdm

def parse_cuis(cui):
    cui = cui.replace('|',',')
    cui = cui.replace('c', 'C')
    return cui


# Return cell content without count or prevalence info
def trim_vandy_cell(c):
    return c.split('_')[0]


# Wrapper function to convert vanderbilt sense inventories into out standard format
def process_vandy_file(file_name):
    # Load database
    vand_db = pd.read_csv( '../sources/uthealth/{}.txt'.format(file_name),
                                   sep = '\t',
                                   na_filter = False,
                                   index_col = False)

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
    out_db['NSF'] = vand_db['abbreviation'].apply(standard_sf)

    # Prevalence
    out_db['Prevalence'] = vand_db['frequency']

    # Source
    out_db['Source'] = file_name

    # CUIs
    out_db['UMLS CUI'] = vand_db['CUI'].apply(parse_cuis)

    # Short Form
    out_db['SF'] = vand_db['variation']

    # Long Form
    out_db['LF'] = vand_db['sense']

    # Expand and trim Short Form
    out_db = expand_col(out_db, 'SF')
    out_db['SF'] = out_db['SF'].apply(trim_vandy_cell)

    # Reorder columns
    out_db = out_db[['NSF',
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

    ### Clean Vandy Clinic Notes ###

    # Replace rows
    out_db['LF'] = out_db['LF'].replace(to_replace='phoneme ""s"" sound', value="sound of letter S (phoneme)")
    out_db['LF'] = out_db['LF'].replace(to_replace="living children (2)", value="2 living children")
    out_db['LF'] = out_db['LF'].replace(to_replace="living children (3)", value="3 living children")
    out_db['LF'] = out_db['LF'].replace(to_replace="ace inhibitor (angiotensin converting enzyme inhibitor)",
                                        value="angiotensin converting enzyme inhibitor")
    out_db['LF'] = out_db['LF'].replace(to_replace="2nd diagonal branch (off of left anterior descending coronary artery)", value="2nd diagonal branch")
    out_db['LF'] = out_db['LF'].replace(to_replace="digital versatile disc (digital video disc)", value="digital video disc")
    out_db['SF'] = out_db['SF'].replace(to_replace=".LM", value="LM")
    out_db['SF'] = out_db['SF'].replace(to_replace="OD.", value="OD")
    out_db['LF'] = out_db['LF'].replace(to_replace="ophthalmic nerve (of cn5)", value="ophthalmic nerve")
    out_db['LF'] = out_db['LF'].replace(to_replace="thiamine", value="vitamin B1 (thiamine)")
    out_db['LF'] = out_db['LF'].replace(to_replace="with meals", value="with meals (From Latin: 'cum cibo')")
    out_db['LF'] = out_db['LF'].replace(to_replace="ck-mb ratio", value="creatine kinase MB ratio")
    out_db['LF'] = out_db['LF'].replace(to_replace="enterovirus by amp probe", value="enterovirus species D")
    out_db['LF'] = out_db['LF'].replace(to_replace="mohs", value="MOHS surgery")
    out_db['LF'] = out_db['LF'].replace(to_replace="misses", value="mrs.")
    out_db['LF'] = out_db['LF'].replace(to_replace="pet", value="pet animal")
    out_db['LF'] = out_db['LF'].replace(to_replace="tums", value="tums (antacid)")
    out_db['LF'] = out_db['LF'].replace(to_replace="nothing by moouth", value="nothing by mouth (From Latin: Nil per os)")
    out_db['LF'] = out_db['LF'].replace(to_replace="o (blood type)", value="blood type o")
    out_db['LF'] = out_db['LF'].replace(to_replace="st (ekg)", value="ST segment (on an electrocardiogram)")

    # Remove rows
    out_db = out_db[out_db['LF'].str.contains('latin for ""foot"" / part of ""pes planus"" = ""flat foot') == False]
    out_db = out_db[out_db['LF'].str.contains('latin for ""foot"" / part of ""pes cavus"" = high-arched foot') == False]
    out_db = out_db[out_db['LF'].str.contains('part of ""pes anserine"" =  insertion of the conjoined tendons of three muscles onto the anteromedial surface of the proximal extremity of the tibia') == False]
    out_db = out_db[out_db['LF'].str.contains('special supplemental nutrition program') == False]
    out_db = out_db[out_db['LF'].str.contains('medical center east') == False]
    out_db = out_db[(out_db['LF'].str.contains('afternoon') == False) & (out_db['SF'].str.contains('p$') == False)]
    out_db = out_db[(out_db['LF'].str.contains('22q') == False) & (out_db['LF'].str.contains('chromosome') == False)]
    out_db = out_db[out_db['NSF'].str.contains('RHYTHM') == False]

    # Complex replacements
    for index, row in out_db.iterrows():
        if (row['NSF'] == 'CVS') and (row['LF'] == "cvs"):
            out_db.set_value(index, 'LF', "CVS Drugstore")
        if (row['NSF'] == 'ETOH') and (row['LF'] == "alcohol"):
            out_db.set_value(index, 'LF', "ethanol (alcohol)")
        if (row['NSF'] == 'BPD') and (row['LF'] == "bronch"):
            out_db.set_value(index, 'LF', "bronchopulmonary dysplasia")
        if (row['NSF'] == 'BASORE') and (row['LF'] == "basophils"):
            out_db.set_value(index, 'LF', "relative basophil count")
        if (row['NSF'] == 'EOSIRE'):
            out_db.set_value(index, 'LF', "relative eosinophil count")
        if (row['NSF'] == 'KY') and (row['LF'] == "ky"):
            out_db.set_value(index, 'LF', "null")
        if (row['NSF'] == 'LYMPRE') and (row['LF'] == "lymphocytes"):
            out_db.set_value(index, 'LF', "relative lymphocyte count")
        if (row['NSF'] == 'MD') and (row['LF'] == "md"):
            out_db.set_value(index, 'LF', "medical doctor")
        if (row['NSF'] == 'MDS') and (row['LF'] == "medical doctor"):
            out_db.set_value(index, 'LF', "medical doctors")
        if (row['NSF'] == 'MONORE') and (row['LF'] == "monocytes"):
            out_db.set_value(index, 'LF', "relative monocyte count")
        if (row['NSF'] == 'OS') and (row['LF'] == "os"):
            out_db.set_value(index, 'LF', "mouth (From Latin: 'os')")
        if (row['NSF'] == 'PEDS') and (row['LF'] == "pediatric"):
            out_db.set_value(index, 'LF', "pediatrics")
        if (row['NSF'] == 'PTINR') and (row['LF'] == "international normalized ratio"):
            out_db.set_value(index, 'LF', "prothrombin time - international normalized ratio")
        if (row['NSF'] == 'V') and (row['LF'] == "v"):
            out_db.set_value(index, 'LF', "The letter V")

    # Remove "null"
    out_db['UMLS CUI'] = out_db['UMLS CUI'].replace(to_replace='null', value="")
    out_db = out_db[out_db['LF'].str.contains('null') == False]

    # Remove short forms with periods at beginning
    out_db = out_db[out_db['SF'].str.contains("^\.") == False]

    ### Save to a file ###
    out_db.to_csv('Step1_Output/preprocess_{}'.format(file_name),
                  index = False,
                  header = True,
                  sep = '|')

if __name__ == '__main__':
    process_vandy_file('vanderbilt_clinic_notes')
    process_vandy_file('vanderbilt_discharge_sums')
