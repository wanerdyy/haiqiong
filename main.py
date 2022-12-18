# This is a sample Python script.
import pandas as pd
from math import *
import numpy as np
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


"""
读取movies文件，设置列名为’videoId', 'title', 'genres'
读取ratings文件，设置列名为'userId', 'videoId', 'rating', 'timestamp'
通过两数据框之间的 videoId 连接
保存'userId', 'rating', 'videoId', 'title'为data数据表
"""
movies = pd.read_csv("./movies.csv", names=['videoId', 'title', 'genres'])
ratings = pd.read_csv("./ratings.csv",names=['userId', 'videoId', 'rating', 'timestamp'])
data = pd.merge(movies, ratings, on='videoId')
data[['userId', 'rating', 'videoId', 'title']].sort_values('userId').to_csv('./data.csv',index=False)

"""
新建一个data字典存放每位用户评论的电影和评分, 如果字典中没有某位用户，则使用用户ID来创建这位用户,否则直接添加以该用户ID为key字典中
"""
file = open("./data.csv",'r', encoding='UTF-8')
data = {}
for line in file.readlines():
    line = line.strip().split(',')
    if not line[0] in data.keys():
        data[line[0]] = {line[3]:line[1]}
    else:
        data[line[0]][line[3]] = line[1]

"""
找到两位用户共同评论过的电影,然后计算两者之间的欧式距离，最后算出两者之间的相似度，欧式距离越小两者越相似
"""


def Euclidean(user1, user2):
    user1_data = data[user1]
    user2_data = data[user2]
    distance = 0
    for key in user1_data.keys():
        if key in user2_data.keys():
            distance += pow(float(user1_data[key]) - float(user2_data[key]), 2)

    return 1 / (1 + sqrt(distance))

"""
计算某个用户与其他用户的相似度
"""
def top_simliar(userID):
    res = []
    for userid in data.keys():
        # 排除与自己计算相似度
        if not userid == userID :
            simliar = Euclidean(userID, userid)
            res.append((userid, simliar))
    res.sort(key=lambda val: val[1])
    return res[:4]

"""
从控制台输入需要推荐的用户ID，如果用户不在原始数据集中则报错，重新输入
"""
getIdFlag = 0
while not getIdFlag:
    inputUid = str(input("请输入用户ID\n"))
    try:
        uid = data[inputUid]
        getIdFlag = 1
    except Exception:
        print("用户ID错误，请重新输入\n")

"""
根据与当前用户相似度最高的用户评分记录，按降序排列，推荐出改用户还未观看的评分最高的10部电影
"""
def recommend(user):
    top_sim_user = top_simliar(user)[0][0]
    items = data[top_sim_user]
    recommendations = []
    for item in items.keys():
        if item not in data[user].keys():
            recommendations.append((item, items[item]))
    recommendations.sort(key=lambda val: val[1], reverse=True)  # 按照评分排序
    return recommendations[:10]

"""
根据输入的用户ID，输出为他推荐的影片
"""
Recommendations = recommend(inputUid)
print("为用户" + inputUid + "推荐下列评分最高的十部影片\n")
for video in Recommendations:
    print(video)