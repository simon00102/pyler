# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users, admins

app = FastAPI(version="v1.0.0", title="Pyler Auth Server", description="Pyler Auth Server API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(users.router)
app.include_router(admins.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
