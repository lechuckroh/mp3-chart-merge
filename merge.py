import argparse
import glob
import os
import re
import shutil


# get filenames with matching pattern in given path
def get_filenames(path, pattern):
    os.chdir(path)
    return glob.glob(pattern)


# parse filename and return dictionary
def parse_filename(name):
    search = re.search('(^\d+)\.?(.*)-(.*).mp3', name, re.IGNORECASE)
    if search:
        return {
            'rank': search.group(1),
            'singer': search.group(2).strip(),
            'title': search.group(3).strip()
        }
    else:
        return {'title': name}


def copy_mp3_files(src, dest, move):
    for filename in get_filenames(src, "*.mp3"):
        info = parse_filename(filename)
        if info['singer']:
            new_filename = "%s - %s.mp3" % (info['singer'], info['title'])
        else:
            new_filename = filename
        src_path = os.path.join(src, filename)
        dest_path = os.path.join(dest, new_filename)
        if move:
            print("[MOVE] %s => %s" % (src_path, dest_path))
            shutil.move(src_path, dest_path)
        else:
            print("[COPY] %s => %s" % (src_path, dest_path))
            shutil.copyfile(src_path, dest_path)


parser = argparse.ArgumentParser(description='Move mp3 files to another directory')
parser.add_argument('--src', help='source directory', default='./')
parser.add_argument('--dest', help='destination directory', required=True)
parser.add_argument('--move', help='move file', action='store_true')
args = parser.parse_args()

print("source dir : %s" % args.src)
print("destination dir : %s" % args.dest)

copy_mp3_files(os.path.abspath(args.src), os.path.abspath(args.dest), args.move)
