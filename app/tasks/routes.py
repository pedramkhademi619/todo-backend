from fastapi import APIRouter, Path, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from app.core.database import get_db
from app.tasks.schemas import *
from app.tasks.models import TaskModel
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix="/todo", tags=["tasks"])


@router.get("/tasks", response_model=List[TaskResponseSchema])
async def retrieve_tasks_list(completed: bool | None = Query(None,
                                                             description="filter tasks basedon their completed or nor"),
                              limit: int = Query(10,
                                                 gt=0, le=50, description="limiting the number of items to retrieve"),
                              offset: int = Query(0,ge=0,description="how many items used for paginationg based on passed items"),

                              db: Session = Depends(get_db)):
    query = db.query(TaskModel)
    if completed:
        query = query.filter(TaskModel.is_completed == completed)
    return query.limit(limit).offset(offset).all()


@router.get("/tasks/{task_id}", response_model=TaskResponseSchema)
async def retrieve_task_detail(task_id: int, db: Session = Depends(get_db)):
    task_obj = db.query(TaskModel).where(TaskModel.id == task_id).one_or_none()

    if task_obj:
        return task_obj
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")


@router.post("/tasks/", response_model=TaskResponseSchema)
async def create_task(request: TaskCreateSchema, db: Session = Depends(get_db)):
    task_obj = TaskModel(**request.model_dump())
    db.add(task_obj)
    db.commit()
    db.refresh(task_obj)
    return task_obj


@router.patch("/tasks/{task_id}", response_model=TaskResponseSchema)
async def update_task(request: TaskUpdateSchema,
                      task_id: int = Path(..., gt=0),
                      db: Session = Depends(get_db)
                      ):
    task_obj = db.query(TaskModel).filter(TaskModel.id == task_id).first()

    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = request.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(task_obj, key, value)

    db.commit()
    db.refresh(task_obj)

    return task_obj


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int = Path(...), db: Session = Depends(get_db)):
    task_obj = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task_obj)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
