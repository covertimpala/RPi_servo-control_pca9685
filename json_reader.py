import json
import __main__


def readfile():
    with open(__main__.jsonfile, 'r+') as f:  # with open('data.json', 'r+') as f:
        data = json.load(f)
        f.seek(0)

    print("ref num:", __main__.ref)
    global val
    val = data[str(__main__.ref)]   # data extraction using ref string
    print(val)