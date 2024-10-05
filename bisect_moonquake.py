"""Cut out relevant samples from the training set"""
import pandas as pd
from obspy import UTCDateTime, read
from datetime import datetime, timedelta
import os
from pathlib import Path
from tqdm import tqdm


# Define directories for use
CAT_LUNAR_DIR = './space_apps_2024_seismic_detection/data/lunar/training/catalogs/'
CAT_LUNAR_FILE = CAT_LUNAR_DIR + 'apollo12_catalog_GradeA_final.csv'
CAT_LUNAR = pd.read_csv(CAT_LUNAR_FILE)
LUNAR_DATA_DIR = './space_apps_2024_seismic_detection/data/lunar/training/data/S12_GradeA/'
PREPROCESSED_LUNAR_DIR = './preprocessed/lunar/data/'

def from_mseed(test_filename:str, data_directory:str, arrival_time:datetime):
    mseed_file = f'{data_directory}{test_filename}.mseed'
    st = read(mseed_file)
    # This is how you get the data and the time, which is in seconds
    tr = st.traces[0].copy()
    # Start time of trace (another way to get the relative arrival time using datetime)
    starttime = tr.stats.starttime.datetime
    arrival = (arrival_time - starttime).total_seconds()
    return st, arrival

if __name__ == "__main__":
    # Make output dir if not present
    Path(PREPROCESSED_LUNAR_DIR).mkdir(parents=True, exist_ok=True)

    # Iterate over all lunar samples and extract arrival:arrival + 7000 sec of samples
    for row in tqdm(CAT_LUNAR.iloc):
        arrival_time = datetime.strptime(row['time_abs(%Y-%m-%dT%H:%M:%S.%f)'],'%Y-%m-%dT%H:%M:%S.%f')
        test_filename = row.filename
        try:
            st, arrival = from_mseed(test_filename, LUNAR_DATA_DIR, arrival_time)
        except FileNotFoundError:
            # Because csv is faulty...
            test_filename = test_filename.replace('HR00', 'HR02')
            st, arrival = from_mseed(test_filename, LUNAR_DATA_DIR, arrival_time)

        stream_out = st.copy()
        utc_arrival = UTCDateTime(arrival_time)
        endtime = UTCDateTime(arrival_time + timedelta(seconds=7000))
        stream_out.trim(utc_arrival, endtime)
        fout_name = test_filename + "_trimmed_7000_sec.mseed"
        stream_out.write(os.path.join(PREPROCESSED_LUNAR_DIR, fout_name), format="mseed")

