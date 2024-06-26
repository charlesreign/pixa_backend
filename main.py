from fastapi import FastAPI, Request, status, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from db import models
from db.database import engine
from routers import user, post, comment
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from auth import authentication
from config import env

api = FastAPI()

api.include_router(user.router)
api.include_router(post.router)
api.include_router(authentication.router)
api.include_router(comment.router)


models.Base.metadata.create_all(engine)

api.mount("/images", StaticFiles(directory="images"), name="images")


origin = [env.FRONT_END_BASE_URL]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs", status_code=status.HTTP_301_MOVED_PERMANENTLY)
