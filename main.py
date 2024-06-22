from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List
from bson import ObjectId

app = FastAPI()
client = MongoClient('mongodb+srv://gayashanrandimagamage:2692g.rg0968CJ@cluster0.kdywp1p.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['main']
cluster = db['user']

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    firstName :str
    lastName :str
    password :str

class UserDetails(BaseModel):
    _id : str
    firstName : str
    lastName : str
    password : str

def all_users():
    alll = list(cluster.find())
    for item in alll:
        item['_id'] = str(item['_id'])
    return alll

@app.post('/user')
def user(user: User):
    cluster.insert_one({
        'first name' : user.firstName,
        'last name' : user.lastName,
        'password' : user.password
    })
    al = all_users()
    return al

@app.get('/allUser')
async def allUser():
    al = all_users()
    return al  

@app.delete('/delete-user/{id}')
async def deleteUser(id : str):
    userId = ObjectId(id)
    cluster.delete_one({'_id' : userId})
    al = all_users()
    return al

@app.patch('/update-user/{:userID}')
async def updateUser(userID:str, userDetails : UserDetails):
    cluster.update_one({'_id' : ObjectId(userID)}, { '$set' : {
        'first name' : userDetails.firstName,
        'last name' : userDetails.lastName,
        'password' : userDetails.password
    }})
    al = all_users()
    return al