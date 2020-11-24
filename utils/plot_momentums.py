"""
utility script to check why velocity for some entities seem to get a bump
possibly when collisions between other planets occur
"""

import ast
import re
import sys

from matplotlib import pyplot as plt

plot_all = True

if len(sys.argv) == 2:
    filename = sys.argv[1]
else:
    filename = "2020-Nov-23 22:46.log"

pattern = re.compile(
    r"^(\d*.\d*).+(?<=Object )(\d+).+(?<=self.velocity=)\w*\((\[[0-9.e\-, +]+\]*)"
)
# takes timestamp, id, and velocity from the following string:
# 1606168027.927264 - DEBUG - Object 3 at self.position=Vector3([428.23973285, 324.60161277,   0.        ]) with self.velocity=Vector3([-0.00059675,  0.00025162,  0.        ]) experiencing 4.426041576865288e-05 forces

with open(filename, "r") as f:
    data = f.readlines()

x, y, ids = list(), list(), list()

for line in data:
    m = pattern.match(line)
    if m:
        x.append(float(m[1]))
        ids.append(int(m[2]))
        if plot_all:
            y.append(ast.literal_eval(m[3]))
        else:
            y.append(sum(ast.literal_eval(m[3])))

# for time, val, _id in zip(x, y, ids):
#    print(f"{time=}: {_id=} - {val=}")

datasets = list()
for i in range(max(ids)):
    valid = [[t, v, _i] for t, v, _i in zip(x, y, ids) if _i == i]
    datasets.extend(valid)

ids = [line[2] for line in datasets]
max_id = max(ids)
time_start = min([line[0] for line in datasets if line[2] == 1])
time_end = max([line[0] for line in datasets if line[2] == 1])
for id in range(1, max_id + 1):
    yvals = [line[1] for line in datasets if line[2] == id]
    xvals = [line[0] - time_start for line in datasets if line[2] == id]

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
