import pandas as pd
import pymssql

conn = pymssql.connect(host="HP1410L783CDCE\SQLEXPRESS", user="NIKE\\BWan19", password="Adi790430!",
                       database="D2N")
# ds = pd.read_sql("select * from FA18_withReturnDays", conn)
#
# dsdigital = ds
#
# # Load Transcation Data
# # dsdigital = pd.concat([pd.read_csv("/Users/wanghaoyi/Desktop/D2N/FA18NIKE_withReturnDays.csv", encoding="utf-16"),
# #                        pd.read_csv("/Users/wanghaoyi/Desktop/D2N/FA18TMALL_withReturnDays.csv", encoding="utf-16")])
#
# # Load Consumer Data
# # dsConsumer = pd.read_excel("/Users/wanghaoyi/Desktop/D2N/CONSUMER_SH_FA18.xlsx")
# dsConsumer = pd.read_sql("select * from CONSUMER_SH_FA18", conn)
#
# # Merge Consumer and Transcation
# demandGroup = dsdigital.groupby("Consumer")["Net_Demand_Amt"].sum()
# demandGroup = demandGroup.reset_index()
# demandGroup.rename(columns={"Net_Demand_Amt": "Demand"}, inplace=True)
#
# # Formatting new Data set
# newds = dsConsumer.merge(demandGroup, how='inner')
# newds["coordniater"] = newds.apply(lambda x: "{},{}".format(x["GDlng"], x["GDlat"]), axis=1)
# newds = newds[newds["lat"] != 0]
#
# # Remove abnormal data
# # newds[newds["Addr"].str.contains("1324810")].drop(inplace=True)
#
# # Export new data set
# newds[["coordniater", "Demand"]].to_csv("CoordDemand.csv")
# # newds.to_csv("/Users/wanghaoyi/Desktop/D2N/CoordDemand.csv")

# -------------------------
ds = pd.read_sql("select * from FA18_withReturnDays_SH_TZ", conn)
ds["coordniater"] = ds.apply(lambda x: "{},{}".format(x["GDlng"], x["GDlat"]), axis=1)
ds.rename(columns={"Net_Demand_Amt": "Demand"}, inplace=True)
ds = ds[ds["GDlat"] != 0]

ds = ds[ds["Store_Nm"] != "SWOOSH"]

ds[["coordniater", "Demand"]].to_csv("CoordDemand.csv")
