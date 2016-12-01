import argparse
import glob
import os
import re


# get filenames with matching pattern in given path
def get_filenames(path, pattern):
    os.chdir(path)
    return glob.glob(pattern)


def parse_filename(filename):
    search = re.search('(^\d+)\.?(.*)-(.*).mp3', filename, re.IGNORECASE)
    if search:
        return {
            'rank': search.group(1),
            'singer': search.group(2).strip(),
            'title': search.group(3).strip()
        }
    else:
        return {'title': filename}


parser = argparse.ArgumentParser(description='Move mp3 files to another directory')
parser.add_argument('--src', help='source directory', default='./')
parser.add_argument('--dest', help='destination directory', required=True)
args = parser.parse_args()

print("[MOVE] %s -> %s" % (args.src, args.dest))

files = get_filenames(args.src, "*.mp3")

for f in files:
    info = parse_filename(f)
    print("%s => %s" % (f, info))
