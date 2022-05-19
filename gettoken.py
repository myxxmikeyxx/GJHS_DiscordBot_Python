import json
# https://realpython.com/python-return-statement/

def gettoken():
    data = json.load(open("config.json"))
    for key, value in data.items():
        if key == "token":
            # print(value)
            token=value
    return( {"token" : token})