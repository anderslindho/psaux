"""
utility script to check velocities of entities
"""

import sys

from matplotlib import pyplot as plt

from extract_data import get_data_from


if len(sys.argv) == 2:
    filename = sys.argv[1]
else:
    filename = "../2020-Nov-23 22:46.log"

dataset = get_data_from(filename)

### plot velocities
max_id = max([line[3] for line in dataset])
time_start = min([line[0] for line in dataset if line[3] == 1])
time_end = max([line[0] for line in dataset if line[3] == 1])
for id in range(1, max_id + 1):
    yvals = [line[2] for line in dataset if line[3] == id]
    xvals = [line[0] - time_start for line in dataset if line[3] == id]

    plt.figure()
    # each y entry thus looks like this: [num, num, num]
    for i, char in enumerate(["x", "y"]):
        plt.plot(xvals, [_y[i] for _y in yvals], label="%s" % char)
    plt.legend()
    plt.xlabel("time (s)")
    plt.xlim(0, time_end - time_start)
    plt.ylabel("velocity (m/s)")
    plt.title(f"Object {id}")
    plt.show()
