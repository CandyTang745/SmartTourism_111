import pymongo
import pandas as pd
from datetime import datetime

# 读取 CSV 文件
file_path = "scenic_spots_introduction1_5A.csv"
df = pd.read_csv(file_path, encoding="utf-8")


# 连接 MongoDB
client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db = client["tourism_db"]
collection = db["scenic_spots"]


# 插入数据
data_list = []
for _, row in df.iterrows():
    # 处理图片路径（可能为空）
    images = row["图片路径"].split(", ") if pd.notna(row["图片路径"]) else []

    # 构造 MongoDB 文档
    scenic_spot = {
        "name": row["景区名称"],
        "introduction": row["简介"],
        "image_paths": images,
        "created_at": datetime.utcnow()  # 记录插入时间
    }
    data_list.append(scenic_spot)

# 批量插入 MongoDB
collection.insert_many(data_list)

print("数据导入完成！")
# result = collection.find_one({"name": "古塔公园"})
# print(result)






