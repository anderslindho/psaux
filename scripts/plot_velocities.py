"""
utility script to check velocities of entities
"""

import sys
from math import sqrt, ceil

from matplotlib import pyplot as plt

from extract_data import get_data_from


if len(sys.argv) == 2:
    filename = sys.argv[1]
else:
    filename = "../2020-Nov-25 20:17.log"

dataset = get_data_from(filename)

### plot velocities
max_id = max([line[3] for line in dataset])
time_start = min([line[0] for line in dataset if line[3] == 1])
time_end = max([line[0] for line in dataset if line[3] == 1])

fig, axs = plt.subplots(5, 5)
axs = axs.flatten()
for i in range(max_id):
    velocity = [line[2] for line in dataset if line[3] == i + 1]
    time = [line[0] - time_start for line in dataset if line[3] == i + 1]

    for j, char in enumerate(["x", "y"]):
        axs[i].plot(time, [direction[j] for direction in velocity], label=char)
        axs[i].set_xlim(0, time_end - time_start)

fig.show()
