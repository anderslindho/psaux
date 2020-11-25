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

fig_vel, axs_vel = plt.subplots(5, 5)
axs_vel = axs_vel.flatten()
fig_pos, axs_pos = plt.subplots(5, 5)
axs_pos = axs_pos.flatten()

for i in range(max_id):
    time = [line[0] - time_start for line in dataset if line[3] == i + 1]
    position = [line[1] for line in dataset if line[3] == i + 1]
    velocity = [line[2] for line in dataset if line[3] == i + 1]

    for j, char in enumerate(["x", "y"]):
        axs_vel[i].plot(time, [direction[j] for direction in velocity], label=char)
        axs_vel[i].set_xlim(0, time_end - time_start)

    axs_pos[i].plot(
        [direction[0] for direction in position],
        [direction[1] for direction in position],
    )
    axs_pos[i].set_xlim(0, 1024)
    axs_pos[i].set_ylim(0, 768)

fig_vel.show()
fig_pos.show()
