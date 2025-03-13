from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import user, post, comments

app = FastAPI(title="Board API")

app.include_router(user.router)
app.include_router(post.router)
app.include_router(comments.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
