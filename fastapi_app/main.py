from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import projects, feedback, auth

app = FastAPI(title="Student Project Portal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects.router)
app.include_router(feedback.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "API is running"}