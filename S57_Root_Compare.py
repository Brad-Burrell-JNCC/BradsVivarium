import hashlib
import os
import datetime

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
            "md5_hash":md5_hash}


paths_to_files = [r'J:\GISprojects\Marine\UKHOS57\Data\20230620\UKHO-S57 23-06-20\ENC_ROOT.zip',
                  r"J:\GISprojects\Marine\UKHOS57\Data\20230803\UKHO-S57 27-06-23\ENC_ROOT.zip"]

og_file = file_checker(paths_to_files[0])
new_file = file_checker(paths_to_files[1])
print('='*80)
print("""
S57 2023 Original
Download Date:     {}
FTTP Filename:     {}
Filesize:          {} Bytes
Datetime Created:  {}
Datetime Modified: {}
MD5 Hash:          {}\n""".format(og_file['file_path'].split('\\')[5],
                                  og_file['file_path'].split('\\')[6],
                                  og_file['file_size'],
                                  datetime.datetime.fromtimestamp(og_file['create_time']).strftime('%Y-%m-%d %H:%M:%S'),
                                  datetime.datetime.fromtimestamp(og_file['mod_time']).strftime('%Y-%m-%d %H:%M:%S'),
                                  og_file['md5_hash']))
print('-'*80)
print("""
S57 2023 FTTP Latest
Download Date:     {}
FTTP Filename:     {}
Filesize:          {} Bytes
Datetime Created:  {}
Datetime Modified: {}
MD5 Hash:          {}\n""".format(new_file['file_path'].split('\\')[5],
                                  new_file['file_path'].split('\\')[6],
                                  new_file['file_size'],
                                  datetime.datetime.fromtimestamp(new_file['create_time']).strftime('%Y-%m-%d %H:%M:%S'),
                                  datetime.datetime.fromtimestamp(new_file['mod_time']).strftime('%Y-%m-%d %H:%M:%S'),
                                  new_file['md5_hash']))
print("{:-^80}".format("MD5 Comparison"))
if og_file['md5_hash'] == new_file['md5_hash']:
    print("MD5 Hash Match, File are Identical, No Rework")
else:
    print("MD5 Hash Match, File are Not Identical, Rework Needed")
print('='*80)
