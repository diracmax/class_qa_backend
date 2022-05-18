import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status, Request
from werkzeug.exceptions import NotFound
from http import HTTPStatus
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from mysql import connector
from interface.repository_interface import UserRepositoryInterface
from db.user_repository import UserRepository
from db.class_repository import ClassRepository
from db.question_repository import QuestionRepository
from fastapi.encoders import jsonable_encoder
from starlette.responses import Response

import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = 30

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app: FastAPI = FastAPI()

# MySQL Connection
config = {
    'user': 'root',
    'password': 'password',
    'host': 'mysql',
    'database': 'db',
    'autocommit': True
}

conn = connector.connect(**config)


class Token(BaseModel):
    access_token: str
    token_type: str


# リクエスト用のモデル
class RequestUser(BaseModel):
    username: str
    password: str


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str):
    user = UserRepository(conn).get(username)
    if user is None:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(
        form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/users")
def create_user(user: RequestUser):
    is_saved = UserRepository(conn).save(user.username, user.password)
    if not is_saved:
        return Response(status_code=400)
    return Response(status_code=201)


@app.get("/classes")
def get_classes():
    class_objects = ClassRepository(conn).get_all_classes()
    return JSONResponse(
        content=[
            {
                "id": class_object.id,
                "name": class_object.name,
                "semester": class_object.semester,
                "year": class_object.year
            }
            for class_object in class_objects
        ]
    )


@app.get("/classes/{class_id}/questions")
def get_questions(class_id: int):
    question_objects = QuestionRepository(conn).get_all_questions_by(class_id)
    response_data = [jsonable_encoder(question_object) for question_object in question_objects]
    # FIXME: datetime型をjson用に書き換える
    return JSONResponse(
        content=[
            {
                "id": question_object["id"],
                "user_id": question_object["user_id"],
                "content": question_object["content"],
                "created_at": question_object["created_at"]
            }
            for question_object in response_data
        ]
    )


class RequestQuestion(BaseModel):
    content: str


@app.post("/test/{classId}")
def post_question(
                  classId: int,
                  requestQuestion: RequestQuestion,
                  token: str = Depends(oauth2_scheme)
                  ):
    return JSONResponse(
        content={
            "token": token,
            "classId": classId,
            "content": requestQuestion.content
        }
    )


@app.get("/")
def read_root():
    return JSONResponse(
        content={"message": "Hello"}
    )


@app.exception_handler(NotFound)
async def handle_404(request: Request, exc: NotFound):
    return JSONResponse(
        status_code=HTTPStatus.NOT_FOUND,
        content={"message": exc.description},
    )


uvicorn.run(app=app, host="0.0.0.0", port=80)
