from sys import argv
from os import listdir, mkdir, rename
from os.path import isfile, join, isdir, exists
from shutil import copytree, rmtree
import re
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("directory", type=str, help="directory to categorize")
ap.add_argument("-w", "--whitelist", type=str, required=False, help="whitelist comma sepparated no space")
ap.add_argument("-b", "--blacklist", type=str, required=False, help="blacklist")
args = vars(ap.parse_args())

whitelist = []
blacklist = []
if args["whitelist"]:
    whitelist = args["whitelist"].split(",")
if args["blacklist"]:
    blacklist = args["blacklist"].split(",")

print(whitelist, blacklist)

start_path = "./%s__%s"%(argv[1], "workcopy")

if not exists(argv[1]):
    raise Exception("Dir does not exist!")

print(exists(start_path))
if exists(start_path):
        rmtree(start_path)

copytree("./%s"%(argv[1]), start_path)

found_count = 0

def find_files(folder_path, files):
    global found_count, whitelist, blacklist
    for f in sorted(listdir(folder_path)):
        if isfile(join(folder_path, f)):
            ext = re.search("\.[0-9a-zA-Z]+$", f)
            if not ext:
                ext = ""
            else:
                ext = ext.group()[1:].lower()
                # print(files, ext)
                if ext in whitelist or len(whitelist) == 0 and ext not in blacklist:
                    if not ext in files:
                        files[ext] = []

                    files[ext].append([join(folder_path, f), f])
                    found_count += 1
        else:
            files = find_files(join(folder_path, f), files)

    return files



ordered_files = find_files(start_path, {})
print("Found %s files!"%found_count)
move_count = 0


def move_files(out_folder, files):
    global move_count
    if not exists(out_folder):
        mkdir(out_folder)

    for key, val in files.items():
        key_path = join(out_folder, key)
        if not exists(key_path):
            mkdir(key_path)

        for v in val:
            rename(v[0], join(key_path, v[1]))
            move_count += 1



move_files("./%s_categorized_data"%argv[1], ordered_files)
print("Moved %s files!"%move_count)
rmtree(start_path)
