from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Arjun"}

@app.get("/about")
def intro():
    return {"message": "This is practice notebook to learn about the fastapi."}