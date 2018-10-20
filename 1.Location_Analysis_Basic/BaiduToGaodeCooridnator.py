import pandas as pd
import requests
import json
import sys
from time import ctime


def BD2GD(lng, lat):
    cooridnate = "{},{}".format(lng, lat)

    url_template = "https://restapi.amap.com/v3/assistant/coordinate/convert?locations={}&coordsys=baidu&output=JSON&key={}"

    key = "6db69300890974d6b83b474efc6ea792"
    if cooridnate != "":
        url = url_template.format(cooridnate, key)
        request = requests.get(url)
        js = json.loads(request.text)

    if js["status"] == "1":
        GDCoordinate = js["locations"]
        lng, lat = str(GDCoordinate).split(",")
        return float(lat), float(lng)
    else:
        return 0, 0


ds = pd.read_excel("C:\\Users\\bwan19\\Desktop\\TZ Analysis\\Consumer Info\\CONSUMER_SH_FA18.xlsx",
                   encoding="utf8")

# ds["GDlat"] = 0
# ds['GDlng'] = 0

startNum = 41089
errorTime = 0

while (errorTime <= 20):

    currentNum = 0

    try:
        myds = ds.loc[startNum:]

        for i in myds.index:
            currentNum = i

            lat = myds.loc[i]["lat"]
            lng = myds.loc[i]["lng"]

            GDlat, GDlng = BD2GD(lng, lat)

            # 维度
            myds.iloc[i - startNum, 6] = GDlat
            # 经度
            myds.iloc[i - startNum, 7] = GDlng

            if i % 10 == 0:
                print("{} - {}".format(i, ctime()))
            #
            # if currentNum == 10:
            #     break
    except:
        print(sys.exc_info()[0])

    finally:
        ds.loc[startNum:] = myds
        print("Erro @ {}".format(currentNum))

        errorTime += 1

        startNum = currentNum

ds.to_excel(
    "C:\\Users\\bwan19\\Desktop\\TZ Analysis\\Consumer Info\\CONSUMER_SH_FA18.xlsx",
    encoding="utf8")

print("done")
