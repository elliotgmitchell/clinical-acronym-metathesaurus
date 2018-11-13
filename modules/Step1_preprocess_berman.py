#-------------------------------------------------------------------
# Step 1: Preprocessing
# Berman Database
#-------------------------------------------------------------------

import pandas as pd
from master_functions import *

berm_db = pd.read_csv('../sources/berman/12000_pathology_abbreviations.txt',
                       sep = '=',
                       header = None,
                       index_col = False,
                       na_filter = False,
                       names = ['SF',
                                'LF'])

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

# Strip leading and trailing whitespace
berm_db['LF'] = berm_db['LF'].str.strip()
berm_db['SF'] = berm_db['SF'].str.strip()

# Add short form
out_db['SF'] = berm_db['SF']

# Add long form
out_db['LF'] = berm_db['LF']

# Add normalized short form
out_db['NSF'] = berm_db['SF'].apply(standard_sf)

# Add source
out_db['Source'] = "berman"

### Cleaning

# Remove rows
out_db = out_db[out_db['SF'].str.contains('.*@$') == False]
out_db = out_db[out_db['SF'].str.contains("///////////////") == False]
out_db = out_db[out_db['SF'].str.contains("%") == False]
out_db = out_db[out_db['LF'].str.contains("dipeptidyl peptidase a") == False]
out_db = out_db[out_db['LF'].str.contains("^c$") == False]
out_db = out_db[out_db['NSF'].str.contains("CONGRUOUS") == False]
out_db = out_db[out_db['NSF'].str.contains("EDTARENALVASCULARDISEASE") == False]
out_db = out_db[out_db['LF'].str.contains("hepatitis surface antigen") == False]
out_db = out_db[out_db['NSF'].str.contains("HVSCULTURE") == False]
out_db = out_db[out_db['LF'].str.contains("gardnerella vaginialis") == False]
out_db = out_db[out_db['NSF'].str.contains("JUMP") == False]
out_db = out_db[out_db['NSF'].str.contains("KCODESASSIGNEDTODURABLEMEDICALEQUIPMENTREGIONALCARRIERS") == False]
out_db = out_db[out_db['LF'].str.contains("musculoskeletal") == False]
out_db = out_db[out_db['LF'].str.contains("provided by a non physician") == False]
out_db = out_db[out_db['NSF'].str.contains("PHYLUMARTHROPODA") == False]
out_db = out_db[out_db['SF'].str.contains("rbs") == False]
out_db = out_db[out_db['NSF'].str.contains("RNSOFTTISSUE") == False]
out_db = out_db[out_db['NSF'].str.contains("RNSOFTTISSUEBLOODPOOLSTUDY") == False]
out_db = out_db[out_db['NSF'].str.contains("SEROTONIN") == False]
out_db = out_db[out_db['NSF'].str.contains("UNGULATES") == False]
out_db = out_db[out_db['LF'].str.contains("maximum oxygen uptake") == False]
out_db = out_db[out_db['LF'].str.contains("calovo fever") == False]

# Replace rows
out_db['LF'] = out_db['LF'].replace(to_replace='combined term for "guys and gals"', value="combined term for guys and gals")
out_db['LF'] = out_db['LF'].replace(to_replace='arterial pressure index', value="ankle-brachial blood pressure index")
out_db['LF'] = out_db['LF'].replace(to_replace='bleo mtx vcr', value="methotrexate, bleomycin, vincristine")
out_db['LF'] = out_db['LF'].replace(to_replace='bleo dox vbl', value="doxorubicin, bleomycin, vinblastine")
out_db['LF'] = out_db['LF'].replace(to_replace='adult polycystic disease', value="adult polycystic kidney disease")
out_db['LF'] = out_db['LF'].replace(to_replace='mad cow disease', value="Bovine spongiform encephalopathy (aka mad cow disease)")
out_db['LF'] = out_db['LF'].replace(to_replace='mad cow disease', value="Bovine spongiform encephalopathy (aka mad cow disease)")
out_db['LF'] = out_db['LF'].replace(to_replace='congenital central hypoventilation', value="congenital central hypoventilation syndrome")
out_db['LF'] = out_db['LF'].replace(to_replace='lying down', value="decubitus (lying down)")
out_db['LF'] = out_db['LF'].replace(to_replace='840', value="an antitumor agent")
out_db['LF'] = out_db['LF'].replace(to_replace='gonadoblastoma', value="gonadoblastoma Y")
out_db['LF'] = out_db['LF'].replace(to_replace='thalassemia screen', value="hemoglobin A2")
out_db['LF'] = out_db['LF'].replace(to_replace='hiv', value="human immunodeficiency virus")
out_db['LF'] = out_db['LF'].replace(to_replace='cyfos', value="ifosfamide")
out_db['LF'] = out_db['LF'].replace(to_replace='muscle power', value="Medical Research Council")
out_db['SF'] = out_db['SF'].replace(to_replace="mrc grade", value="mrc")
out_db['NSF'] = out_db['NSF'].replace(to_replace="MRCGRADE", value="MRC")
out_db['LF'] = out_db['LF'].replace(to_replace="never gave birth", value="nulliparous (never gave birth)")
out_db['LF'] = out_db['LF'].replace(to_replace="pediatric clinical test of sensory integration", value="pediatric clinical test of sensory interaction and balance")
out_db['LF'] = out_db['LF'].replace(to_replace="packed #000066 blood cells", value="packed red blood cells")
out_db['LF'] = out_db['LF'].replace(to_replace="first pregnancy", value="primipara (first pregnancy)")
out_db['LF'] = out_db['LF'].replace(to_replace="factor 11", value="plasma thromboplastin antecedent (factor 11)")
out_db['LF'] = out_db['LF'].replace(to_replace="reading comprehension for aphasia", value="reading comprehension battery for aphasia")
out_db['LF'] = out_db['LF'].replace(to_replace="alanin-transaminase", value="alanine aminotransferase")
out_db['LF'] = out_db['LF'].replace(to_replace="sr calf bolus", value="sustained release")
out_db['SF'] = out_db['SF'].replace(to_replace="sulfa sure", value="sr")
out_db['NSF'] = out_db['NSF'].replace(to_replace="SULFASURE", value="SR")
out_db['LF'] = out_db['LF'].replace(to_replace="tretinoin", value="all-trans retinoic acid (tretinoin)")
out_db['LF'] = out_db['LF'].replace(to_replace="total anomalous venous return", value="total anomalous pulmonary venous return")
out_db['LF'] = out_db['LF'].replace(to_replace="tumor of vip secreting cells", value="tumor of vasoactive-intestinal-peptide-secreting cells")
out_db['LF'] = out_db['LF'].replace(to_replace="ascorbic acid", value="vitamin C (ascorbic acid)")
out_db['LF'] = out_db['LF'].replace(to_replace="tocopherol", value="vitamin E (tocopherol)")
out_db['LF'] = out_db['LF'].replace(to_replace="diarrheogenic tumor", value="Watery diarrhea, hypokalaemia, hypochlorhydria or achlorhydria (syndrome)")
out_db['LF'] = out_db['LF'].replace(to_replace="x rays", value="roentgen radiation")
out_db['LF'] = out_db['LF'].replace(to_replace="hepatitis b vaccine", value="hepatitis b immunoglobulin (vaccine)")

# Complex replacements
for index, row in out_db.iterrows():
    if (row['SF'] == 'bf') and (row['LF'] == "lymphocyte mitogenic factor"):
        out_db.set_value(index, 'LF', "blastogenic factor (a type of lymphocyte mitogenic factor)")
    if row['SF'] == 'epoxyatp':
        out_db.set_value(index, 'LF', "epoxy adenosine triphosphate")
    if (row['SF'] == 'fvc') and (row['LF'] == "vital capacity"):
        out_db.set_value(index, 'LF', "forced vital capacity")
    if (row['SF'] == 'hd') and (row['LF'] == "huntington chorea"):
        out_db.set_value(index, 'LF', "huntington disease")
    if (row['SF'] == 'hiaa') and (row['LF'] == "serotonin"):
        out_db.set_value(index, 'LF', "5-hydroxyindoleacetic acid (serotonin)")
    if (row['SF'] == 'hmg') and (row['LF'] == "menopausal gonadotropin"):
        out_db.set_value(index, 'LF', "human menopausal gonadotropin")
    if (row['SF'] == "ht") and (row['LF'] == "serotonin"):
        out_db.set_value(index, 'LF', "5-hydroxytryptamine (serotonin)")
    if (row['SF'] == "grav") and (row['LF'] == "pregnancy"):
        out_db.set_value(index, 'LF', "gravida (number of pregnancies)")
    if (row['SF'] == "hnig") and (row['LF'] == "normal immunoglobulin"):
        out_db.set_value(index, 'LF', "human normal immunoglobulin")
    if (row['SF'] == "mefv") and (row['LF'] == "maximum expiratory flow rate"):
        out_db.set_value(index, 'LF', "maximum expiratory flow volume")
    if (row['SF'] == "mifv") and (row['LF'] == "maximum inspiratory flow rate"):
        out_db.set_value(index, 'LF', "maximum inspiratory flow volume")
    if (row['SF'] == "oirda") and (row['LF'] == "intermittent rhythmic delta activity"):
        out_db.set_value(index, 'LF', "occipital intermittent rhythmic delta activity")
    if (row['SF'] == "ol") and (row['LF'] == "left eye"):
        out_db.set_value(index, 'LF', "Oculus laevus (left eye)")
    if (row['SF'] == "pggp") and (row['LF'] == "poly"):
        out_db.set_value(index, 'LF', "poly (chemical)")
    if (row['SF'] == "prb") and (row['LF'] == "rectal bleeding"):
        out_db.set_value(index, 'LF', "per-rectal bleeding")
    if (row['SF'] == "rec") and (row['LF'] == "fresh"):
        out_db.set_value(index, 'LF', "recent")
    if (row['SF'] == "rh") and (row['LF'] == "cord blood"):
        out_db.set_value(index, 'LF', "rh factor")
    if (row['SF'] == "sig") and (row['LF'] == "prescription"):
        out_db.set_value(index, 'LF', "prescription (From Latin: 'signetur')")
    if (row['SF'] == "srif") and (row['LF'] == "somatostatin"):
        out_db.set_value(index, 'LF', "somatotropin release inhibiting factor (aka somatostatin)")
    if (row['SF'] == "svi") and (row['LF'] == "stroke index"):
        out_db.set_value(index, 'LF', "stroke volume index")
    if (row['SF'] == "ung") and (row['LF'] == "ointment"):
        out_db.set_value(index, 'LF', "ointment (From Latin: 'unguentum')")
    if (row['SF'] == "vitd") and (row['LF'] == "cholecalciferol"):
        out_db.set_value(index, 'LF', "vitamin D (cholecalciferol)")
    if (row['SF'] == "htlv 3") and (row['LF'] == "human immunodeficiency virus"):
        out_db.set_value(index, 'LF', "human immunodeficiency virus (formerly human t cell lymphotropic virus type 3)")
    if (row['SF'] == "htlv3") and (row['LF'] == "human immunodeficiency virus"):
        out_db.set_value(index, 'LF', "human immunodeficiency virus (formerly human t cell lymphotropic virus type 3)")
    if (row['SF'] == "htlv-iii") and (row['LF'] == "human immunodeficiency virus"):
        out_db.set_value(index, 'LF', "human immunodeficiency virus (formerly human t cell lymphotropic virus type 3)")
    if (row['SF'] == "htlv-3") and (row['LF'] == "human t cell lymphotropic virus 3"):
        out_db.set_value(index, 'LF', "human immunodeficiency virus (formerly human t cell lymphotropic virus type 3)")
    if (row['SF'] == "htig") and (row['LF'] == "tetanus vaccine"):
        out_db.set_value(index, 'LF', "human tetanus immunoglobulin (tetanus vaccine)")
    if (row['SF'] == "cf") and (row['LF'] == "white female"):
        out_db.set_value(index, 'LF', "caucasian female (white female)")

# Export file
out_db.to_csv( path_or_buf='Step1_Output/preprocess_berman',
               index = False,
               header = True,
               sep = '|')
