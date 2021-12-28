import json
from __main__ import ref

with open('data.json', 'r+') as f:
    data = json.load(f)

print("ref num:", ref)
val = data[str(ref)]   # data extraction using ref string
print(val)