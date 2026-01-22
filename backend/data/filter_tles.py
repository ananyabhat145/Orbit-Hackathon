import random

INPUT_FILE = "all_tles.txt"        
OUTPUT_FILE = "sample_tles.txt"
TARGET_OBJECTS = 400               

with open(INPUT_FILE, "r") as f:
    lines = f.readlines()

# Each object = 3 lines
objects = [lines[i:i+3] for i in range(0, len(lines), 3)]

print("Total objects:", len(objects))

# Randomly sample objects
sampled = random.sample(objects, TARGET_OBJECTS)

with open(OUTPUT_FILE, "w") as f:
    for obj in sampled:
        f.writelines(obj)

print("Saved", TARGET_OBJECTS, "objects to", OUTPUT_FILE)
