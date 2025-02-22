import uvicorn
from fastapi import FastAPI
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database configurations
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CRUD operations
@app.post("/student/")
async def create(name: str, description: str):
    db = SessionLocal()
    db_stud = Item(name=name, description=description)
    db.add(db_stud)
    db.commit()
    db.refresh(db_stud)
    db.close()  
    return db_stud

@app.get("/student/{stud_id}")
async def read(stud_id: int):
    db = SessionLocal()
    item = db.query(Student).filter(Student.id == stud_id).first()
    db.close()  
    return stud

@app.put("/student/{stud_id}")
async def update(stud_id: int, name: str, description: str):
    db = SessionLocal()
    db_stud = db.query(Student).filter(Student.id == stud_id).first()
    if db_stud:
        db_stud.name = name
        db_stud.description = description
        db.commit()
        db.refresh(db_stud)
    db.close()  
    return db_stud

@app.delete("/student/{item_id}")
async def delete(stud_id: int):
    db = SessionLocal()
    db_stud = db.query(Student).filter(Student.id == stud_id).first()
    if db_stud:
        db.delete(db_stud)
        db.commit()
    db.close() 
    return {"message": "Record deleted successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8005)
