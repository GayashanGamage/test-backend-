import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List
from bson import ObjectId
import sib_api_v3_sdk

load_dotenv()

app = FastAPI()
client = MongoClient(os.getenv('mongodb'))
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

# email configeration 
config = sib_api_v3_sdk.Configuration()
config.api_key['api-key'] = os.getenv('brevo')

api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(config))

class User(BaseModel):
    firstName :str
    lastName :str
    password :str

class UserDetails(BaseModel):
    firstName : str
    lastName : str
    password : str

class mailDetail(BaseModel):
    name : str
    reciverMail : str

def all_users():
    alll = list(cluster.find())
    for item in alll:
        item['_id'] = str(item['_id'])
    return alll

@app.post('/user', tags=['crud'])
def user(user: User):
    cluster.insert_one({
        'first name' : user.firstName,
        'last name' : user.lastName,
        'password' : user.password
    })
    al = all_users()
    return al

@app.get('/allUser', tags=['crud'])
async def allUser():
    al = all_users()
    return al  

@app.delete('/delete-user/{id}', tags=['crud'])
async def deleteUser(id : str):
    userId = ObjectId(id)
    cluster.delete_one({'_id' : userId})
    al = all_users()
    return al

@app.patch('/update-user/{userID}', tags=['crud'])
async def updateUser(userID:str, userDetails : UserDetails):
    cluster.update_one({'_id' : ObjectId(userID)}, { '$set' : {
        'first name' : userDetails.firstName,
        'last name' : userDetails.lastName,
        'password' : userDetails.password
    }})
    al = all_users()
    return al

@app.post('/send-mail', tags=['email'])
async def sendMail(mailDetail : mailDetail):
    subject = "My Subject"
    html_content = "<html><body><h1>welcome to ROPAPER </h1></body></html>"
    sender = {"name":"John Doe","email":"gayashan.randimagamage@gmail.com"}
    to = [{"email": mailDetail.reciverMail,"name": mailDetail.name}]
    # cc = [{"email":"example2@example2.com","name":"Janice Doe"}]
    # bcc = [{"name":"John Doe","email":"example@example.com"}]
    # reply_to = {"email":"gayashan.randimagamage@gmail.com","name":"John Doe"}
    headers = {"Some-Custom-Name":"unique-id-1234"}
    # params = {"parameter":"My param value","subject":"New Subject"}
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers, html_content=html_content, sender=sender, subject=subject, template_id=1, params={"username": mailDetail.name})

    api_response = api_instance.send_transac_email(send_smtp_email)
    return api_response