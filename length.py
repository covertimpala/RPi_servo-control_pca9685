import json
with open('data.json', 'r+') as f:
    global data
    data = json.load(f)
file_length = (len(data))