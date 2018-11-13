#-------------------------------------------------------------------
# Output crosswalk
#-------------------------------------------------------------------

import pandas as pd

# Import abbreviation database from Step 4

abr_db = pd.read_csv('Step4_Output/abr_db_with_PLFs',
                na_filter = False,
                sep = '|')

# Add new column names

abr_db.columns = ['NSF', 'NSFUI', 'SF', 'SFUI', 'LF', 'LFUI', 'PLF', 'PLFUI', 'SourceCUI',
                  'MetaMapCUI_LF', 'Source', 'SourceEUI', 'SourcePrevalence', 'NLF', 'MetaMapTerm_LF']

#-------------------------------------------------------------------
# Output SourceInstances.txt
#-------------------------------------------------------------------

df_SourceInstances = abr_db[['NSFUI', 'SFUI','SF', 'PLFUI', 'LFUI', 'LF', 'Source',
                             'SourceCUI', 'SourceEUI', 'SourcePrevalence']]

df_SourceInstances = df_SourceInstances.sort('SFUI')

df_SourceInstances.to_csv(path_or_buf='Step5_Output/SourceInstances.txt',
          index = False,
          header = True,
          sep = '|')

#-------------------------------------------------------------------
# Output SemanticGroups.txt
#-------------------------------------------------------------------

df_SemanticGroups = abr_db[['NSFUI', 'NSF', 'PLFUI', 'PLF']]

df_SemanticGroups = df_SemanticGroups.drop_duplicates().sort('PLFUI')

df_SemanticGroups.to_csv(path_or_buf='Step5_Output/SemanticGroups.txt',
          index = False,
          header = True,
          sep = '|')

#-------------------------------------------------------------------
# Output SimpleMap.txt
#-------------------------------------------------------------------

df_SimpleMap = abr_db[['NSFUI', 'NSF', 'PLFUI', 'PLF', 'MetaMapCUI_LF', 'MetaMapTerm_LF']]

df_SimpleMap.columns = ['NSFUI', 'NSF', 'PLFUI', 'PLF', 'MetaMapCUI_PLF', 'MetaMapTerm_PLF']

df_SimpleMap = df_SimpleMap.drop_duplicates(subset='PLFUI').sort('PLFUI')

df_SimpleMap.to_csv(path_or_buf='Step5_Output/SimpleMap.txt',
          index = False,
          header = True,
          sep = '|')

#-------------------------------------------------------------------
# Output Map.txt
#-------------------------------------------------------------------

df_Map = abr_db[['NSFUI', 'SFUI','SF', 'PLFUI', 'LFUI', 'LF', 'MetaMapCUI_LF', 'MetaMapTerm_LF']]

df_Map = df_Map.sort('SFUI')

df_Map.to_csv(path_or_buf='Step5_Output/Map.txt',
          index = False,
          header = True,
          sep = '|')

#-------------------------------------------------------------------
# Output Sources.txt
#-------------------------------------------------------------------

df_Sources = pd.read_csv('Preliminary_Work/Manual/Sources.txt',
                na_filter = False,
                sep = '|')

# Assign PLFUI frequency and LFUI frequency
# Note this takes about 20 minutes to run
for index, line in df_Sources.iterrows():
    item = line['Source']
    count_PLF = []
    count_LF = []
    for row in df_SourceInstances.itertuples():
        if item in row:
            if row[4] not in count_PLF:  # row[4] = 'PLFUI'
                count_PLF.append(row[4])
            if row[5] not in count_LF:  # row[5] = 'LFUI'
                count_LF.append(row[5])
    df_Sources.set_value(index, 'PLFUIFrequency', len(count_PLF))
    df_Sources.set_value(index, 'LFUIFrequency', len(count_LF))

df_Sources.to_csv(path_or_buf='Step5_Output/Sources.txt',
          index = False,
          header = True,
          sep = '|')

#-------------------------------------------------------------------
# Output Files.txt
#-------------------------------------------------------------------

df_Files = pd.read_csv('Preliminary_Work/Manual/Files.txt',
                na_filter = False,
                sep = '|')

df_ColumnNames = pd.read_csv('Preliminary_Work/Manual/ColumnNames.txt',
                na_filter = False,
                sep = '|')

# Assign Columns
df_Files.set_value(0, 'Columns', df_Files.shape[1])
df_Files.set_value(1, 'Columns', df_ColumnNames.shape[1])
df_Files.set_value(2, 'Columns', df_Sources.shape[1])
df_Files.set_value(3, 'Columns', df_SourceInstances.shape[1])
df_Files.set_value(4, 'Columns', df_SemanticGroups.shape[1])
df_Files.set_value(5, 'Columns', df_SimpleMap.shape[1])
df_Files.set_value(6, 'Columns', df_Map.shape[1])

# Assign Rows
df_Files.set_value(0, 'Rows', df_Files.shape[0])
df_Files.set_value(1, 'Rows', df_ColumnNames.shape[0])
df_Files.set_value(2, 'Rows', df_Sources.shape[0])
df_Files.set_value(3, 'Rows', df_SourceInstances.shape[0])
df_Files.set_value(4, 'Rows', df_SemanticGroups.shape[0])
df_Files.set_value(5, 'Rows', df_SimpleMap.shape[0])
df_Files.set_value(6, 'Rows', df_Map.shape[0])

df_Files.to_csv(path_or_buf='Step5_Output/Files.txt',
          index = False,
          header = True,
          sep = '|')

# Manually added size to output
