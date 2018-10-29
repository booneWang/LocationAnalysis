# ----------------------------
# Process the data from ED&A
# ----------------------------

import pandas as pd
import chardet
import codecs
import numpy as np

#  File Path
filePath = "C:\\Users\\bwan19\\Desktop\\consumer_info.csv"

# Read file encoding
# with open(filePath, "rb") as f:
f = open(filePath, "rb")
data = f.read()
codeType = chardet.detect(data)['encoding']

in_enc = codeType
out_enc = "UTF-16"

in_enc = in_enc.upper()
out_enc = out_enc.upper()

# Convert the file code, ignore error and export
f = codecs.open(filePath, 'r', in_enc, errors="ignore")
new_content = f.read()
codecs.open(filePath, 'w', out_enc).write(new_content)

# Load the file with split
ds = pd.read_csv("C:\\Users\\bwan19\\Desktop\\consumer_info1.csv", encoding="UTF-16", sep="\|\|,\|\|", engine="python")

# Formatting the file
ds.columns = ["Consumer", "City", "Dist", "Addr"]
ds["Consumer"] = ds["Consumer"].apply(lambda x: x.replace("||", ""))
ds["Addr"] = ds["Addr"].apply(lambda x: x.replace("||", ""))

# Export the final file
ds.to_csv("C:\\Users\\bwan19\\Desktop\\consumer_201708_201808.csv", encoding="UTF-8")

###################
ds["City"] = ds["City"].replace(np.nan, "")
ds["Dist"] = ds["Dist"].replace(np.nan, "")
ds[(ds["City"].str.contains("上海")) | (ds["Addr"].str.contains("上海市"))].to_excel(
    "C:\\Users\\bwan19\\Desktop\\CONSUMER_SH_201708_201808.xlsx")
