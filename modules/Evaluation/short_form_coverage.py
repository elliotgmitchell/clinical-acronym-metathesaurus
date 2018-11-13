'''
coverage.py

Ananlysis of short form coverage in the MIMIC III database

MIMIC short forms extracted from the first 1 million notes using
UTHealth's java module for abbreviation detection (CARD module 1)
https://sbmi.uth.edu/ccb/resources/abbreviation.htm
https://drive.google.com/file/d/0B1ZQiTNDfmlBdFM0SUt1RWxwRzA/view

'''
from __future__ import division
import numpy as np
import pandas as pd
import string


# TODO reference master function instead
# Function to standardize short form abbreviations.
#   Converts text to uppercase
#   Removes punctuation and whitespace
def standard_sf(sf):
    sf = sf.upper()
    sf = sf.translate(None, string.punctuation + " ")
    return sf


# Load list of short forms in MIMIC
with open("mimic_card_abr_detection_output.txt") as mimic_output:
    mimic_short_forms = mimic_output.read().strip()
    # mimic_short_forms = mimic_short_forms.replace('/', '\n') # Deal with weird combo abbreviations
    mimic_short_forms = mimic_short_forms.split('\n')

# Normaize
mimic_short_forms = pd.Series(mimic_short_forms).apply(standard_sf)
# Store as a set
mimic_short_forms = set(mimic_short_forms)

# Load Normalized short forms (NSF) from SematicGroups.txt
mae_db = pd.read_csv(r"../../Clinical Abbreviation and Acronym Crosswalk/SemanticGroups.txt",
                        sep = '|',
                        na_filter = False)
mae_short_forms = mae_db.NSF

# Store as a set
mae_short_forms = set(mae_short_forms)

# Print lengths
print "MIMIC has {} unique short forms".format(len(mimic_short_forms))
print "MAE has {} unique short forms".format(len(mae_short_forms))

# Intersection
intersect = mimic_short_forms & mae_short_forms
print "There are {} overlapping short forms".format(len(intersect))

# Coverage = Intersection / MIMIC Length
coverage = len(intersect) / len(mimic_short_forms)
print "Macro coverage: {:.2f}%".format(coverage*100)


# Calculate coverage with frequency information
mimic_freq = pd.read_csv('mimic_card_output_with_freq.txt', na_filter = False)
mimic_freq['NSF'] = mimic_freq.word.apply(standard_sf)
# print mimic_freq


total_count = sum(mimic_freq.freq)

coverage_count = mimic_freq.loc[mimic_freq.NSF.isin(intersect)]
coverage_count = sum(coverage_count.freq)

print 'Total short form occurences in MIMIC: {}'.format(total_count)
print 'Total occurences of covered short forms in MIMIC: {}'.format(coverage_count)
print 'Micro coverage: {:.2f}%'.format(coverage_count/total_count*100)
