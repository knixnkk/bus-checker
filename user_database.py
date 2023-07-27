import pymongo
from pymongo import MongoClient
import os
import datetime
user = os.environ.get("DB_USER")
secret = os.environ.get("DB_PASS")

cluster = pymongo.MongoClient(f"mongodb://localhost:27017")
db = cluster["pymongo_auth"]
collection = db["users"]
def add_user(user):
    return collection.insert_one(user)

def check_for_user(email):
    if collection.find_one({"citizenid" : email}):
        return True
    else:
        return False
def checkUser(string):
    if collection.find_one({"username" : string}):
        return True
    else:
        return False
def checkTelephone(string):
    if collection.find_one({"telephone" : string}):
        return True
    else: 
        return False
def getData(string):
    collections = collection.find()
    for item in collections:
        if item['citizenid'] == str(string):
            return item['citizenid'], item["username"], item["telephone"], item["status"], item['seat']
def updateSeat(string, number):
    collections = collection.find()
    for item in collections:
        if item['citizenid'] == str(string):
            collection.update_one({
                "_id": item["_id"]
                },
                {
                "$set": {
                    "seat": int(number),
                }
            })
def updateStatustoUp(string):
    mydate = datetime.datetime.now()
    timenow = (mydate.strftime("%X"))
    collections = collection.find()
    for item in collections:
        if item['citizenid'] == str(string):
            collection.update_one({
                "_id": item["_id"]
                },
                {
                "$set": {
                    "status": "UP",
                }
            })
            collection.update_one({
                "_id": item["_id"]
                },
                {
                "$set": {
                    "time": timenow,
                }
            })
def updateStatustoDown(string):
    mydate = datetime.datetime.now()
    timenow = (mydate.strftime("%X"))
    collections = collection.find()
    for item in collections:
        if item['citizenid'] == str(string):
            collection.update_one({
                "_id": item["_id"]
                },
                {
                "$set": {
                    "status": "DOWN",
                }
            })
            collection.update_one({
                "_id": item["_id"]
                },
                {
                "$set": {
                    "time": timenow,
                }
            })
def updateTable():
    xList = []
    collections = collection.find()
    for i in collections:
        x = (i["username"], i["status"], i["time"])
        xList.append(x)
    return xList
def get_user(email):
    return collection.find_one({"citizenid" : email})

def getAllUser():
    allUser = []
    collections = collection.find()
    for i in collections:
        allUser.append(i)
    return len(allUser)
def getUserUp():
    UpUser = []
    collections = collection.find()
    for i in collections:
        if i["status"] == "UP":
            UpUser.append(i)
    return len(UpUser)
# def delete_user(user):
#     pass
    
# def update_user(user):
    

