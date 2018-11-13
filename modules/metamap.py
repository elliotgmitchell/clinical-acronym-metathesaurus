'''MetaMap.py

Relies on local installation of MetaMap :(

from .../public_mm
    start server:       ./bin/skrmedpostctl start
    stop server:        ./bin/skrmedpostctl stop
    is server running:  ps -ef | grep java
https://metamap.nlm.nih.gov/Installation.shtml

'''
# Python wrapper for MetaMap: https://github.com/AnthonyMRios/pymetamap
from pymetamap import MetaMap
import pandas as pd
import subprocess
import os

mm_path = os.path.expanduser('~/UMLS/MetaMap/public_mm')
# my_mm_path = os.path.expanduser('~/UMLS/MetaMap/public_mm/bin/metamap16')

mm = MetaMap.get_instance(mm_path + '/bin/metamap16')


# Helper function to start the MetaMap server
def start_mm(mm_path = mm_path):
    mm_path = mm_path + '/bin/skrmedpostctl'
    subprocess.call([mm_path, 'start'])

def stop_mm(mm_path = mm_path):
    mm_path = mm_path + '/bin/skrmedpostctl'
    subprocess.call([mm_path, 'stop'])

# Function to execute MetaMap on a given file
# Pass file name, (it will use option --sldiID) FIle should be ID|sentence
# -N for detailed output
# https://metamap.nlm.nih.gov/Docs/MM09_Usage.shtml
def execute_mm(filename,
            output_file = None,
            mm_path = mm_path,
            file_id_format = True,
            exact_match = True):
    command = [mm_path + '/bin/metamap16']

    command.append('-N')  # Machine readable output

    if exact_match:
        command.append('-z')  # Term processing flag - treat input as one term
        command += ["--threshold", "1000"]  # Only return exact matches

    if file_id_format:
        command.append('--sldiID')  # Indicate that input file has ID column
    command.append(filename)
    if output_file:
        command.append(output_file)
    mm_process = subprocess.check_output(command)
    return mm_process

if __name__ == '__main__':


    start_mm(mm_path)


    # Testing with random terms
    sents = ['Heart Attack', 'John had a huge heart attack', 'lung cancer'] # Sentences to process with MetaMap
    ix = ['x11', 'x12', 'x13'] # Index labels for each sentence
    concepts, error = mm.extract_concepts(sents, ix)
    for concept in concepts:
        print concept
        print concept.cui
        print concept.score

    # Testing with our data
    wiki_db = pd.read_csv('./Step1_Output/wikipedia', sep = '|')
    sample = wiki_db[110:120]['LF']
    print sample
    concepts, error = mm.extract_concepts(sample, sample.index)
    for concept in concepts:
        # print sample[int(concept.index)], concept.preferred_name, concept.cui, concept.score
        print concept

    stop_mm(mm_path)

'''
Things that might be important to consider:
What proportion of the string is covered by the concept (concept.pos_info)?
    This matters less for matching, but more for findin relevant content
Pick the term with the highest score (concept.score)?
    should there be a minimum score?
Do multiple matches cover different parts of the string?
    If so, maybe they should be combined
'''
