#-------------------------------------------------------------------
# Step 1: Preprocessing
# wikipedia database
#-------------------------------------------------------------------

import pandas as pd
from master_functions import *

# Load database
db = pd.read_csv('../sources/wikipedia/wikipedia_abr_database.csv',
                       sep = ',',
                        na_filter = False
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

# Source
out_db['Source'] = 'wikipedia'

# Short Form
out_db['SF'] = db['abr']

# Long Form
out_db['LF'] = db['long_form']

### Cleaning ###

# Manual replacement based on heuristics
out_db['LF'] = out_db['LF'].replace(to_replace="5% dextrose in water - IV fluids for intravenous therapy", value="5% dextrose in water")
out_db['LF'] = out_db['LF'].replace(to_replace="amino acids:", value="amino acids")
out_db['LF'] = out_db['LF'].replace(to_replace='airway, breathing, circulation, etc. Refers to priority of needs in emergency situations. Exact spell-out and details after "C" vary by institution, but the "ABCs" theme is recurrent.', value="airway, breathing, circulation, etc.")
out_db['LF'] = out_db['LF'].replace(to_replace='{{anchor|CHEM-20}} a group of blood tests', value="a group of blood tests")
out_db['LF'] = out_db['LF'].replace(to_replace='echocardiogram,| enteric cytopathic human orphan virus', value="echocardiogram")
out_db['LF'] = out_db['LF'].replace(to_replace="four times each day (from Latin ''{{not a typo|quater}} in die'')", value="four times each day (from Latin ''quater in die'')")
out_db['LF'] = out_db['LF'].replace(to_replace="which see (from Latin ''quod vide'');", value="which see (from Latin ''quod vide'')")
out_db['LF'] = out_db['LF'].replace(to_replace='transfer (pronounced "turf")', value="transfer (pronounced 'turf')")
out_db['LF'] = out_db['LF'].replace(to_replace='transferred (pronounced "turfed", as in "We just turfed Mrs Johnson OTD")', value="transferred (pronounced 'turfed')")
out_db['LF'] = out_db['LF'].replace(to_replace='"bone break, me fix"', value="bone break, me fix")
out_db['LF'] = out_db['LF'].replace(to_replace="within normal limits (also: we never looked)", value="within normal limits")
out_db['LF'] = out_db['LF'].replace(to_replace="Duchenne muscular dystrophy;", value="Duchenne muscular dystrophy")
out_db['LF'] = out_db['LF'].replace(to_replace="extracorporeal shockwave lithotripsy;", value="extracorporeal shockwave lithotripsy")
out_db['LF'] = out_db['LF'].replace(to_replace="full ward diet;", value="full ward diet")
out_db['LF'] = out_db['LF'].replace(to_replace="gastrointestinal;", value="gastrointestinal")
out_db['LF'] = out_db['LF'].replace(to_replace="in vitro fertilization;", value="in vitro fertilization")
out_db['LF'] = out_db['LF'].replace(to_replace="kilocalorie;", value="kilocalorie")
out_db['LF'] = out_db['LF'].replace(to_replace="Kaposi's sarcoma;", value="Kaposi's sarcoma")
out_db['LF'] = out_db['LF'].replace(to_replace="mean cell hemoglobin;", value="mean cell hemoglobin")
out_db['LF'] = out_db['LF'].replace(to_replace="moderate;", value="moderate")
out_db['LF'] = out_db['LF'].replace(to_replace="nitric oxide synthase;", value="nitric oxide synthase")
out_db['LF'] = out_db['LF'].replace(to_replace="normal vaginal delivery;", value="normal vaginal delivery")
out_db['LF'] = out_db['LF'].replace(to_replace="recurrent laryngeal nerve;", value="recurrent laryngeal nerve")
out_db['LF'] = out_db['LF'].replace(to_replace="student nurse ;", value="student nurse")
out_db['LF'] = out_db['LF'].replace(to_replace="sodium nitroprusside;", value="sodium nitroprusside")
out_db['LF'] = out_db['LF'].replace(to_replace="verotoxin-producing Escherichia coli, also known as enterohaemorrhagic E.&nbsp;coli", value="verotoxin-producing Escherichia coli (aka enterohaemorrhagic Escherichia coli)")
out_db['LF'] = out_db['LF'].replace(to_replace="sodium nitroprusside;", value="sodium nitroprusside")
out_db['SF'] = out_db['SF'].replace(to_replace="VPC (PVC)", value="VPC")
out_db['NSF'] = out_db['NSF'].replace(to_replace="VPCPVC", value="VPC")
out_db['LF'] = out_db['LF'].replace(to_replace="within defined limits (as per hospital defined policy)", value="within defined limits")
out_db['LF'] = out_db['LF'].replace(to_replace="as evidenced by (commonly used by nurses)", value="as evidenced by")
out_db['NSF'] = out_db['NSF'].replace(to_replace="AGESCRITERIA", value="AGES")
out_db['SF'] = out_db['SF'].replace(to_replace="AGES criteria", value="AGES")
out_db['LF'] = out_db['LF'].replace(to_replace="bowel signs in all 4 quadrants (also sometimes BS + all 4 quads)", value="bowel signs in all 4 quadrants")
out_db['LF'] = out_db['LF'].replace(to_replace="Community Treatment Order (psychiatric term for forced drugging outside hospital context)", value="Community Treatment Order")
out_db['LF'] = out_db['LF'].replace(to_replace="end diastolic flow (describing the flow of blood through the umbilical artery)", value="end diastolic flow")
out_db['LF'] = out_db['LF'].replace(to_replace="early morning urine sample (being the most concentrated, generally used for pregnancy testing)", value="early morning urine sample")
out_db['LF'] = out_db['LF'].replace(to_replace="general medical condition (e.g., 0 GMC)", value="general medical condition")
out_db['LF'] = out_db['LF'].replace(to_replace="keep vein open (with slow infusion)", value="keep vein open")
out_db['NSF'] = out_db['NSF'].replace(to_replace="PVCVPC", value="PVC")
out_db['SF'] = out_db['SF'].replace(to_replace="PVC (VPC)", value="PVC")
out_db['LF'] = out_db['LF'].replace(to_replace="pack-years (years of smoking multiplied by average number of packs, or fraction thereof, per day)", value="pack-years")
out_db['LF'] = out_db['LF'].replace(to_replace="social history (personal habits, living situation, job)", value="social history")
out_db['LF'] = out_db['LF'].replace(to_replace="test-of-cure (+TOC meaning patient cured of disease proven via test)", value="test-of-cure")
out_db['LF'] = out_db['LF'].replace(to_replace="transport (by ambulance to or between hospitals)", value="transport")
out_db['NSF'] = out_db['NSF'].replace(to_replace="BRCA1GENE", value="BRCA1")
out_db['SF'] = out_db['SF'].replace(to_replace="BRCA1 (gene)", value="BRCA1")
out_db['LF'] = out_db['LF'].replace(to_replace="breast cancer 1", value="breast cancer 1 (gene or protein)")
out_db['NSF'] = out_db['NSF'].replace(to_replace="BRCA2GENE", value="BRCA2")
out_db['SF'] = out_db['SF'].replace(to_replace="BRCA2 (gene)", value="BRCA2")
out_db['LF'] = out_db['LF'].replace(to_replace="breast cancer 2", value="breast cancer 2 (gene or protein)")
out_db['LF'] = out_db['LF'].replace(to_replace="cool, dry, intact (when referring to incision/surgical sites)", value="cool, dry, intact")
out_db['LF'] = out_db['LF'].replace(to_replace="return to clinic (appointment for outpatient for next medical examination)", value="return to clinic")
out_db['NSF'] = out_db['NSF'].replace(to_replace="QWKALSOQW", value="QWK")
out_db['SF'] = out_db['SF'].replace(to_replace="q.wk. also qw", value="q.wk.")
out_db['LF'] = out_db['LF'].replace(to_replace="Bilateral Lower Extremity (in/on both legs).", value="Bilateral Lower Extremity")
out_db['LF'] = out_db['LF'].replace(to_replace="complains of...", value="complains of")
out_db['SF'] = out_db['SF'].replace(to_replace="C/O or c/o", value="c/o")
out_db['NSF'] = out_db['NSF'].replace(to_replace="COORCO", value="CO")
out_db['LF'] = out_db['LF'].replace(to_replace="Type two diabetes mellitus, formerly known as Non-Insulin Dependent Diabetes Mellitus.", value="Type two diabetes mellitus")
out_db['LF'] = out_db['LF'].replace(to_replace="group B Strep.", value="group B Strep")
out_db['LF'] = out_db['LF'].replace(to_replace="history of ...", value="history of")
out_db['LF'] = out_db['LF'].replace(to_replace="every day, usually regarded as once daily. Generally written in lowercase.", value="once daily")
out_db['LF'] = out_db['LF'].replace(to_replace="every morning. Generally written in lowercase.", value="every morning")
out_db['LF'] = out_db['LF'].replace(to_replace="every night. Generally written in lowercase.", value="every night")
out_db['LF'] = out_db['LF'].replace(to_replace="semel in die meaning once daily. Used only in veterinary medicine.", value="once daily (From Latin 'semel in die')")
out_db['LF'] = out_db['LF'].replace(to_replace="date=November 2016}}", value="End-of-life")
out_db['LF'] = out_db['LF'].replace(to_replace="Jackson-Pratt {drain}", value="Jackson-Pratt (drain)")
out_db['LF'] = out_db['LF'].replace(to_replace="day(s)", value="day (or days)")
out_db['LF'] = out_db['LF'].replace(to_replace="modified release)", value="modified release")
out_db['LF'] = out_db['LF'].replace(to_replace="note well (please pay attention) (from Latin 'nota bene')", value="note well (please pay attention, from Latin 'nota bene')")
out_db['LF'] = out_db['LF'].replace(to_replace="slow release)", value="slow release")
out_db['LF'] = out_db['LF'].replace(to_replace="abdominal[abduction]", value="abdominal")
out_db['LF'] = out_db['LF'].replace(to_replace="nonspecific [drug]", value="nonspecific (drug)")
out_db['LF'] = out_db['LF'].replace(to_replace="Physicians' Desk Reference[]", value="Physicians' Desk Reference")
out_db['LF'] = out_db['LF'].replace(to_replace="motor neurone disease, also known as 'amyotrophic lateral sclerosis', 'Lou Gehrig's disease' or 'Charcot disease'", value="motor neuron disease (also known as 'amyotrophic lateral sclerosis', 'Lou Gehrig's disease' or 'Charcot disease')")
out_db['LF'] = out_db['LF'].replace(to_replace="alpha-amino-3-hydroxy-5-methyl-4-isoxazolepropionic acid receptor of the brain", value="alpha-amino-3-hydroxy-5-methyl-4-isoxazolepropionic acid")
out_db['SF'] = out_db['SF'].replace(to_replace="AMPA receptor", value="AMPA")
out_db['NSF'] = out_db['NSF'].replace(to_replace="AMPARECEPTOR", value="AMPA")
out_db['LF'] = out_db['LF'].replace(to_replace="aware and oriented or alert and oriented", value="alert and oriented")
out_db['SF'] = out_db['SF'].replace(to_replace="A&O or A/O", value="A&O")
out_db['NSF'] = out_db['NSF'].replace(to_replace="AOORAO", value="AO")
out_db['LF'] = out_db['LF'].replace(to_replace="computed axial tomography / computed tomography", value="computed axial tomography")
out_db['SF'] = out_db['SF'].replace(to_replace="CAT / CT", value="CAT")
out_db['NSF'] = out_db['NSF'].replace(to_replace="CATCT", value="CAT")
out_db['LF'] = out_db['LF'].replace(to_replace="familial atypical multiple mole melanoma syndrome", value="familial atypical multiple mole melanoma (syndrome)")
out_db['SF'] = out_db['SF'].replace(to_replace="FAMMM syndrome", value="FAMMM")
out_db['NSF'] = out_db['NSF'].replace(to_replace="FAMMMSYNDROME", value="FAMMM")
out_db['SF'] = out_db['SF'].replace(to_replace="H/H or H&H", value="H/H")
out_db['NSF'] = out_db['NSF'].replace(to_replace="HHORHH", value="HH")
out_db['LF'] = out_db['LF'].replace(to_replace="natural killer cells", value="natural killer (a type of cell)")
out_db['SF'] = out_db['SF'].replace(to_replace="NK cells", value="NK")
out_db['NSF'] = out_db['NSF'].replace(to_replace="NKCELLS", value="NK")
out_db['LF'] = out_db['LF'].replace(to_replace="Sternberg cell", value="Sternberg (a type of cell)")
out_db['SF'] = out_db['SF'].replace(to_replace="RS cell", value="RS")
out_db['NSF'] = out_db['NSF'].replace(to_replace="RSCELL", value="RS")
out_db['SF'] = out_db['SF'].replace(to_replace="T.S.T.H.", value="TSTH")
out_db['LF'] = out_db['LF'].replace(to_replace="air conduction and bone conduction, as in Weber test", value="air conduction and bone conduction (as in Weber test)")
out_db['LF'] = out_db['LF'].replace(to_replace="amyotrophic lateral sclerosis, also known as 'motor neurone disease', 'Lou Gehrig's disease' or 'Charcot disease", value="amyotrophic lateral sclerosis (also known as 'motor neurone disease', 'Lou Gehrig's disease' or 'Charcot disease)")
out_db['LF'] = out_db['LF'].replace(to_replace="antitetanus serum, that is, antitetanus immunoglobulins", value="antitetanus serum (that is, antitetanus immunoglobulins)")
out_db['LF'] = out_db['LF'].replace(to_replace="benign prostatic hyperplasia aka benign prostatic hypertrophy", value="benign prostatic hypertrophy")
out_db['LF'] = out_db['LF'].replace(to_replace="The BRAT diet: bananas, rice, applesauce, toast", value="bananas, rice, applesauce, toast (diet)")
out_db['LF'] = out_db['LF'].replace(to_replace="another version of the BRAT diet: bananas, rice, applesauce, toast, yogurt", value="bananas, rice, applesauce, toast, yogurt (diet)")
out_db['LF'] = out_db['LF'].replace(to_replace="chronic myelogenous leukemia, also called chronic myeloid leukaemia", value="chronic myelogenous leukemia (aka chronic myeloid leukaemia)")
out_db['LF'] = out_db['LF'].replace(to_replace="cardiopulmonary-cerebral resuscitation, a version of CPR", value="cardiopulmonary-cerebral resuscitation (a version of CPR)")
out_db['LF'] = out_db['LF'].replace(to_replace="Dentariae Medicinae Doctor, that is, Doctor of Dental Medicine", value="Doctor of Dental Medicine (Dentariae Medicinae Doctor)")
out_db['LF'] = out_db['LF'].replace(to_replace="docusate sodium; from the chemical name dioctyl sodium sulfosuccinate", value="docusate sodium (from the chemical name dioctyl sodium sulfosuccinate)")
out_db['LF'] = out_db['LF'].replace(to_replace="estimated date of delivery (at 40/40 weeks of pregnancy); expected date of delivery", value="estimated date of delivery (at 40/40 weeks of pregnancy)")
out_db['LF'] = out_db['LF'].replace(to_replace="endothelium-derived relaxing factor aka nitric oxide", value="endothelium-derived relaxing factor (aka nitric oxide)")
out_db['LF'] = out_db['LF'].replace(to_replace="electronic fetal monitoring, aka external fetal monitoring", value="electronic fetal monitoring (aka external fetal monitoring)")
out_db['LF'] = out_db['LF'].replace(to_replace="healthcare-associated infection or hospital-acquired infection", value="healthcare-associated infection")
out_db['LF'] = out_db['LF'].replace(to_replace="hydroxy ethyl methacrylate, a material in soft contact lenses", value="hydroxy ethyl methacrylate (a material in soft contact lenses)")
out_db['LF'] = out_db['LF'].replace(to_replace="spinal disk herniation or herniated disk, that is, herniated nucleus pulposus", value="herniated nucleus pulposus (spinal disk herniation or herniated disk)")
out_db['LF'] = out_db['LF'].replace(to_replace="intraparenchymal hemorrhage or intraperitoneal hemorrhage or idiopathic pulmonary hemosiderosis", value="intraparenchymal hemorrhage")
out_db['LF'] = out_db['LF'].replace(to_replace="last menstrual period first day of the menstrual period", value="last menstrual period (first day of the last menstrual period)")
out_db['LF'] = out_db['LF'].replace(to_replace="mobile intensive care unit / medical intensive care unit", value="medical intensive care unit")
out_db['LF'] = out_db['LF'].replace(to_replace="mechlorethamine, vincristine, procarbazine, and prednisone in combination", value="mechlorethamine, vincristine, procarbazine, and prednisone (in combination)")
out_db['LF'] = out_db['LF'].replace(to_replace="pulmonary artery catheter, pulmonary artery catheterisation", value="pulmonary artery catheter")
out_db['LF'] = out_db['LF'].replace(to_replace="postpartum depression, that is, postnatal depression", value="postpartum depression (aka postnatal depression)")
out_db['LF'] = out_db['LF'].replace(to_replace="purified protein derivative or Mantoux test, for tuberculosis testing", value="purified protein derivative (aka Mantoux test, for tuberculosis testing)")
out_db['LF'] = out_db['LF'].replace(to_replace="tetanus, diphtheria, and acellular pertussis combined vaccine", value="tetanus, diphtheria, and acellular pertussis (combined vaccine)")
out_db['LF'] = out_db['LF'].replace(to_replace="angiotensin II receptor antagonist", value="angiotensin II receptor blocker")
out_db['LF'] = out_db['LF'].replace(to_replace="calcium pyrophosphate", value="calcium pyrophosphate deposition")
out_db['LF'] = out_db['LF'].replace(to_replace="creatine phosphokinase heart", value="heart creatine phosphokinase")
out_db['LF'] = out_db['LF'].replace(to_replace="guttae", value="drops (from Latin 'guttae')")
out_db['SF'] = out_db['SF'].replace(to_replace="GvHD,", value="GvHD")
out_db['SF'] = out_db['SF'].replace(to_replace="HACEK]]", value="HACEK")
out_db['LF'] = out_db['LF'].replace(to_replace="pound or pounds", value="pound")
out_db['LF'] = out_db['LF'].replace(to_replace="by mouth, that is, orally", value="by mouth (from Latin 'per os')")
out_db['LF'] = out_db['LF'].replace(to_replace="St Louis virus", value="St Louis encephalitis virus")
out_db['LF'] = out_db['LF'].replace(to_replace="thyrotropin-receptor antibody", value="thyroid-stimulating-hormone-receptor antibody")

for index, row in out_db.iterrows():
    if (row['NSF'] == 'AC') and (row['LF'] == "before a meal"):
        out_db.set_value(index, 'LF', "before a meal (from Latin 'Ante cibum')")
    if (row['NSF'] == 'ATCC') and (row['LF'] == "ATCC"):
        out_db.set_value(index, 'LF', "American Type Culture Collection")
    if (row['NSF'] == 'BID') and (row['LF'] == "twice a day"):
        out_db.set_value(index, 'LF', "twice a day (from Latin 'bis in die')")
    if (row['NSF'] == 'ISQ') and (row['LF'] == "no change"):
        out_db.set_value(index, 'LF', "no change (from Latin 'in status quo')")
    if (row['NSF'] == 'SOS') and (row['LF'] == "if needed"):
        out_db.set_value(index, 'LF', "if needed (from Latin 'si opus sit')")

# Replace extra quotes
out_db['LF'] = out_db['LF'].str.replace("''","'")

# Add rows
df = pd.DataFrame([["ECHO","","ECHO","","enteric cytopathic human orphan (virus)","","","","","","wikipedia","","",""],
                   ["BS+4QUADS","","BS + 4 quads","","bowel signs in all 4 quadrants","","","","","","wikipedia","","",""],
                   ["QW","","qw","","weekly (once a week)","","","","","","wikipedia","","",""],
                   ["INF", "", "INF", "", "Interferon", "", "", "", "", "", "wikipedia", "", "", ""],
                   ["AO", "", "A/O", "", "alert and oriented", "", "", "", "", "", "wikipedia", "", "", ""],
                   ["CT", "", "CT", "", "computed tomography", "", "", "", "", "", "wikipedia", "", "", ""],
                   ["HH", "", "H&H", "", "hemoglobin and hematocrit", "", "", "", "", "", "wikipedia", "", "", ""],
                   ["BPH", "", "BPH", "", "benign prostatic hyperplasia", "", "", "", "", "", "wikipedia", "", "", ""],
                   ["HAI", "", "HAI", "", "hospital-acquired infection", "", "", "", "", "", "wikipedia", "", "", ""],
                   ["IPH", "", "IPH", "", "intraperitoneal hemorrhage", "", "", "", "", "", "wikipedia", "", "", ""],
                   ["IPH", "", "IPH", "", "idiopathic pulmonary hemosiderosis", "", "", "", "", "", "wikipedia", "", "", ""],
                   ["MICU", "", "MICU", "", "mobile intensive care unit", "", "", "", "", "", "wikipedia", "", "", ""],
                   ["PAC", "", "PAC", "", "pulmonary artery catheterisation", "", "", "", "", "", "wikipedia", "", "", ""],
                   ["ABD", "", "Abd", "", "abduction", "", "", "", "", "", "wikipedia", "", "", ""]],
                  columns=['NSF',
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

out_db = out_db.append(df)

# Remove rows
out_db = out_db[out_db['NSF'].str.contains("BRCA1PROTEIN") == False]
out_db = out_db[out_db['NSF'].str.contains("BRCA2PROTEIN") == False]
out_db = out_db[out_db['LF'].str.contains("and many variations of the above") == False]
out_db = out_db[out_db['LF'].str.contains("interferons -") == False]
out_db = out_db[out_db['LF'].str.contains("intrauterine death") == False]

### Save to a file ###
out_db.to_csv('Step1_Output/preprocess_wikipedia',
              index = False,
              header = True,
              sep = '|')
