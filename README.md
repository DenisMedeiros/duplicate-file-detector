# similar-files-detector

This is a simple tool to detect similar (or identical) files based on 3 techniques:

- Similarity of filenames by employing the Jaro-Winkler distance.
- Similarity of Computing Triggered Piecewise Hashes (CTPH) - also known as fuzzy hashes - by employing the Jaro-Winkler distance on the hashes.
- Similarity of file sizes by calculating the relative percent error and subtracting it from 1.

All these techniques generate a numerical metric from 0 to 1.0, where 1.0 means the files are as similar as possible.

## Dependencies

### System Libraries

The Python library `ssdeep` depends on some system dependencies. To install it in Linux, please check the installation instructions at:

https://python-ssdeep.readthedocs.io/en/latest/installation.html

If you are using Windows, then you may need to use the pre-compiled library and DLL from:

https://github.com/MacDue/ssdeep-windows-32_64

### Python Libraries

After installing the system libraries, install the Python libraries in a virtual environment by runing:

```bash
python3 -m venv venv/
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

This tool works by receiving a directory as argument and then processing all files on the top level of it (sub-directories are ignored). It will then print out the similar files found according to the given thresholds, which are:

- **Filename threshold**: Used in the similarity of filenames.
- **Hash threshold**: Used in the similarity of fuzzy hashes.
- **File size threshold**: Used in the similarity of file sizes.

These thresholds can have values from 0.0 to 1.0 inclusive, have default value 0,0, and are combined with `AND` logic. That means if you select the thresholds 0.5, 0.6, and 0.7 for filename, hash, and size respectively, then only files that has a similarity for all those values simultaneously are detected. If you want toi check only the hash similarity, for example, leave the other values in blank or set them to 0.

### CLI

To see all possible parameters, run the help option the `cli.py`:

```bash
$ python3 cli.py -h
usage: cli.py [-h] -d path [-n {[0.0,1.0]}] [-f {[0.0,1.0]}] [-s {[0.0,1.0]}]

options:
  -h, --help            show this help message and exit
  -d path, --directory path
                        Directory where files are located.
  -n {[0.0,1.0]}, --name-distance-threshold {[0.0,1.0]}
                        The threshold used in the name distance.
  -f {[0.0,1.0]}, --fuzzy-hash-distance-threshold {[0.0,1.0]}
                        The threshold used in the fuzzy hash distance.
  -s {[0.0,1.0]}, --size-distance-threshold {[0.0,1.0]}
                        The threshold used in the file size distance.
```

Example of detecting files with similar fuzzy hashes (threshold > 0.7) in the folder `/tmp/files`:

```bash
python3 cli.py --directory /tmp/files/ --fuzzy-hash-distance-threshold=0.7
```

Example of detecting similar files in all possible metrics:

```bash
python3 cli.py --directory /tmp/files/ \
  --name-distance-threshold=0.5 \
  --fuzzy-hash-distance-threshold=0.7 \
  --size-distance-threshold=0.9
```

### GUI

To be implemented in the future.

## References

https://en.wikipedia.org/wiki/Fuzzy_hashing

https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance

https://en.wikipedia.org/wiki/Relative_change

https://github.com/jamesturk/jellyfish

https://github.com/DinoTools/python-ssdeep
