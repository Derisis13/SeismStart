from os import path
from bisect_moonquake import from_mseed
import detect_moonquakes
import glob
from obspy import read
import create_matched_filter
from pathlib import Path
import matplotlib.pyplot as plt
import json
from tqdm import tqdm

def process_file(file: str, matched_filter, outfolder):
    st = read(file)
    arrival, likelyhood = detect_moonquakes.do_detection(st, matched_filter)
    outfile = outfolder.joinpath(path.basename(file) + "_correlation.svg")
    fig,ax = plt.subplots(1,1,figsize=(20,6))
    ax.plot(st.traces[0].times(), likelyhood)
    ax.axvline(x = arrival, color='green',label='Est. Arrival')
    ax.legend(loc='upper left')
    ax.set_ylabel('Likelyhood of activity')
    ax.set_xlabel('Time (s)')
    ax.set_title(f'Correlation of seismic data with average sample.', fontweight='bold')
    # plt.show()
    plt.savefig(outfile)
    plt.close(fig)
    return float(arrival)
    

def main():
    matched_filter = create_matched_filter.create_matched_filter()
    outfolder = Path(detect_moonquakes.IMGDIR + "/lunar/test/")
    outfolder.mkdir(parents=True, exist_ok=True)
    arrivals = {}
    for dir in glob.glob("./space_apps_2024_seismic_detection/data/lunar/test/data/*"):
        print(dir)
        for file in tqdm(glob.glob(path.join(dir, "*.mseed"))):
            arrival = process_file(file, matched_filter, outfolder)
            arrivals.update({file: arrival})
    with open("lunar_test_arrivals.json", "w") as jsonfile:
        json.dump(arrivals, jsonfile)



if __name__ == "__main__":
    main()
