import json
from pathlib import Path
import os
p = Path(__file__).parents[1]
dataDir = os.path.join(p, "data")
dataPath = dataDir + "/data.json"
def loadData():
    with open(dataPath, 'r') as dataFile:
        data = dataFile.read()
    obj = json.loads(data)
    dic = {
        "face_avg": obj["face_avg"],
        "contact_range" :obj["contact_range"],
        "mask_lower_percent" : obj["mask_lower_percent"],
        "wrong_count" : obj["wrong_count"]
    }
    return dic
