import uvicorn

import secrets

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "abc")
    correct_password = secrets.compare_digest(credentials.password, "abc")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username


@app.get("/")
def read_current_user(username: str = Depends(get_current_username)):
    return {"username": username}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
