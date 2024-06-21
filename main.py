from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List

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


@app.get('/')
def home():
    return 'this is home'

@app.post('/user')
def user(user: User):
    cluster.insert_one({
        'first name' : user.firstName,
        'last name' : user.lastName,
        'password' : user.password
    })
    return allUser()

@app.get('/allUser')
async def allUser():
    alll = list(cluster.find())
    for item in alll:
        item['_id'] = str(item['_id'])
    return alll  
