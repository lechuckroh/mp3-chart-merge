import argparse
import errno
import glob
import os
import re
import shutil


# make sure path exists
def mkdirs(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise


# get filenames with matching pattern in given path
def get_filenames(path, pattern):
    cwd = os.getcwd()
    os.chdir(path)
    filenames = glob.glob(pattern)
    os.chdir(cwd)
    return filenames


# parse filename and return dictionary
def parse_filename(name):
    search = re.search('(^\d*)\.?([^-]*)-?(.*)', name, re.IGNORECASE)
    if search:
        rank = search.group(1).strip()
        artist = search.group(2).strip()
        title = search.group(3).strip()
        # case : '-' separator not found
        if not title:
            artist, title = '', artist
        return {
            'rank': rank,
            'artist': artist,
            'title': title
        }
    else:
        return {'title': name}


# Remove ranking from filename
def remove_ranking(name):
    basename = name[:-4]
    info = parse_filename(basename)
    if info['artist']:
        return "%s - %s.mp3" % (info['artist'], info['title'])
    else:
        return "%s.mp3" % info['title']


# Normalize string
# Removes whitespace, special characters
def normailze(name):
    pass1 = re.sub('\(.*\)', '', name.lower())
    pass2 = re.sub('[^A-Za-z0-9가-힣]', '', pass1)
    return pass2


# get normalized filenames in given path
def get_normalized_filenames(path):
    filenames = get_filenames(path, "*.mp3")
    normailzed = map(lambda x: normailze(x), filenames)
    return set(normailzed)


# Copy or move mp3 files from src to dest directory
def copy_mp3_files(src, dest, move):
    header = "MOVE" if move else "COPY"
    print("%s => %s" % (src, dest))

    mkdirs(dest)
    dest_filenames = get_normalized_filenames(dest)

    for filename in get_filenames(src, "*.mp3"):
        new_filename = remove_ranking(filename)
        normalized = normailze(new_filename)
        src_path = os.path.join(src, filename)

        # skip copy/move if exists
        if normalized in dest_filenames:
            continue

        # copy/move
        dest_path = os.path.join(dest, new_filename)
        print("[%s] %s => %s : %s" % (header, filename, new_filename, normalized))
        if move:
            shutil.move(src_path, dest_path)
        else:
            shutil.copyfile(src_path, dest_path)


parser = argparse.ArgumentParser(description='Move mp3 files to another directory')
parser.add_argument('--src', help='source directory', default='./')
parser.add_argument('--dest', help='destination directory', required=True)
parser.add_argument('--move', help='move file', action='store_true')
args = parser.parse_args()

dest_dir = os.path.abspath(args.dest)
wildcard_src = True if any(ch in args.src for ch in ['?', '*']) else False

if wildcard_src:
    src_parent = os.path.dirname(args.src)
    src_pattern = os.path.basename(args.src)
    for d in get_filenames(src_parent, src_pattern):
        copy_mp3_files(os.path.abspath(os.path.join(src_parent, d)),
                       dest_dir,
                       args.move)
else:
    copy_mp3_files(os.path.abspath(args.src),
                   dest_dir,
                   args.move)
