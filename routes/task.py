from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from models.task import Task
from schemas.task import TaskCreate, TaskUpdate, TaskResponse,age
from dependencies.auth import get_current_user

router = APIRouter(prefix="/api/v1/tasks", tags=["Tasks"])

@router.post("/create",response_model=TaskResponse)
def create_task(task:TaskCreate,db:Session=Depends(get_db),user=Depends(get_current_user)):
    new_task=Task(
        title=task.title,
        description=task.description,
        owner_id=user["id"],
        is_completed=False

    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
@router.get("/age/{age}")
def show_age(age:age,user=Depends(get_current_user)):
    return {"age":f"age is {age}"}


@router.get("/",response_model=list[TaskResponse])
def get_task(db:Session=Depends(get_db),user=Depends(get_current_user)):
   

    
    tasklist=db.query(Task).filter(Task.owner_id==user["id"]).all()
    if not tasklist:
        raise HTTPException(status_code=404,detail="task not found")
    if user['role']=="admin":
        tasklist=db.query(Task).all()


    
    return tasklist

@router.get("/{task_id}",response_model=TaskResponse)
def getTask(task_id:int,db:Session=Depends(get_db),user=Depends(get_current_user)):
    task=db.query(Task).filter(Task.id==task_id).first()
    
    
    return task
@router.put("/update/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    update_data: TaskUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    present_data = db.query(Task).filter(Task.id == task_id).first()

    if not present_data:
        raise HTTPException(status_code=404, detail="Task not found to update")

    # OPTIONAL BUT IMPORTANT: ownership check
    if present_data.owner_id != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    update_dict = update_data.model_dump(exclude_unset=True)

    allowed_fields = {"title", "description", "is_completed"}

    for key, value in update_dict.items():
        if key in allowed_fields:
            setattr(present_data, key, value)

    db.commit()
    db.refresh(present_data)

    return present_data

@router.delete("/delete/{task_id}")
def delete_task(task_id:int,db:Session=Depends(get_db),user=Depends(get_current_user)):
    task=db.query(Task).filter(Task.id==task_id).first()
    if task:
        db.delete(task)
        db.commit()
    
    return {"message":f"{task_id} is deleted"}




