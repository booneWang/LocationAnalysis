# 官方API: http://lbs.amap.com/api/webservice/guide/api/convert
# 坐标体系说明：http://lbs.amap.com/faq/top/coordinate/3
# GCJ02->WGS84 Java版本：http://www.cnblogs.com/xinghuangroup/p/5787306.html
# 验证坐标转换正确性的地址：http://www.gpsspg.com/maps.htm
# 以下内容为原创，转载请注明出处。

import math
import pandas as pd
import pymssql


# from xlutils.copy import copy

def GCJ2WGS(lat, lon):
    # location格式如下：locations[1] = "113.923745,22.530824"
    a = 6378245.0  # 克拉索夫斯基椭球参数长半轴a
    ee = 0.00669342162296594323  # 克拉索夫斯基椭球参数第一偏心率平方
    PI = 3.14159265358979324  # 圆周率
    # 以下为转换公式
    x = lon - 105.0
    y = lat - 35.0
    # 经度
    dLon = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x));
    dLon += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0;
    dLon += (20.0 * math.sin(x * PI) + 40.0 * math.sin(x / 3.0 * PI)) * 2.0 / 3.0;
    dLon += (150.0 * math.sin(x / 12.0 * PI) + 300.0 * math.sin(x / 30.0 * PI)) * 2.0 / 3.0;
    # 纬度
    dLat = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x));
    dLat += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0;
    dLat += (20.0 * math.sin(y * PI) + 40.0 * math.sin(y / 3.0 * PI)) * 2.0 / 3.0;
    dLat += (160.0 * math.sin(y / 12.0 * PI) + 320 * math.sin(y * PI / 30.0)) * 2.0 / 3.0;
    radLat = lat / 180.0 * PI
    magic = math.sin(radLat)
    magic = 1 - ee * magic * magic
    sqrtMagic = math.sqrt(magic)
    dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * PI);
    dLon = (dLon * 180.0) / (a / sqrtMagic * math.cos(radLat) * PI);
    wgsLon = lon - dLon
    wgsLat = lat - dLat
    return wgsLat, wgsLon


conn = pymssql.connect(host="HP1410L783CDCE\SQLEXPRESS", user="NIKE\\BWan19", password="Adi790430!",
                       database="D2N")
cur = conn.cursor()

ds = pd.read_sql("select * from CONSUMER_SH_FA18", conn)

ds["GPSlng"], ds["GPSlat"] = 0, 0

for indexs in ds.index:
    gdlat = float(ds.loc[indexs]["GDlat"])
    gdlng = float(ds.loc[indexs]["GDlng"])

    gpslat, gpslng = GCJ2WGS(gdlat, gdlng)

    ds.iloc[indexs, 9] = gpslng
    ds.iloc[indexs, 10] = gpslat

    if indexs % 100 == 0:
        print(indexs)


for indexs in ds.index:
    consumer = ds.loc[indexs]["Consumer"]
    lng = float(ds.loc[indexs]["GPSlng"])
    lat = float(ds.loc[indexs]["GPSlat"])

    sql = "update CONSUMER_SH_FA18 set GPSlat={}, GPSlng={} where Consumer = \'{}\'".format(lat, lng, consumer)

    cur.execute(sql)

    if indexs % 10 == 0:
        print(indexs)
        conn.commit()



