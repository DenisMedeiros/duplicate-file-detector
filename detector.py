import os
import ssdeep
import logging
import mpire
import jellyfish


class SimilarFilesDetector(object):

    def __init__(self, name_distance_threshold: float, fuzzy_hash_distance_threshold: float,
                 size_distance_threshold: float, *args, **kwargs):
        """Constructor for similar files detector.

        Args:
            name_distance_threshold (float): The threshold for file name distance (between 0 and 1).
            fuzzy_hash_distance_threshold (float): The threshold for file name distance (between 0 and 1).
            size_distance_threshold (float): The threshold for file name distance (between 0 and 1).
        """
        self.name_distance_threshold = name_distance_threshold
        self.fuzzy_hash_distance_threshold = fuzzy_hash_distance_threshold
        self.size_distance_threshold = size_distance_threshold

    def get_file_info(self, filepath: str) -> dict:
        """Generates the fuzzy hash and gets the file size for the given file.

        Args:
            filepath (str): The path for the file.

        Returns:
            str: The fuzzy hash.
        """
        return {"hash": ssdeep.hash_from_file(filepath), "size": os.path.getsize(filepath)}

    def find_similar_files(self, context: dict, i: int) -> dict:
        """Helper function used in worker to find similar files.

        Args:
            context (dict): The context with the list of names and hashes.
            i (int): The index for the current item.

        Returns:
            dict: The dict with all similar files.
        """
        names = context["names"]
        files_info = context["files_info"]
        name1 = names[i]
        hash1 = files_info[i]["hash"]
        size1 = files_info[i]["size"]
        similars = {}
        for j in range(i+1, len(names)):
            name2 = names[j]
            hash2 = files_info[j]["hash"]
            size2 = files_info[j]["size"]
            # Compare the name, hashes, and size to calculate the distance (1 is the max of similarity).
            name_distance = jellyfish.jaro_winkler_similarity(name1, name2)
            hash_distance = jellyfish.jaro_winkler_similarity(hash1, hash2)
            size_distance = 1 - abs((size1 - files_info[j]["size"])/size1)
            # Include the current only if the distances are higher than the given threshold.
            if (name_distance >= self.name_distance_threshold and
                    hash_distance >= self.fuzzy_hash_distance_threshold and
                    size_distance >= self.size_distance_threshold):
                similars[name2] = {
                    "hash": hash2,
                    "size": size2,
                    "name_distance": round(name_distance, 3),
                    "hash_distance": round(hash_distance, 3),
                    "size_distance": round(size_distance, 3)
                }
        return similars

    def detect_similar_files(self, files: list[os.DirEntry], progress_bar: bool = False) -> dict:
        """Detects all similar files based on hash.

        Args:
            files (list[os.DirEntry]): _description_
            progress_bar (bool, optional): _description_. Defaults to False.

        Returns:
            dict: _description_
        """
        names = [entry.name for entry in files]
        filepaths = [entry.path for entry in files]

        # Use half the number of CPUs to process the tasks if the number of files is too large,
        # otherwise use only 2 jobs.
        if len(names) > 100:
            # Define number of jobs based on number of files to process.
            n_jobs = mpire.cpu_count() // 2
        else:
            n_jobs = 2

        logging.info("Getting information all files (fuzzy hash, file size)...")
        with mpire.WorkerPool(n_jobs=n_jobs) as pool:
            files_info = pool.map(self.get_file_info, filepaths, progress_bar=progress_bar)

        context = {
            "names": names,
            "files_info": files_info
        }
        logging.info("Comparing all files and their information...")
        with mpire.WorkerPool(n_jobs=n_jobs, shared_objects=context) as pool:
            results = pool.map(self.find_similar_files, range(len(files)), progress_bar=progress_bar)

        # Prepare report.
        similar_files = {}
        for i, result in enumerate(results):
            if not result:
                continue
            similar_files[names[i]] = {
                "hash": files_info[i]["hash"],
                "size": files_info[i]["size"],
                "similar_files": result
            }
        return similar_files
