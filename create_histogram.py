import json
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    with open("training_report.json") as jsonfile:
        from_json = json.load(jsonfile)
        values = np.array(list(from_json.values()))
        values = values.__abs__()
        fig,ax = plt.subplots()
        
        ax.hist(values, bins=200 )
        # ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_ylabel('Number of detections')
        ax.set_xlabel('Error (s)')
        ax.set_title(f'Histogram of error relative to marked start over the training dataset', fontweight='bold')
        plt.show()
        
