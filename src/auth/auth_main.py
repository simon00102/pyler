from fastapi import FastAPI
#from fastapi.middleware.cors import CORSMiddleware
from database import get_db

app = FastAPI(
    title="Pyler Auth Service",
    description="APIs Pyler Auth Service",
    version="1.0.0",
)

# app.add_middleware(CORSMiddleware,
#                    allow_origins=["*"],
#                    allow_methods=["*"],
#                    allow_headers=["*"])

# Include the routers
# app.include_router(master.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
