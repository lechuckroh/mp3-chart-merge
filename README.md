# mp3 chart merge

[한국어](README-kr.md)

This script removes the ranking from the mp3 filename and moves to another directory.


For example, the following command will move mp3 files from `src` directory to `dest` directory.

```bash
$ python merge.py --src ./Billboard.2016.12.02 --dest ./Billboard.2016 --move
```

```
[SRC] Billboard.2016.12.02/
 - 001.Black Beatles - Rae Sremmurd (feat. Gucci Mane).mp3
 - 002.The Chainsmokers feat. Halsey - Closer.mp3

[DEST] Billboard.2016/
 - Black Beatles - Rae Sremmurd (feat. Gucci Mane).mp3
 - The Chainsmokers feat. Halsey - Closer.mp3
```

### source filename pattern

```
${ranking} ${artist}-${title}.mp3
${ranking}. ${artist}-${title}.mp3
```

There can be a space between each token.

### destination filename pattern

```
${artist} - ${title}.mp3
```

### filename comparison rule

* spaces and special characters are ignored.
* characters inside `()` are ignored.
* filename comparison is not case-sensitive.

## Requirements

* [Python 3.x](https://www.python.org/downloads/)

## Command line options

### `--src dir` 

Source mp3 directory.

Wild card can be used.

### `--dest dir`

Target mp3 directory.

### `--move`

Optional.

mp3 files will be moved to `dest` directory if specified.

Duplicate mp3 files are skipped without moving.

### Example

```bash
# mp3 files in "mp3/Billboard 2016.*" directories will be moved to "mp3/Billboard 2016"
$ python merge.py --src "mp3/Billboard 2016.*" --dest "mp3/Billboard 2016" --move
```
