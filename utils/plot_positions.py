"""
utility script to check why velocity for some entities seem to get a bump
possibly when collisions between other planets occur
"""

import sys

from matplotlib import pyplot as plt

from extract_data import get_data_from


if len(sys.argv) == 2:
    filename = sys.argv[1]
else:
    filename = "2020-Nov-23 22:46.log"

dataset = get_data_from(filename)

### plot velocities
max_id = max([line[3] for line in dataset])
for id in range(1, max_id + 1):
    vals = [line[1] for line in dataset if line[3] == id]

    plt.figure()
    # each y entry thus looks like this: [num, num, num]
    plt.plot([val[0] for val in vals], [val[1] for val in vals])
    plt.xlabel("x (m)")
    plt.xlim([0, 1024])
    plt.ylabel("y (m)")
    plt.ylim([0, 768])
    plt.title(f"Object {id}")
    plt.show()
