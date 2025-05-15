from concurrent.futures import ThreadPoolExecutor
from threading import Lock

class DataSingleton:
    _instance = None

    _lock = Lock()  # Ensures thread-safe singleton instantiation

    def __new__(cls, data_dict=None):
        with cls._lock:  # Thread-safe initialization
            if cls._instance is None:
                cls._instance = super(DataSingleton, cls).__new__(cls)
                cls._instance._data_store = {}
                if data_dict:
                    cls._instance._load_all_data_parallel(data_dict)
        return cls._instance

    def _load_all_data_parallel(self, data_dict):
        """
        Load and preprocess all datasets in parallel.
        :param data_dict: A dictionary where keys are dataset names and values are file paths.
        """
        def process_dataset(name, file_path):
            preprocessing_class = self._select_preprocessing_class(name)
            return name, preprocessing_class.load_and_preprocess(file_path)

        # Use ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor() as executor:
            results = executor.map(lambda item: process_dataset(*item), data_dict.items())

        # Store results in the shared data store
        for name, data in results:
            self._data_store[name] = data

    def _select_preprocessing_class(self, name):
        """
        Select the appropriate preprocessing class based on the dataset name.
        """
        if 'Sweden' in name:
            from utils.datasets.sweden import SwedenPreprocessing
            return SwedenPreprocessing
        elif 'India' == name:
            from utils.datasets.india import IndiaPreprocessing
            return IndiaPreprocessing
        elif 'Mexico' == name:
            from utils.datasets.mexico import MexicoPreprocessing
            return MexicoPreprocessing
        elif 'Calihome' in name:
            from utils.datasets.cali import CaliPreprocessing
            return CaliPreprocessing
        elif 'Caliapt' in name:
            from utils.datasets.cali2 import CaliAptPreprocessing
            return CaliAptPreprocessing
        elif 'Italy' in name:
            from utils.datasets.italy import ItalyPreprocessing
            return ItalyPreprocessing
        else:
            raise ValueError(f"No preprocessing class defined for the dataset {name}")

    def get_data(self, dataset_name):
        """
        Retrieve the data for a specific dataset.
        """
        if dataset_name not in self._data_store:
            raise ValueError(f"Dataset {dataset_name} not found.")
        return self._data_store[dataset_name]
