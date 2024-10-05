import os
from scipy.signal import correlate
from bisect_moonquake import CAT_LUNAR, LUNAR_DATA_DIR, PREPROCESSED_LUNAR_DIR, from_mseed
from datetime import datetime
import create_matched_filter
import matplotlib.pyplot as plt
from pathlib import Path
from tqdm import tqdm

IMGDIR = "./images"
def main():
    matched_filter = create_matched_filter.create_matched_filter()
    outfolder = Path(IMGDIR + "/lunar/training/")
    outfolder.mkdir(parents=True, exist_ok=True)
    for row in tqdm(CAT_LUNAR.iloc):
        arrival_time = datetime.strptime(row['time_abs(%Y-%m-%dT%H:%M:%S.%f)'],'%Y-%m-%dT%H:%M:%S.%f')
        test_filename = row.filename
        try:
            st, arrival = from_mseed(test_filename, LUNAR_DATA_DIR, arrival_time)
        except FileNotFoundError:
            # Because csv is faulty...
            test_filename = test_filename.replace('HR00', 'HR02')
            st, arrival = from_mseed(test_filename, LUNAR_DATA_DIR, arrival_time)
        st.traces[0].data *= 1 / st.traces[0].data.max()
        st.traces[0].decimate(3)
        likelyhood = correlate(st.traces[0].data, matched_filter, mode='same')
        estimated_arrival = (likelyhood.argmax() - matched_filter.shape[0] / 2) * st.traces[0].stats.delta
        print(arrival - estimated_arrival)
        # Plot trace
        outfile = outfolder.joinpath(test_filename + "_correlation.svg")
        fig,ax = plt.subplots(1,1,figsize=(10,3))
        ax.plot(st.traces[0].times(), likelyhood)
        ax.axvline(x = arrival, color='red',label='Rel. Arrival')
        ax.axvline(x = estimated_arrival, color='green',label='Est. Arrival')
        # plt.show()
        plt.savefig(outfile)


if __name__ == "__main__":
    main()
