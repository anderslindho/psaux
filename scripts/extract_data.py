import ast
import re


def get_data_from(filename: str = None) -> list:
    pattern = re.compile(
        r"^(\d*.\d*).+(?<=Object )(\d+).+(?<=self.position=)\w*\((\[[0-9.,\- e+]+])\).+\((\[[0-9.e\-, +]+\]*)"
    )
    # takes timestamp, id, position, and velocity from the following string:
    # 1606168027.927264 - DEBUG - Object 3 at self.position=Vector3([428.23973285, 324.60161277,   0.        ]) with self.velocity=Vector3([-0.00059675,  0.00025162,  0.        ]) experiencing 4.426041576865288e-05 forces

    with open(filename, "r") as f:
        data = f.readlines()

    dataset = list()
    for line in data:
        m = pattern.match(line)
        if m:
            time = float(m[1])
            ids = int(m[2])
            positions = ast.literal_eval(m[3])
            velocities = ast.literal_eval(m[4])
            dataset.append([time, positions, velocities, ids])

    return dataset
