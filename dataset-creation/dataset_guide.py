import time
import numpy as np
import random
features = [
    "fist"
]
"""
    "thumb",
    "index",
    "middle",
    "ring",
    "pinky",
    "fist",
    "shaka",
    "woo",
    "fight on",
    "birdie"
"""
def count_down(i):
    for x in range(i):
        print(i - x)
        time.sleep(1)
"""
for feature in features:
    for x in range(10):
        print(feature)
        count_down(5)
        print("break")
        count_down(3)
"""
for x in range(50):
    arr = np.arange(len(features))
    np.random.shuffle(arr)
    for val in arr:
        print(features[val])
        count_down(random.randint(3, 5))
        print("stop")
        count_down(1)
