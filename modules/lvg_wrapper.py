'''
Python wrapper for UMLS specialist lexicon tools

NOTE: Requires local installation of umls lvg tools
'''
import os
import subprocess

lvg_path = os.path.expanduser('~/UMLS/lvg2017')

# Functions to take input and execute command line specialist lexicon tools

# Function specific to norm
def lvg_norm(term_string):
    p = subprocess.Popen(['echo', term_string], stdout = subprocess.PIPE)
    norm = subprocess.check_output([lvg_path + '/bin/norm'], stdin = p.stdout)
    norm = norm.strip().split('|')[1]
    return norm

def lvg(file_name, flow = '', output_file = '', restrict = False, print_no_output = False):
    command = [lvg_path + '/bin/lvg',
                '-i:' + file_name,
                '-f:' + flow]
    if output_file != '':
        command.append('-o:' + output_file)
    if restrict:
        command.append('-R:1')
    if print_no_output:
        command.append('-n')
    lvg_process = subprocess.check_output(command)
    return lvg_process
