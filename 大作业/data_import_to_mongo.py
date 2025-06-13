import pymongo
import pandas as pd

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["NIS3317"]
mycol = mydb["filtered_data"]
# 从csv中读取数据
df = pd.read_csv("data/filtered_data.csv", encoding='utf-8-sig')
# 将数据插入到MongoDB中
for index, row in df.iterrows():
    data = row.to_dict()
    mycol.update_one({"title": data["title"], "district": data["district"]}, {"$set": data}, upsert=True)
print("Data imported to MongoDB successfully.")