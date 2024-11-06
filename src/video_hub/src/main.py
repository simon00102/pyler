import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from task import generate_statistics
from routers import videos, statistics

# FastAPI lifespan을 활용하여 주기적 작업 설정
@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(generate_statistics())
    yield  # 앱이 실행될 동안 lifespan 유지
    task.cancel()  # 앱 종료 시 주기적 작업도 중지

app = FastAPI(version="v1.0.0", title="Pyler Video Hub Server", description="Pyler Video Hub API", lifespan=lifespan)

# 라우터 추가
app.include_router(videos.router)
app.include_router(statistics.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
