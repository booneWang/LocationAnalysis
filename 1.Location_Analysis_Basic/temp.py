import pandas as pd

ds = pd.read_csv(
    "C:\\Users\\bwan19\\Boone_Document\\# Nwork\\$Projects\\Digital G2N Analysis\\05. Analysis\\Raw Data\Original\\FA18\\FA18NIKE_withReturnDays.csv",
    encoding="UTF-16")

ds1 = pd.read_csv(
    "C:\\Users\\bwan19\\Boone_Document\\# Nwork\\$Projects\\Digital G2N Analysis\\05. Analysis\\Raw Data\Original\\FA18\\FA18TMALL_withReturnDays.csv",
    encoding="UTF-16")

d = pd.concat([ds, ds1])
c = d["Consumer"].unique()

dsc = pd.read_excel("C:\\Users\\bwan19\\Desktop\\TZ Analysis\\Consumer Info\\CONSUMER_SH_201708_201808.xlsx")

d = dsc[dsc["Consumer"].isin(c)]
d.to_excel("C:\\Users\\bwan19\\Desktop\\TZ Analysis\\Consumer Info\\CONSUMER_SH_FA18_201708_201808.xlsx")