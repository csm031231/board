from fastapi import FastAPI

app = FastAPI()  # 애플리케이션 인스턴스 생성

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
