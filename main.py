from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def home():
    return 'this is home'

@app.get('/about')
def about():
    return 'this is about page'