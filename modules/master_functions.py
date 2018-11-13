'''
master_functions.py

Library of commonly used functions for the clinical abbreviation expander
'''
import pandas as pd
import string

# Function to standardize short form abbreviations.
#   Converts text to uppercase
#   Removes punctuation and whitespace
def standard_sf(sf):
    sf = sf.upper()
    sf = sf.translate(None, string.punctuation + " ")
    return sf


# Given a data frame with cells that themselves contain delimited data,
#   expand the data frame such that each value in the delimited cell
#   gets its own row.
#   Fancy thing from Stack Overflow...
#       http://stackoverflow.com/questions/17116814/pandas-how-do-i-split-text-in-a-column-into-multiple-rows
def expand_col(df, col, d = '|'):
    # s = df[col].str.split(d).apply(pd.Series, 1).stack()
    s = df[col]
    s = s.str
    s = s.split(d)
    s = s.apply(pd.Series, 1)
    s = s.stack()
    s.index = s.index.droplevel(-1) # to line up with df's index
    s.name = col
    del df[col]
    df = df.join(s)
    return df
