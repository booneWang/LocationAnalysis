import pandas as pd
import numpy as np
from time import ctime


def IsPtInPoly(sPoint, pointList):
    aLon, aLat = sPoint[0], sPoint[1]
    iSum = 0
    iCount = len(pointList)

    if (iCount < 3):
        return False

    for i in range(iCount):

        pLon1 = pointList[i][0]
        pLat1 = pointList[i][1]

        if (i == iCount - 1):

            pLon2 = pointList[0][0]
            pLat2 = pointList[0][1]
        else:
            pLon2 = pointList[i + 1][0]
            pLat2 = pointList[i + 1][1]

        if ((aLat >= pLat1) and (aLat < pLat2)) or ((aLat >= pLat2) and (aLat < pLat1)):

            if (abs(pLat1 - pLat2) > 0):

                pLon = pLon1 - ((pLon1 - pLon2) * (pLat1 - aLat)) / (pLat1 - pLat2);

                if (pLon < aLon):
                    iSum += 1

    if (iSum % 2 != 0):
        return True
    else:
        return False


# Load point Data Set
dsPoints = pd.read_excel("C:\\Users\\bwan19\\Desktop\\TZ Analysis\\Consumer Info\\CONSUMER_SH_FA18.xlsx",
                         encoding="utf8")
dsPoints["TZ"] = ""

# --
# Load TZ Data
# --
dsTZ = pd.read_excel("C:\\Users\\bwan19\\Desktop\\TZ Analysis\\TZ Definition\\NEW TZ polygon to point_181009.xlsx")
dsTZ = dsTZ[dsTZ["CITY_C"] == "上海市"]

TZList = dsTZ["TZ_ID_FIX"].unique()
TZDic = {}

# Create TZ Coordinate Dictionary
for TZ in TZList:
    # ET_Y = LONGITUDE ; ET_X = latitude

    TZtemp = dsTZ[dsTZ["TZ_ID_FIX"] == TZ][["ET_Y", "ET_X"]]

    # Convert from Dataframe to Array
    TZArray = np.array(TZtemp).tolist()

    TZDic[TZ] = TZArray

# Update TZ against the address
for indexs in dsPoints.index:

    sPoint = list(dsPoints.loc[indexs][["GDlat", "GDlng"]])

    for key in TZDic:
        if IsPtInPoly(sPoint, TZDic[key]):
            dsPoints.iloc[indexs, 8] = key

    if indexs % 100 == 0:
        print("{} - {}".format(indexs, ctime()))

dsPoints.to_excel("C:\\Users\\bwan19\\Desktop\\TZ Analysis\\Consumer Info\\201808ConsumerList_all_withTZ.xlsx")
