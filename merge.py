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


# get normalized filenames in given path
def get_normalized_filenames(path):
    filenames = get_filenames(path, "*.mp3")
    normailzed = map(lambda x: normailze(x), filenames)
    return set(normailzed)


# Copy or move mp3 files from src to dest directory
def copy_mp3_files(src, dest, move):
    header = "MOVE" if move else "COPY"
    print("[%s] %s => %s" % (header, src, dest))

    dest_filenames = get_normalized_filenames(dest)

    for filename in get_filenames(src, "*.mp3"):
        new_filename = remove_ranking(filename)
        normalized = normailze(new_filename)
        src_path = os.path.join(src, filename)

        # skip copy/move if exists
        if normalized in dest_filenames:
            print("[SKIP] %s" % filename)
            continue

        # copy/move
        dest_path = os.path.join(dest, new_filename)
        print("[%s] %s => %s" % (header, filename, new_filename))
        if move:
            shutil.move(src_path, dest_path)
        else:
            shutil.copyfile(src_path, dest_path)


parser = argparse.ArgumentParser(description='Move mp3 files to another directory')
parser.add_argument('--src', help='source directory', default='./')
parser.add_argument('--dest', help='destination directory', required=True)
parser.add_argument('--move', help='move file', action='store_true')
parser.add_argument('--regex', help='source directory regular expression')
args = parser.parse_args()

dest_dir = os.path.abspath(args.dest)
if args.regex:
    for d in get_filenames(args.src, args.regex):
        copy_mp3_files(os.path.abspath(os.path.join(args.src, d)),
                       dest_dir,
                       args.move)
else:
    copy_mp3_files(os.path.abspath(args.src),
                   dest_dir,
                   args.move)
