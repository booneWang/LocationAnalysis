import pandas as pd
import requests
import json
import threading
from time import ctime


def GetCoordinateOnBaidu(address):
    url_template = "http://api.map.baidu.com/geocoder/v2/?address={0}&output=json&ak={1}"
    myAK = "RmTWSrlP7ijaCUadIUArGrmXv9ZsKgSg"
    if address != "":
        url = url_template.format(address, myAK)
        request = requests.get(url)
        js = json.loads(request.text)

        if js["status"] == 0:
            lat, lng = js["result"]["location"]["lat"], js["result"]["location"]["lng"]

            return float(lat), float(lng)
        else:
            return 0, 0


def GetCoordinateOnGaodei(address):
    url_template = "https://restapi.amap.com/v3/geocode/geo?address={0}&key={1}&output=JSON"
    key = "6db69300890974d6b83b474efc6ea792"
    if address != "":
        url = url_template.format(address, key)
        request = requests.get(url)
        js = json.loads(request.text)

        # check result 1:successful, 0:failed
        if js["status"] == "1" and js["count"] != "0":
            lng, lat = js["geocodes"][0]["location"].split(",")

            return float(lat), float(lng)
        else:
            return 0, 0


ds = pd.read_excel("C:\\Users\\bwan19\\Desktop\\TZ Analysis\\Consumer Info\\CONSUMER_SH_FA18.xlsx",
                   encoding="utf8")
ds["lat"] = 0
ds['lng'] = 0


# 100 sample for test purpose
# ds = ds.head(5000)
# ds.reset_index(inplace=True)
# del ds["index"]

# How many Cycle need to run
# ds = ds.loc[:100]

def updateCoordinator(tNum, ds, startNum, endNum):
    if endNum != 0:
        myds = ds.loc[startNum:endNum]
    else:
        myds = ds.loc[startNum:]

    for i in myds.index:
        address = myds.loc[i]["City"] + myds.loc[i]["Addr"]

        lat, lng = GetCoordinateOnBaidu(address)

        # 维度
        myds.iloc[i - startNum, 4] = lat
        # 经度
        myds.iloc[i - startNum, 5] = lng

        if i % 10 == 0:
            print("t({}){} - {}".format(tNum, i, ctime()))

    if endNum != 0:
        ds.loc[startNum:endNum] = myds
    else:
        ds.loc[startNum:] = myds


threads = []
threads.append(threading.Thread(target=updateCoordinator, args=(1, ds, 0, 100)))
threads.append(threading.Thread(target=updateCoordinator, args=(2, ds, 101, 200)))

for t in threads:
    t.setDaemon(True)
    t.start()
t.join()

# ds.to_excel(
#     "C:\\Users\\bwan19\\Desktop\\TZ Analysis\\Consumer Info\\CONSUMER_SH_FA18_201708_201808_withCoordinator.xlsx",
#     encoding="utf8")

print("done")
