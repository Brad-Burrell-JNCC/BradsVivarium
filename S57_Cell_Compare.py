# Name: S57_Cell_Compare.py
# Author: Bradley Burrell - August 2023
# Description: This script accepts a CSV with wiki information, downloads it as HTML, convert all to markdown and save
#              into a directory structure that mirror the wiki structure.


# CSV Schema, Header(Example):
#   Page Tile (UKHO S57 ENC Conversion),
#   Data Engineer(Brad.Burrell)
#   Last Editor(Brad.Burrell)
#   Path(http://jncc-wiki/Projects_and_solutions/UKHO_S57_ENC_Conversion)

# Version: 1.0
# REQUIREMENTS:
#  1. Python
#   1.1. Version 3.10
#  2. Modules
#   2.1. csv
#   2.2. os
#   2.3. requests
#   2.4. configparser
#   2.5. markdownify
#   2.6  sys
#   2.7

import hashlib
import os
from datetime import datetime
import winsound
import sys
import configparser

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def file_checker(path_to_file):
    file_size = os.path.getsize(path_to_file)
    mod_time = os.path.getmtime(path_to_file)
    create_time = os.path.getctime(path_to_file)
    md5_hash = md5(path_to_file)
    return {"file_path": path_to_file, "file_size": file_size, "mod_time": mod_time, "create_time": create_time,
            "md5_hash": md5_hash}

def process_done():
    """
    Produces a Sound when script is Done
    :return:
    """
    freq = 100
    dur = 50

    # loop iterates 7 times i.e, 7 beeps will be produced.
    for beeps in range(0, 7):
        winsound.Beep(freq, dur)
        freq += 100
        dur += 50


# Check for a valid config file, and creates one if needed.
cwd = os.getcwd()
config_path = "{}\\{}".format(cwd, 'S57_Cell_Compare.ini')
check_for_config = os.path.exists(config_path)
if check_for_config is True:
    print("Config File found... Reading...")
elif check_for_config is False:
    print("Config File Not found...\nPlease edit {} and rerun...".format(config_path))
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'Path to New S57': r'Please\Update\To\Path',
                         'Path to Old S57': r'Please\Update\To\Path',
                         'Cells': 'All'}
    with open(config_path, 'w') as configfile:
        config.write(configfile)
    sys.exit()


# Read parameters from config file
config = configparser.ConfigParser()
config.sections()
config.read(config_path)
# old_parent_dir = r"J:\GISprojects\Marine\UKHOS57\Data\20230620\UKHO-S57 23-06-20\ENC_ROOT\GB"
old_parent_dir = config['DEFAULT']['Path to New S57']
# new_parent_dir = r"J:\GISprojects\Marine\UKHOS57\Data\20230803\UKHO-S57 27-06-23\ENC_ROOT\ENC_ROOT\GB"
new_parent_dir = config['DEFAULT']['Path to Old S57']
# issue_cells = ["GB42524C", "GB50220C", "GB50220D", "GB50588A"]
issue_cells = config['DEFAULT']['Cells']

if issue_cells == 'All':
    issue_cells = []
    for old_cell in os.listdir(old_parent_dir):
        issue_cells.append(old_cell)
    for new_cell in os.listdir(new_parent_dir):
        if new_cell not in issue_cells:
            issue_cells.append(new_cell)
else:
    issue_cells = issue_cells.split(',')

# Checks parameters aren't Placeholders
if old_parent_dir == r'Please\Update\To\Path':
    print("Path to New S57 is still set to Placeholder, Please update...")
    sys.exit()
elif new_parent_dir == 'Please Update to your JNCC Wiki Username':
    print("Path to Old S57 is still set to Placeholder, Please update...")
    sys.exit()
else:
    pass

for cells in issue_cells:
    old_file_check = None
    old_cell_path = "{}\\{}".format(old_parent_dir, cells)
    print(old_cell_path)
    for old_root, old_dir, old_files in os.walk(old_cell_path):
        for old_file in old_files:
            if old_file.endswith(".000"):
                old_file_path = os.path.join(old_root, old_file)
                old_file_check = file_checker(old_file_path)

    new_file_check = None
    new_cell_path = "{}\\{}".format(new_parent_dir, cells)
    for new_root, new_dir, new_files in os.walk(new_cell_path):
        for new_file in new_files:
            if new_file.endswith(".000"):
                new_filepath = os.path.join(new_root, new_file)
                new_file_check = file_checker(new_filepath)

    old_download_date = datetime.strptime(old_file_check['file_path'].split('\\')[5], '%Y%m%d').strftime('%d/%m/%Y')
    old_cell_name = old_file_check['file_path'].split('\\')[-1].split('.')[0]
    old_cell_filename = old_file_check['file_path'].split('\\')[-1]
    old_fttp_name = old_file_check['file_path'].split('\\')[6]
    old_size = old_file_check['file_size']
    old_create_date = datetime.fromtimestamp(old_file_check['create_time']).strftime('%Y-%m-%d %H:%M:%S')
    old_mod_date = datetime.fromtimestamp(old_file_check['mod_time']).strftime('%Y-%m-%d %H:%M:%S')
    old_md5_hashcode = old_file_check['md5_hash']

    new_download_date = datetime.strptime(new_file_check['file_path'].split('\\')[5], '%Y%m%d').strftime('%d/%m/%Y')
    new_cell_name = new_file_check['file_path'].split('\\')[-1].split('.')[0]
    new_cell_filename = new_file_check['file_path'].split('\\')[-1]
    new_fttp_name = new_file_check['file_path'].split('\\')[6]
    new_size = new_file_check['file_size']
    new_create_date = datetime.fromtimestamp(new_file_check['create_time']).strftime('%Y-%m-%d %H:%M:%S')
    new_mod_date = datetime.fromtimestamp(new_file_check['mod_time']).strftime('%Y-%m-%d %H:%M:%S')
    new_md5_hashcode = new_file_check['md5_hash']

    print()
    print("{:=^80}".format(old_cell_name))
    print("""
    S57 - {0}
    FTTP Filename:     {2}
    Cell Filename:     {3}
    Filesize:          {4} Bytes
    Date Download:     {0}
    Datetime Created:  {5}
    Datetime Modified: {6}
    MD5 Hash:          {7}
    """.format(old_download_date, old_cell_name, old_fttp_name, old_cell_filename, old_size, old_create_date,
               old_mod_date, old_md5_hashcode))
    print("""
    S57 - {0}
    FTTP Filename:     {2}
    Cell Filename:     {3}
    Filesize:          {4} Bytes
    Date Download:     {0}
    Datetime Created:  {5}
    Datetime Modified: {6}
    MD5 Hash:          {7}
    """.format(new_download_date, new_cell_name, new_fttp_name, new_cell_filename,  new_size, new_create_date,
               new_mod_date, new_md5_hashcode))




    print("{:-^80}".format("Comparison"))
    if old_size == new_size:
        print("Size: No Change")
    elif old_size >= new_size:
        print("Size: New file from {} is larger by {} bytes".format(old_download_date, old_size - new_size))
    elif old_size <= new_size:
        print("Size: Old file from {} is larger by {} bytes".format(new_download_date, new_size - old_size))

    if old_create_date == new_create_date:
        print("Datetime Created: No Change")
    else:
        print("Datetime Created: New Creation Date")

    if old_mod_date == new_mod_date:
        print("Datetime Modified: No Change")
    else:
        print("Datetime Modified: New Modification Date")

    if old_file_check['md5_hash'] == new_file_check['md5_hash']:
        print("MD5 Checksum: Match")
    else:
        print("MD5 Checksum: No Match")
print('='*80)

process_done()

delete_config = False
count = 0
while delete_config is False:
    delete_command = input("Do you wish to delete the Config file? (Y/N)")
    if delete_command.upper() == 'Y':
        os.remove(config_path)
        sys.exit()
    elif delete_command.upper() == 'N':
        sys.exit()
    else:
        print("Incorrect Input")