"""Create the matched filter for correlational detection"""
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

from bisect_moonquake import CAT_LUNAR, PREPROCESSED_LUNAR_DIR, from_mseed

FILTER_SHAPE = [46376 // 3 + 1,] # I want it that way

def create_matched_filter():
    matched_filter = np.zeros(FILTER_SHAPE, 'O')
    type_collection = CAT_LUNAR
    for row in type_collection.iloc:
        arrival_time = datetime.strptime(row['time_abs(%Y-%m-%dT%H:%M:%S.%f)'],'%Y-%m-%dT%H:%M:%S.%f')
        sample_filename = row.filename + "_trimmed_7000_sec"
        try:
            st, _ = from_mseed(sample_filename, PREPROCESSED_LUNAR_DIR, arrival_time)
        except FileNotFoundError:
            # Because csv is faulty...
            sample_filename = sample_filename.replace('HR00', 'HR02')
            st, _ = from_mseed(sample_filename, PREPROCESSED_LUNAR_DIR, arrival_time)
        st.traces[0].data *= 1 / st.traces[0].data.max()
        st.traces[0].decimate(3)
        try:
            matched_filter += st.traces[0].data
        except:
            # print(st.traces[0].data.shape)
            pass
        # # Plot trace
        # fig,ax = plt.subplots(1,1,figsize=(10,3))
        # ax.plot(matched_filter)
        # plt.show()
    return matched_filter

if __name__ == "__main__":
    create_matched_filter()
