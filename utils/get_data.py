from utils.datasets.data_singleton import DataSingleton

def get_cali():
    cali_path = '/home/lvu/playground/data/California-homes/IAQ_Monitoring/'
    import glob, os
    file_paths = glob.glob(os.path.join(cali_path, '*.csv'))
    return {f'Calihome{index}': file_path for index, file_path in enumerate(file_paths)}

def get_cali2():
    cali_path = '/home/lvu/playground/data/California-apt/IAQ_Activity_Monitoring/'
    import glob, os
    file_paths = glob.glob(os.path.join(cali_path, '*.csv'))
    return {f'Caliapt{index}': file_path for index, file_path in enumerate(file_paths)}

def get_sweden():
    return {
        'Sweden Bedroom': '/home/lvu/playground/data/Sweden/IAQbedroom.txt',
        'Sweden Livingroom': '/home/lvu/playground/data/Sweden/IAQlivingroom.txt',
    }

def get_italy():
    return {
        'Italy1': '/home/lvu/playground/data/Italy-airport/gold.csv',
        'Italy2': '/home/lvu/playground/data/Italy-airport/silver.csv',
        'Italy3': '/home/lvu/playground/data/Italy-airport/brown.csv',
    }
    
def get_data():
    """
    Get the data singleton containing all datasets.
    :return: DataSingleton instance with all datasets loaded.
    """
    data_dict = {
        # 'Sweden': '/home/lvu/playground/data/Sweden/IAQbedroom.txt',
        'India': '/home/lvu/playground/data/india.csv',
        'Mexico': '/home/lvu/playground/data/Mexico/per-hour.xlsx'
    }
    cali_data = get_cali()
    caliapt_data = get_cali2()
    sweden_data = get_sweden()
    italy_data = get_italy()

    data_dict = {**data_dict, **sweden_data, **cali_data, **caliapt_data, **italy_data}

    data_singleton = DataSingleton(data_dict)
    return data_singleton

if __name__ == "__main__":
    get_data()
