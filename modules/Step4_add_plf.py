from __future__ import division
import pandas as pd
import string
import jellyfish
import random
from collections import Counter
from tqdm import tqdm
from numpy import mean
import time
import json
import pickle

### Global Variables ###
distance_cutoff = .3  # Validated cutoff based on density of distances
verbose = True
debug = False

distance_cache = {} # {(NLF1,NLF2 - sorted) : distance}
used_cache = 0
new_comparisons = 0

# Convenience setting for printing pandas data frames
pd.set_option('display.width', 1000)


# Function to format unique identifiers
def format_ui(counter, prefix):
    return prefix + ("{:06}".format(counter))


# Function to create a preferred long term unique identifier (PLFUI)
def gen_plfui(PLFUI_counter, NSF, col, col_val):
    PLFUI = format_ui(PLFUI_counter, "P")
    abr_db.loc[(abr_db.NSF == NSF) & (abr_db[col] == col_val), 'PLFUI'] = PLFUI
    PLFUI_counter = PLFUI_counter + 1
    return PLFUI_counter, PLFUI


# Helper function to compare two normalized long forms. Called by
#   get_closest_plfui. Uses a cache of previously performed comparisons
#   to improve performance slightly.
def compare_nlfs(nlf1, nlf2):
    global used_cache
    global new_comparisons
    nlf_pair = [nlf1, nlf2]
    nlf_pair.sort()
    nlf_pair = tuple(nlf_pair)
    if nlf_pair in distance_cache:
        used_cache += 1
        return distance_cache[nlf_pair]
    else:
        dist = jellyfish.levenshtein_distance(str(nlf1), str(nlf2))
        dist = dist / ((len(nlf1) + len(nlf2)) * 0.5)
        distance_cache[nlf_pair] = dist
        new_comparisons += 1
        return dist


# Function to compare the distance between a Normalized Long Form (NLF)
#   and all of the other NLFs that have already been assigned a PLFUI.
#   Returns the PLFUI closest to the NLF in levenshtein_distance. To normalize
#   comparison between short and long strings, the distance if devided by the
#   average length of the two comparison strings.
#   If no assignemnts are within the distance_cutoff, returns None.
def get_closest_plfui(NLF, assignments):
    comparators = list(assignments.keys())

    distance = [compare_nlfs(NLF, x) for x in comparators]
    min_dist = min(distance)

    # Assign to closest match, within distance_cutoff
    if min_dist <= distance_cutoff:
        # Assign to closet match
        PLFUI = assignments[comparators[distance.index(min_dist)]]
        return PLFUI, min_dist
    # No matches - this snowflake gets it's own PLFUI
    else:
        return None, None


# big ol function to assign plfuis
def add_plfuis(abr_db):
    # Will be incremented as PLFUIs are assigned
    PLFUI_counter = 1

    # TODO remove performace testing code
    NSF_counter = 0
    start = time.time()

    # For each normalized short form
    for NSF in tqdm(abr_db.NSF.unique()):
    # for NSF in ['ND']:
        NSF_counter += 1
        nsf_slice = abr_db[abr_db.NSF == NSF]

        # TODO - evidently a dictionary isn't the best data structure for this
        assignments = {} # NLF:PLFUI

        # For each unique CUI
        for CUI, count in Counter(nsf_slice['MetaMap CUI']).items():
            if CUI == '':   continue
            if count <= 1:  continue

            # Assign an ID for first comers
            if len(assignments) == 0:
                PLFUI_counter, PLFUI = gen_plfui(PLFUI_counter, NSF, 'MetaMap CUI', CUI)
                # Track assigned PLFUIs (multiple NLFs may map to the same CUI)
                for NLF in nsf_slice.loc[nsf_slice['MetaMap CUI'] == CUI, 'NLF'].unique():
                    assignments[NLF] = PLFUI
                    if debug: print('Assigned {} as {}'.format(NLF, PLFUI))

            # Compare NLF to already assigned long forms
            else:
                # Handling to work for multiple NLFs within a single CUI
                closest_distance = 100  # Larger than any reasonable distance
                closest_PLFUI = None
                foo = []
                for NLF in nsf_slice.loc[nsf_slice['MetaMap CUI'] == CUI, 'NLF'].unique():
                    PLFUI, distance = get_closest_plfui(NLF, assignments)
                    if (PLFUI != None) & (distance < closest_distance):
                        closest_PLFUI, closest_distance = PLFUI, distance

                if closest_PLFUI:
                    abr_db.loc[(abr_db.NSF == NSF) & (abr_db['MetaMap CUI'] == CUI), 'PLFUI'] = closest_PLFUI
                    if debug: print("Assigned {} to {} (distance is {})".format(NLF, closest_PLFUI, closest_distance))
                else:
                    PLFUI_counter, PLFUI = gen_plfui(PLFUI_counter, NSF, 'MetaMap CUI', CUI)
                    if debug: print ('Assigned {} as {}'.format(NLF, PLFUI))
                assignments[NLF] = PLFUI

            for foo in nsf_slice.loc[nsf_slice['MetaMap CUI'] == CUI, 'NLF'].unique():
                for bar in nsf_slice.loc[nsf_slice['MetaMap CUI'] == CUI, 'NLF'].unique():
                    if compare_nlfs(foo,bar) > distance_cutoff:
                        print ("{},{},{},{},{}".format(NSF, CUI, foo, bar, compare_nlfs(foo,bar)))

        ### Now assign based on NLF ###

        # Assign PLFUI based on lines that share normalized long forms
        for NLF in abr_db.loc[(abr_db.NSF == NSF) & (abr_db['PLFUI'] == ''), 'NLF'].unique():
            if NLF == '': continue  # Sanity check

            # If no PLFUIs have been assigned yet, assign one
            if len(assignments) == 0:
                PLFUI_counter, PLFUI = gen_plfui(PLFUI_counter, NSF, 'NLF', NLF)
                assignments[NLF] = PLFUI
                if debug: print ('Assigned {} as {}'.format(NLF, PLFUI))
            # Otherwise, compare disatances
            else:
                PLFUI, distance = get_closest_plfui(NLF, assignments)
                if PLFUI:
                    abr_db.loc[(abr_db.NSF == NSF) & (abr_db['NLF'] == NLF), 'PLFUI'] = PLFUI
                    if debug: print ("Assigned {} to {} (distance is {})".format(NLF, PLFUI, distance))
                else:
                    PLFUI_counter, PLFUI = gen_plfui(PLFUI_counter, NSF, 'NLF', NLF)
                    if debug: print ('Assigned {} as {}'.format(NLF, PLFUI))
                assignments[NLF] = PLFUI


        if debug: print (abr_db.loc[abr_db.NSF == NSF,['NSF','NLF','MetaMap CUI','PLFUI']].drop_duplicates())
        # if NSF_counter >= 20: break

    if verbose:
        print ("Running on {} NSFs took {} seconds total ({} on average)".format(NSF_counter,
                                                                                time.time() - start,
                                                                                (time.time() - start) / NSF_counter))
        print ("Used cache {} times, with {} new comparisions ({}% cache)".format(used_cache,
                                                                                    new_comparisons,
                                                                                    used_cache / new_comparisons))

    return abr_db



# Function to assign a preferred long form (PLF) for each PLFUI
def add_plfs(abr_db):
    # Load cached cistance comparisons
    global distance_cache
    if len(distance_cache) == 0:
        if verbose: print ("Loading cached distance comparisons...")
        with open('Step4_Output/distance_comparison_cache.dict', 'r') as cache_file:
            distance_cache = pickle.load(cache_file)
    global used_cache
    global new_comparisons
    used_cache = 0
    new_comparisons = 0

    # TODO remove performace testing code
    start = time.time()

    # For each PLFUI
    for PLFUI in tqdm(abr_db['PLFUI'].unique()):
        # What are the unique NLFs?
        plfui_slice = abr_db[abr_db['PLFUI'] == PLFUI]
        nlf_list = plfui_slice.NLF.unique()
        NSF = plfui_slice.NSF.unique()[0]

        nlf_count = len(nlf_list)
        # If there's just one NLF, it's our PLF too
        if nlf_count == 1:
            PLF = nlf_list[0]
        # If there are two, they will be equidistant, just pick one
        elif nlf_count == 2:
            PLF = nlf_list[1]
        # Otherwise, if there are more than two, compare distances
        else:
            # how far is each nlf from all of its neighbors?
            nlf_distances_list = []
            for NLF in nlf_list:
                distances = [compare_nlfs(NLF, x) for x in nlf_list]
                nlf_distances_list.append(sum(distances))
            # pick the nlf closest to the other nlfs
            min_dist = min(nlf_distances_list)
            PLF = nlf_list[nlf_distances_list.index(min_dist)]


        # print "NSF length: {} ".format(len(NSF))
        # print "NLF Count: {} ".format(nlf_count)


        # TODO filter to make sure lf is comprehensive of sf characters
        # print nlf_list
        # nlf_list = nlf_list[[lf_has_sf(sf=NSF[0],lf=lf) for lf in nlf_list]]
        # print nlf_list
        # nlf_count = len(nlf_list)

        # print NSF
        # print nlf_list
        # print nlf_distances_list
        # print PLF

        # Save the PLF
        abr_db.loc[abr_db['PLFUI'] == PLFUI, 'PLF'] = PLF

        if debug and (nlf_count > 4):
            print (abr_db.loc[abr_db.PLFUI == PLFUI, ['NSF', 'NLF', 'PLFUI', 'PLF']])

    if verbose:
        print ("Running took {} seconds total ({} on average)".format(time.time() - start,
                                                                     (time.time() - start) / len(abr_db['PLFUI'].unique())))
        print ("Used cache {} times, with {} new comparisions ({}% cache)".format(used_cache,
                                                                                    new_comparisons,
                                                                                    used_cache / new_comparisons))

    return abr_db



if __name__ == '__main__':

    # Load abbreviation database with normalized long forms and CUIs
    if verbose: print ("Loading abbreviation database...")
    abr_db = pd.read_csv('Step3_Output/abr_db_with_NLF_and_CUIs',
                            na_filter = False,
                            sep = '|')

    if verbose: print ("Beginning PLFUI analysis (this could take a while)...")
    abr_db = add_plfuis(abr_db)

    if verbose: print ("Saving file with PLFUIs...")
    abr_db.to_csv('Step4_Output/abr_db_with_PLFUIs',
                    index = False,
                    sep = '|')

    # Save distance_cache as a JSON for future use and analysis
    if verbose: print ("Saving cached distance calculations...")
    with open('Step4_Output/distance_comparison_cache.dict', 'w') as cache_file:
        # save pairwise distance comparisions for future use
        pickle.dump(distance_cache, cache_file, protocol=pickle.HIGHEST_PROTOCOL)


    # if verbose: print "Loading file with PLFUIs..."
    # abr_db = pd.read_csv('Step4_Output/abr_db_with_PLFUIs',
    #                         na_filter = False,
    #                         sep = '|')

    if verbose: print ("Beginning PLF assignment (this could take a while)...")
    abr_db = add_plfs(abr_db)

    if verbose: print ("Saving file with PLFs...")
    abr_db.to_csv('Step4_Output/abr_db_with_PLFs',
                    index = False,
                    sep = '|')

    print ("Done!")
