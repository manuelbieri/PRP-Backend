import uvicorn
import database.ToDoDatabase as dB

from fastapi import Depends, FastAPI
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from typing import List


def get_database() -> dB.ToDoDatabase:
    return dB.ToDoDatabase("todo.db", "items")


app: FastAPI = FastAPI()
router = InferringRouter()


@cbv(router)
class Requests:
    database: dB.ToDoDatabase = Depends(get_database)

    @router.get("/items")
    def get_all_items(self) -> List[dict]:
        # Step 4: Use `self.<dependency_name>` to access shared dependencies
        return self.database.readAllEntries()


app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
