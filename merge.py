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


# Remove ranking from filename
def remove_ranking(name):
    info = parse_filename(name)
    if info['singer']:
        return "%s - %s.mp3" % (info['singer'], info['title'])
    else:
        return name


# Normalize string
# Removes whitespace, special characters
def normailze(name):
    return re.sub('[^A-Za-z0-9가-힣]', '', name)


# Copy or move mp3 files from src to dest directory
def copy_mp3_files(src, dest, move):
    dest_filenames = get_filenames(dest, "*.mp3")
    dest_normalized_filenames = map(lambda x: normailze(x), dest_filenames)

    for filename in get_filenames(src, "*.mp3"):
        new_filename = remove_ranking(filename)
        normalized = normailze(new_filename)
        src_path = os.path.join(src, filename)

        # skip copy/move if exists
        if normalized in dest_normalized_filenames:
            print("[SKIP] %s" % filename)
            continue

        # copy/move
        dest_path = os.path.join(dest, new_filename)
        print("[%s] %s => %s" % ("MOVE" if move else "COPY", filename, new_filename))
        if move:
            shutil.move(src_path, dest_path)
        else:
            shutil.copyfile(src_path, dest_path)

parser = argparse.ArgumentParser(description='Move mp3 files to another directory')
parser.add_argument('--src', help='source directory', default='./')
parser.add_argument('--dest', help='destination directory', required=True)
parser.add_argument('--move', help='move file', action='store_true')
args = parser.parse_args()

print("source dir : %s" % args.src)
print("destination dir : %s" % args.dest)

copy_mp3_files(os.path.abspath(args.src), os.path.abspath(args.dest), args.move)
