"""
utility script to check why velocity for some entities seem to get a bump
possibly when collisions between other planets occur
"""

import ast
import re

from matplotlib import pyplot as plt

plot_all = True

fname = "2020-Nov-23 21:55.log"
pattern = re.compile(r"^(\d*.\d*).+(?<=self.velocity=)\w+\((\[\s[0-9., -e]+\])\)")
# takes timestamp and velocity from the following string:
# 1606159259.863943 - DEBUG - Planet at self.position=Vector3([512.59534327, 386.48471699,   0.        ]) with self.velocity=Vector3([1.42945686e-05, 5.55595142e-06, 0.00000000e+00]) experiencing 0.00011083381409430256 forces

with open(fname, "r") as f:
    data = f.readlines()

x, y = list(), list()

for line in data:
    m = pattern.match(line)
    if m:
        x.append(float(m[1]))
        if plot_all:
            y.append(ast.literal_eval(m[2]))
        else:
            y.append(sum(ast.literal_eval(m[2])))

# for time, val in zip(x, y):
#    print(f"{time=} : {val=}")

plt.xlabel("velocity")
plt.ylabel("time")
plt.title("halp")

# each y entry thus looks like this: [num, num, num]
if plot_all:
    for i, char in enumerate(["x", "y", "z"]):
        plt.plot(x, [pt[i] for pt in y], label="%s" % char)
    plt.legend()
else:
    plt.plot(x, y)

plt.show()
