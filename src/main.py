from fastapi import FastAPI


app = FastAPI(root_path="/api")


@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}