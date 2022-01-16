def leng(file):
    import json
    with open(file, 'r+') as f:    # open('data.json', 'r+')
        global data
        data = json.load(f)
    file_length = (len(data)) - 1
    print(file_length)