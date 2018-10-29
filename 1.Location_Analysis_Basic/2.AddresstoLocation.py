# ----------------------------
# Convert Address to Coordinate
# ----------------------------

import pandas as pd
import requests
import json
import sys
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

startNum = 81871
errorTime = 0
endNum = 0

while (errorTime <= 20):

    currentNum = 0

    try:
        if endNum != 0:
            myds = ds.loc[startNum:endNum]
        else:
            myds = ds.loc[startNum:]

        for i in myds.index:
            currentNum = i

            if str(myds.loc[i]["Addr"]) == "nan":
                continue

            address = "上海市" + myds.loc[i]["Addr"]

            lat, lng = GetCoordinateOnBaidu(address)

            # 维度
            myds.iloc[i - startNum, 4] = lat
            # 经度
            myds.iloc[i - startNum, 5] = lng

            if i % 10 == 0:
                print("{} - {}".format(i, ctime()))
    except:
        print(sys.exc_info()[0])

    finally:
        if endNum != 0:
            ds.loc[startNum:endNum] = myds
        else:
            ds.loc[startNum:] = myds
            print("Erro @ {}".format(currentNum))

            errorTime += 1

            startNum = currentNum

ds.to_excel(
    "C:\\Users\\bwan19\\Desktop\\TZ Analysis\\Consumer Info\\CONSUMER_SH_FA18.xlsx",
    encoding="utf8")

print("done")
