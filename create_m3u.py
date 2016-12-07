import argparse
import glob
import os


# list mp3 filenames in the given path sorted by filename
def list_mp3_filenames(path):
    cwd = os.getcwd()
    os.chdir(path)
    filenames = glob.glob('*.mp3')
    filenames.sort()
    os.chdir(cwd)
    return filenames


# create m3u file
def create_m3u(dest, filenames):
    f = open(dest, 'w')
    f.write("#EXTM3U\r\n")
    for filename in filenames:
        f.write("%s\r\n" % filename)
    f.close()
    print("[OK] %s created" % dest)


parser = argparse.ArgumentParser(description='Create m3u file')
parser.add_argument('directory', metavar='dir', help='mp3 directory')
args = parser.parse_args()
arg = args.directory

if os.path.isdir(arg):
    l = list_mp3_filenames(arg)
    if not l:
        print("[WARN] *.mp3 not found in '%s' directory" % arg)
    else:
        basename = os.path.basename(os.path.abspath(arg))
        create_m3u(os.path.join(arg, "%s.m3u" % basename), l)
else:
    print("[ERROR] directory not found : %s" % arg)
