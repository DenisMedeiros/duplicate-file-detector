import os
import argparse


class ArgParseRangeType(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __eq__(self, other):
        return self.start <= other <= self.end

    def __contains__(self, item):
        return self.__eq__(item)

    def __iter__(self):
        yield self

    def __str__(self):
        return '[{0},{1}]'.format(self.start, self.end)

    def __repr__(self):
        return self.__str__()


class ArgParseDirectoryType(object):

    def __call__(self, value_string):
        if not os.path.isdir(value_string):
            raise argparse.ArgumentTypeError(f"The value '{value_string}' is not a valid directory.")
        if not os.access(value_string, os.R_OK):
            raise argparse.ArgumentTypeError(f"The directory '{value_string}' is not readable.")
        return value_string


def get_directory_files(directory: str) -> list[os.DirEntry]:
    """Returns the list of file entries in the given directory.

    Args:
        directory (str): The path for the directory.

    Returns:
        list[os.DirEntry]: The list with all files in the given directory.
    """
    # List all files in selected directory (ignore folders).
    files = [entry for entry in os.scandir(directory) if entry.is_file()]
    files.sort(key=lambda k: k.name)
    return files
