import os
import argparse
import logging

from detector import SimilarFilesDetector
from utils import get_directory_files, ArgParseRangeType, ArgParseDirectoryType


def main():
    """Main function.
    """
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s :: %(name)s :: %(module)s :: %(levelname)s :: %(message)s")
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', metavar="path", type=ArgParseDirectoryType(),
                        help="Directory where files are located.", required=True)
    parser.add_argument('-n', '--name-distance-threshold', type=float, choices=ArgParseRangeType(0.0, 1.0),
                        help="The threshold used in the name distance.", required=False, default=0.0)
    parser.add_argument('-f', '--fuzzy-hash-distance-threshold', type=float, choices=ArgParseRangeType(0.0, 1.0),
                        help="The threshold used in the fuzzy hash distance.", required=False, default=0.0)
    parser.add_argument('-s', '--size-distance-threshold',  type=float, choices=ArgParseRangeType(0.0, 1.0),
                        help="The threshold used in the file size distance.", required=False, default=0.0)

    # Parse and check args.
    args = vars(parser.parse_args())

    logging.info("Starting CLI...")

    logging.info(f"Retrieving all files from directory '{args['directory']}'...")
    files = get_directory_files(args["directory"])
    logging.info(f"Number of files found: {len(files)}.")

    logging.info("Running detector to identify similar files...")
    detector = SimilarFilesDetector(**args)
    similar_files = detector.detect_similar_files(files, progress_bar=True)

    if similar_files:
        logging.info("Report with similars found: ")
        print("*" * 80)
        similars_filepaths = []
        for filename, result in similar_files.items():
            base_file_values = {"hash": result['hash'], "file_size": result['size']}
            print(filename, f"({base_file_values})")
            for similar_filename, values in result["similar_files"].items():
                print(" ", similar_filename, f"({values})")
                similars_filepaths.append(os.path.join(args["directory"], similar_filename))
        print("*" * 80)
        logging.info(f"Number of similar files found: {len(similars_filepaths)}.")

    else:
        logging.info("No similar files found.")

    logging.info("CLI Finished.")


if __name__ == "__main__":
    main()
