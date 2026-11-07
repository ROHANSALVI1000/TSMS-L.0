from fastapi import FastAPI,Depends,HTTPException
from validation import USER,API
from database import get_db,user_info
from pwdlib import PasswordHash
from sqlalchemy import select
from auth import create_access_token

p=PasswordHash.recommended()


app=FastAPI()

@app.post("/register",response_model=API)
def register(user:USER,db=Depends(get_db)):
    new_user=user_info(
        name=user.name,
        pas=p.hash(user.pas)
     )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.post("/login")
def login(user:USER,db=Depends(get_db)):
    name=user.name

    statement=select(user_info).where(user_info.name==name)
    y=db.execute(statement)
    z=y.scalars().first()

    if z is None:
        raise HTTPException(
            status_code=401,
            detail="user not found"
        )
    elif  not p.verify(user.pas,z.pas):
        raise HTTPException(
            status_code=401,
            detail="password incorrect"
        )
    else:
       token=create_access_token(z.id)
       print(token)












    

    
