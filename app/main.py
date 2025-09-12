from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import health, employees, auth, schedules, admin_seed, tasks, dev_tools
from app.db import init_db

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await init_db()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(employees.router)
app.include_router(schedules.router)
app.include_router(tasks.router)
app.include_router(admin_seed.router)
app.include_router(dev_tools.router)