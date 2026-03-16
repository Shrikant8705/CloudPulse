from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def get_msg():
    return{"Hello":"World"}
